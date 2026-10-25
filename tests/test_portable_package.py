import json
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import cast

from core.persistence.portable_package import (
    InvalidPortablePackageError,
    PortableImportResult,
    PortablePackageValidation,
    PortablePackageService,
)


class PortablePackageServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.database = self.root / "live.db"
        with sqlite3.connect(self.database) as connection:
            connection.execute("CREATE TABLE configuration (id INTEGER PRIMARY KEY, value TEXT)")
            connection.execute("INSERT INTO configuration (value) VALUES ('instrument')")
            connection.execute("CREATE TABLE results (id INTEGER PRIMARY KEY, value REAL)")
            connection.execute("INSERT INTO results (value) VALUES (1.25)")
            connection.commit()
        self.service = PortablePackageService(self.database, dispose_callback=lambda: None)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_contains_complete_database_and_manifest(self):
        package = self.root / "portable.zip"

        result = self.service.export_package(package)

        self.assertTrue(package.exists())
        self.assertEqual(result.tables, ("configuration", "results"))
        with zipfile.ZipFile(package) as archive:
            self.assertEqual(set(archive.namelist()), {"database.db", "manifest.json"})
            manifest = json.loads(archive.read("manifest.json"))
            self.assertEqual(manifest["format"], "spectrasoft-portable-data")
            self.assertEqual(manifest["tables"], ["configuration", "results"])
            extracted = self.root / "exported.db"
            extracted.write_bytes(archive.read("database.db"))
            with sqlite3.connect(extracted) as connection:
                self.assertEqual(connection.execute("SELECT value FROM configuration").fetchone()[0], "instrument")
                self.assertEqual(connection.execute("SELECT value FROM results").fetchone()[0], 1.25)

    def test_validate_package_does_not_change_live_database(self):
        package = self.root / "portable.zip"
        self.service.export_package(package)

        result = self.service.import_package(package, dry_run=True)

        validation = cast(PortablePackageValidation, result)
        self.assertEqual(validation.database.table_count, 2)
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT value FROM configuration").fetchone()[0], "instrument")

    def test_import_replaces_all_data_and_preserves_pre_import_backup(self):
        package = self.root / "portable.zip"
        self.service.export_package(package)
        with sqlite3.connect(self.database) as connection:
            connection.execute("UPDATE configuration SET value = 'changed'")
            connection.execute("INSERT INTO results (value) VALUES (9.0)")
            connection.commit()
        pre_import = self.root / "pre-import.db"

        result = self.service.import_package(
            package,
            confirmed=True,
            pre_import_backup=pre_import,
        )

        imported = cast(PortableImportResult, result)
        self.assertTrue(imported.restore.restored)
        self.assertTrue(pre_import.exists())
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT value FROM configuration").fetchone()[0], "instrument")
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM results").fetchone()[0], 1)
        with sqlite3.connect(pre_import) as connection:
            self.assertEqual(connection.execute("SELECT value FROM configuration").fetchone()[0], "changed")
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM results").fetchone()[0], 2)

    def test_tampered_package_is_rejected(self):
        package = self.root / "portable.zip"
        self.service.export_package(package)
        tampered = self.root / "tampered.zip"
        with zipfile.ZipFile(package) as source, zipfile.ZipFile(tampered, "w") as destination:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename == "manifest.json":
                    manifest = json.loads(payload)
                    manifest["database_sha256"] = "0" * 64
                    payload = json.dumps(manifest).encode("utf-8")
                destination.writestr(item, payload)

        with self.assertRaises(InvalidPortablePackageError):
            self.service.validate_package(tampered)


if __name__ == "__main__":
    unittest.main()
