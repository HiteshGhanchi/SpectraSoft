import sqlite3
import tempfile
import unittest
from pathlib import Path

from core.persistence.backup_service import (
    BackupError,
    BackupConfirmationRequired,
    BackupService,
    InvalidBackupError,
)


class BackupServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.database = self.root / "live.db"
        with sqlite3.connect(self.database) as connection:
            connection.execute("CREATE TABLE credentials (id INTEGER PRIMARY KEY, secret TEXT)")
            connection.execute("INSERT INTO credentials (secret) VALUES ('keep-me')")
            connection.execute("CREATE TABLE results (id INTEGER PRIMARY KEY, value REAL)")
            connection.execute("INSERT INTO results (value) VALUES (1.25)")
            connection.commit()
        self.service = BackupService(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_backup_uses_sqlite_online_backup_and_preserves_all_tables(self):
        backup = self.root / "backup.db"

        result = self.service.create_backup(backup)

        self.assertTrue(result.valid)
        self.assertEqual(result.table_count, 2)
        with sqlite3.connect(backup) as connection:
            self.assertEqual(
                connection.execute("SELECT secret FROM credentials").fetchone()[0],
                "keep-me",
            )
            self.assertEqual(
                connection.execute("SELECT value FROM results").fetchone()[0],
                1.25,
            )

    def test_invalid_backup_format_is_rejected(self):
        invalid = self.root / "not-a-database.db"
        invalid.write_text("plain text")

        with self.assertRaises(InvalidBackupError):
            self.service.validate_database(invalid)

    def test_restore_dry_run_verifies_without_mutating_database(self):
        source = self.root / "source.db"
        self.service.create_backup(source)
        with sqlite3.connect(source) as connection:
            connection.execute("UPDATE credentials SET secret = 'restored'")
            connection.commit()

        result = self.service.restore(source, dry_run=True)

        self.assertTrue(result.dry_run)
        self.assertFalse(result.restored)
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT secret FROM credentials").fetchone()[0], "keep-me")

    def test_restore_requires_confirmation_and_preserves_pre_restore_backup(self):
        source = self.root / "source.db"
        self.service.create_backup(source)
        with sqlite3.connect(source) as connection:
            connection.execute("UPDATE credentials SET secret = 'restored'")
            connection.commit()

        with self.assertRaises(BackupConfirmationRequired):
            self.service.restore(source)

        disposed = []
        result = self.service.restore(source, confirmed=True, dispose_callback=lambda: disposed.append(True))

        self.assertTrue(result.restored)
        self.assertTrue(disposed)
        self.assertIsNotNone(result.pre_restore_backup)
        self.assertTrue(Path(result.pre_restore_backup).exists())
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT secret FROM credentials").fetchone()[0], "restored")
        with sqlite3.connect(result.pre_restore_backup) as connection:
            self.assertEqual(connection.execute("SELECT secret FROM credentials").fetchone()[0], "keep-me")

    def test_restore_rejects_same_source_and_running_database_path(self):
        with self.assertRaises(ValueError):
            self.service.restore(self.database, confirmed=True)

    def test_restore_rejects_unrelated_schema_even_when_sqlite_is_valid(self):
        source = self.root / "unrelated.db"
        with sqlite3.connect(source) as connection:
            connection.execute("CREATE TABLE unrelated (value TEXT)")
        with self.assertRaises(InvalidBackupError):
            self.service.restore(source, dry_run=True)

    def test_restore_requires_database_disposal_integration(self):
        source = self.root / "source.db"
        self.service.create_backup(source)
        with self.assertRaises(BackupError):
            self.service.restore(source, confirmed=True)

    def test_restore_keeps_live_inode_and_handles_wal(self):
        source = self.root / "source.db"
        self.service.create_backup(source)
        connection = sqlite3.connect(self.database)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("UPDATE results SET value = 9.0")
            connection.commit()
            inode = self.database.stat().st_ino
            result = self.service.restore(source, confirmed=True, dispose_callback=lambda: None)
            self.assertEqual(self.database.stat().st_ino, inode)
            self.assertEqual(connection.execute("SELECT value FROM results").fetchone()[0], 1.25)
            self.assertEqual(Path(result.pre_restore_backup).parent, self.root)
        finally:
            connection.close()



if __name__ == "__main__":
    unittest.main()
