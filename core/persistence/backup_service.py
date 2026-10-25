"""Safe SQLite backup and restore services.

The service deliberately operates on SQLite files rather than copying selected
tables.  SQLite's online backup API therefore includes every table, including
credentials or application tables added in the future.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import time
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional


class BackupError(RuntimeError):
    """Base class for backup and restore failures."""


class InvalidBackupError(BackupError, ValueError):
    """Raised when a file is not a valid, readable SQLite database."""


class BackupConfirmationRequired(BackupError):
    """Raised when a restore was requested without explicit confirmation."""


@dataclass(frozen=True)
class DatabaseValidation:
    path: Path
    table_count: int
    page_count: int
    user_version: int


@dataclass(frozen=True)
class BackupResult:
    path: Path
    valid: bool
    table_count: int
    page_count: int


@dataclass(frozen=True)
class RestoreResult:
    source: Path
    target: Path
    dry_run: bool
    restored: bool
    pre_restore_backup: Optional[Path]
    validation: DatabaseValidation


ProgressCallback = Callable[[int, int], None]


class BackupService:
    """Back up and restore one application SQLite database."""

    def __init__(self, database_path: os.PathLike[str] | str, dispose_callback=None):
        self.database_path = Path(database_path).expanduser().resolve()
        self.dispose_callback = dispose_callback

    @staticmethod
    def _ensure_sqlite_header(path: Path) -> None:
        try:
            with path.open("rb") as stream:
                header = stream.read(16)
        except OSError as exc:
            raise InvalidBackupError(f"Unable to read SQLite file: {path}") from exc
        if header != b"SQLite format 3\x00":
            raise InvalidBackupError(f"File is not SQLite format 3: {path}")

    def validate_database(self, path: os.PathLike[str] | str) -> DatabaseValidation:
        """Validate SQLite format, schema readability, and integrity."""
        candidate = Path(path).expanduser().resolve()
        if not candidate.is_file():
            raise InvalidBackupError(f"SQLite file does not exist: {candidate}")
        self._ensure_sqlite_header(candidate)

        try:
            with closing(sqlite3.connect(candidate.as_uri() + "?mode=ro", uri=True)) as connection:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                if str(integrity).lower() != "ok":
                    raise InvalidBackupError(
                        f"SQLite integrity check failed for {candidate}: {integrity}"
                    )
                page_count = int(connection.execute("PRAGMA page_count").fetchone()[0])
                user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
                table_count = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM sqlite_master "
                        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                    ).fetchone()[0]
                )
                connection.execute("SELECT name FROM sqlite_master LIMIT 1").fetchall()
        except InvalidBackupError:
            raise
        except sqlite3.DatabaseError as exc:
            raise InvalidBackupError(f"SQLite validation failed for {candidate}: {exc}") from exc

        return DatabaseValidation(candidate, table_count, page_count, user_version)

    def create_backup(
        self,
        destination: os.PathLike[str] | str,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> BackupResult:
        """Create a consistent backup using ``sqlite3.Connection.backup``."""
        source = self.database_path
        target = Path(destination).expanduser().resolve()
        if source == target:
            raise ValueError("Backup destination must differ from the running database")
        self.validate_database(source)
        target.parent.mkdir(parents=True, exist_ok=True)

        temporary = self._temporary_path(target)
        try:
            self._online_copy(source, temporary, progress_callback)
            copied = self.validate_database(temporary)
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()

        return BackupResult(target, True, copied.table_count, copied.page_count)

    def backup(self, destination, progress_callback=None):
        """Convenience alias for :meth:`create_backup`."""
        return self.create_backup(destination, progress_callback)

    def verify_backup(self, path):
        """Convenience alias for :meth:`validate_database`."""
        return self.validate_database(path)

    def restore(
        self,
        source: os.PathLike[str] | str,
        *,
        confirmed: bool = False,
        dry_run: bool = False,
        pre_restore_backup: os.PathLike[str] | str | None = None,
        dispose_callback=None,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> RestoreResult:
        """Validate or restore a backup without deleting the live database.

        The source is staged and validated, then the current database is backed
        up before SQLite copies the staged snapshot into the existing live
        database in one destination transaction. Never unlink/replace the live
        file: doing so would strand open connections and WAL sidecars.

        The required callback must close app sessions and call engine.dispose.
        The caller must prevent application writes throughout this operation
        and reload cached application state after success.
        """
        if not dry_run and not confirmed:
            raise BackupConfirmationRequired("Restore requires explicit user confirmation")

        source_path = Path(source).expanduser().resolve()
        target = self.database_path
        if source_path == target:
            raise ValueError("Restore source must differ from the running database")
        source_validation = self.validate_database(source_path)
        self._validate_compatible_schema(source_path)

        if dry_run:
            return RestoreResult(source_path, target, True, False, None, source_validation)

        if not target.is_file():
            raise InvalidBackupError(f"Running database does not exist: {target}")

        callback = dispose_callback or self.dispose_callback
        if not callable(callback):
            raise BackupError("Restore requires a database session/engine disposal callback")
        pre_restore = self._resolve_pre_restore_path(pre_restore_backup)
        if pre_restore in (source_path, target):
            raise ValueError("Pre-restore backup must differ from source and live database")

        temporary = self._temporary_path(target)
        try:
            self._online_copy(source_path, temporary, progress_callback)
            self.validate_database(temporary)
            self._validate_compatible_schema(temporary)
            callback()
            self.create_backup(pre_restore)
            self._online_copy(temporary, target, progress_callback)
            restored_validation = self.validate_database(target)
        finally:
            if temporary.exists():
                temporary.unlink()

        return RestoreResult(
            source_path,
            target,
            False,
            True,
            pre_restore,
            restored_validation,
        )

    def restore_database(self, source, **kwargs):
        """Convenience alias for :meth:`restore`."""
        return self.restore(source, **kwargs)

    @staticmethod
    def _temporary_path(target: Path) -> Path:
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        os.close(descriptor)
        path = Path(name)
        return path

    def _resolve_pre_restore_path(self, path: os.PathLike[str] | str | None) -> Path:
        if path is not None:
            return Path(path).expanduser().resolve()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        return self.database_path.with_name(f"{self.database_path.stem}.pre-restore-{stamp}.db")

    def _validate_compatible_schema(self, source: Path) -> None:
        """Reject unrelated or older databases missing current app columns."""
        self.validate_database(self.database_path)
        with closing(sqlite3.connect(self.database_path.as_uri() + "?mode=ro", uri=True)) as live:
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as candidate:
                for (name,) in live.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
                    quoted = '"' + name.replace('"', '""') + '"'
                    expected = {(row[1], row[2].upper(), row[5]) for row in live.execute(f"PRAGMA table_info({quoted})")}
                    actual = {(row[1], row[2].upper(), row[5]) for row in candidate.execute(f"PRAGMA table_info({quoted})")}
                    if not expected.issubset(actual):
                        raise InvalidBackupError(f"Backup schema is incompatible with current table: {name}")
                if candidate.execute("PRAGMA user_version").fetchone() != live.execute("PRAGMA user_version").fetchone():
                    raise InvalidBackupError("Backup database schema version differs from current database")

    @staticmethod
    def _online_copy(source: Path, destination: Path, progress_callback=None) -> None:
        try:
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as source_connection, closing(sqlite3.connect(destination)) as destination_connection:
                deadline = time.monotonic() + 60
                def progress(status, remaining, total):
                    if time.monotonic() > deadline:
                        raise BackupError("SQLite backup timed out; close active database writers and retry")
                    if progress_callback is not None:
                        progress_callback(total - remaining, total)

                source_connection.backup(destination_connection, pages=100, progress=progress)
                destination_connection.commit()
        except sqlite3.DatabaseError as exc:
            raise BackupError(f"SQLite online backup failed: {exc}") from exc
