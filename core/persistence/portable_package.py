"""Versioned, validated application export/import packages.

The portable package deliberately contains the complete SQLite database rather
than a hand-maintained list of tables.  This keeps configuration, calibration,
results, maintenance history, and future application tables together when a
user moves SpectraSoft to another device.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
import zipfile
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .backup_service import (
    BackupConfirmationRequired,
    BackupService,
    DatabaseValidation,
    InvalidBackupError,
    RestoreResult,
)


PACKAGE_FORMAT = "spectrasoft-portable-data"
PACKAGE_VERSION = 1
DATABASE_MEMBER = "database.db"
MANIFEST_MEMBER = "manifest.json"
MAX_PACKAGE_BYTES = 512 * 1024 * 1024


class PortablePackageError(RuntimeError):
    """Base class for portable package failures."""


class InvalidPortablePackageError(PortablePackageError, ValueError):
    """Raised when a package is missing, malformed, unsafe, or incompatible."""


@dataclass(frozen=True)
class PortablePackageValidation:
    path: Path
    format: str
    package_version: int
    created_at: str
    database: DatabaseValidation
    tables: tuple[str, ...]


@dataclass(frozen=True)
class PortableExportResult:
    path: Path
    database: DatabaseValidation
    tables: tuple[str, ...]


@dataclass(frozen=True)
class PortableImportResult:
    package: Path
    restore: RestoreResult
    validation: PortablePackageValidation


class PortablePackageService:
    """Create, inspect, and safely import complete application data packages."""

    def __init__(self, database_path: os.PathLike[str] | str, dispose_callback=None):
        self.database_path = Path(database_path).expanduser().resolve()
        self.backup_service = BackupService(self.database_path, dispose_callback=dispose_callback)

    def export_package(self, destination: os.PathLike[str] | str) -> PortableExportResult:
        """Write a validated ZIP package containing the complete live database."""
        target = Path(destination).expanduser().resolve()
        if target == self.database_path:
            raise ValueError("Export package destination must differ from the live database")

        target.parent.mkdir(parents=True, exist_ok=True)

        temporary = target.with_name(f".{target.name}.tmp")
        with tempfile.TemporaryDirectory(prefix="spectrasoft-export-") as staging_dir:
            snapshot = Path(staging_dir) / DATABASE_MEMBER
            self.backup_service.create_backup(snapshot)
            database = self.backup_service.validate_database(snapshot)
            tables = self._table_names(snapshot)
            manifest = self._manifest(database, tables)
            try:
                with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    archive.write(snapshot, DATABASE_MEMBER)
                    archive.writestr(MANIFEST_MEMBER, json.dumps(manifest, indent=2, sort_keys=True))
                validation = self.validate_package(temporary)
                os.replace(temporary, target)
            finally:
                if temporary.exists():
                    temporary.unlink()

        return PortableExportResult(target, validation.database, validation.tables)

    def validate_package(self, package: os.PathLike[str] | str) -> PortablePackageValidation:
        """Validate package structure, checksums, SQLite integrity, and schema."""
        path = Path(package).expanduser().resolve()
        if not path.is_file():
            raise InvalidPortablePackageError(f"Portable package does not exist: {path}")
        if path.stat().st_size > MAX_PACKAGE_BYTES:
            raise InvalidPortablePackageError("Portable package exceeds the 512 MiB safety limit")

        with tempfile.TemporaryDirectory(prefix="spectrasoft-package-") as temporary_dir:
            extracted = Path(temporary_dir)
            try:
                with zipfile.ZipFile(path) as archive:
                    self._validate_members(archive)
                    manifest = self._read_manifest(archive)
                    archive.extract(DATABASE_MEMBER, extracted)
            except (OSError, zipfile.BadZipFile, KeyError, json.JSONDecodeError) as exc:
                raise InvalidPortablePackageError(f"Could not read portable package: {exc}") from exc

            database_path = extracted / DATABASE_MEMBER
            try:
                validation = self.backup_service.validate_database(database_path)
            except InvalidBackupError as exc:
                raise InvalidPortablePackageError(str(exc)) from exc

            expected_hash = manifest.get("database_sha256")
            if expected_hash != self._sha256(database_path):
                raise InvalidPortablePackageError("Portable package database checksum does not match its manifest")

            expected_tables = tuple(manifest.get("tables", []))
            actual_tables = self._table_names(database_path)
            if expected_tables != actual_tables:
                raise InvalidPortablePackageError("Portable package table inventory does not match its database")

            self._validate_manifest_database(manifest, validation)
            if self.database_path.is_file():
                try:
                    self.backup_service._validate_compatible_schema(database_path)
                except InvalidBackupError as exc:
                    raise InvalidPortablePackageError(str(exc)) from exc

            return PortablePackageValidation(
                path=path,
                format=manifest["format"],
                package_version=manifest["package_version"],
                created_at=manifest["created_at"],
                database=validation,
                tables=actual_tables,
            )

    def import_package(
        self,
        package: os.PathLike[str] | str,
        *,
        confirmed: bool = False,
        dry_run: bool = False,
        pre_import_backup: os.PathLike[str] | str | None = None,
    ) -> PortableImportResult | PortablePackageValidation:
        """Validate and optionally replace the live database from a package."""
        if not dry_run and not confirmed:
            raise BackupConfirmationRequired("Portable import requires explicit user confirmation")

        validation = self.validate_package(package)
        if dry_run:
            return validation

        package_path = Path(package).expanduser().resolve()
        with tempfile.TemporaryDirectory(prefix="spectrasoft-import-") as temporary_dir:
            extracted = Path(temporary_dir)
            with zipfile.ZipFile(package_path) as archive:
                archive.extract(DATABASE_MEMBER, extracted)

            pre_import = self._resolve_pre_import_path(pre_import_backup)
            restore = self.backup_service.restore(
                extracted / DATABASE_MEMBER,
                confirmed=True,
                pre_restore_backup=pre_import,
            )
        return PortableImportResult(package_path, restore, validation)

    def _resolve_pre_import_path(self, path: os.PathLike[str] | str | None) -> Path:
        if path is not None:
            return Path(path).expanduser().resolve()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        return self.database_path.with_name(f"{self.database_path.stem}.pre-import-{stamp}.db")

    @staticmethod
    def _validate_members(archive: zipfile.ZipFile) -> None:
        names = archive.namelist()
        if DATABASE_MEMBER not in names or MANIFEST_MEMBER not in names:
            raise InvalidPortablePackageError("Portable package must contain database.db and manifest.json")
        for name in names:
            member = Path(name)
            if member.is_absolute() or ".." in member.parts:
                raise InvalidPortablePackageError(f"Unsafe portable package member: {name}")
        if archive.getinfo(DATABASE_MEMBER).file_size > MAX_PACKAGE_BYTES:
            raise InvalidPortablePackageError("Portable package database exceeds the 512 MiB safety limit")

    @staticmethod
    def _read_manifest(archive: zipfile.ZipFile) -> dict[str, Any]:
        manifest = json.loads(archive.read(MANIFEST_MEMBER).decode("utf-8"))
        if not isinstance(manifest, dict):
            raise InvalidPortablePackageError("Portable package manifest must be an object")
        if manifest.get("format") != PACKAGE_FORMAT:
            raise InvalidPortablePackageError("Portable package format is not supported")
        if manifest.get("package_version") != PACKAGE_VERSION:
            raise InvalidPortablePackageError("Portable package version is not supported")
        required = {"created_at", "database_sha256", "sqlite_user_version", "tables"}
        missing = sorted(required - set(manifest))
        if missing:
            raise InvalidPortablePackageError(f"Portable package manifest is missing: {', '.join(missing)}")
        if not isinstance(manifest["tables"], list) or not all(isinstance(item, str) for item in manifest["tables"]):
            raise InvalidPortablePackageError("Portable package table inventory is invalid")
        return manifest

    @staticmethod
    def _validate_manifest_database(manifest: dict[str, Any], database: DatabaseValidation) -> None:
        if int(manifest["sqlite_user_version"]) != database.user_version:
            raise InvalidPortablePackageError("Portable package SQLite schema version does not match its database")
        if int(manifest.get("table_count", -1)) != database.table_count:
            raise InvalidPortablePackageError("Portable package table count does not match its database")

    @staticmethod
    def _manifest(database: DatabaseValidation, tables: tuple[str, ...]) -> dict[str, Any]:
        return {
            "format": PACKAGE_FORMAT,
            "package_version": PACKAGE_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "database_sha256": PortablePackageService._sha256(database.path),
            "sqlite_user_version": database.user_version,
            "table_count": database.table_count,
            "tables": list(tables),
        }

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _table_names(path: Path) -> tuple[str, ...]:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as connection:
            rows = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()
        return tuple(row[0] for row in rows)
