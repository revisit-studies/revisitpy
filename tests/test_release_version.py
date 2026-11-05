from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.set_release_version import select_version, update_project_version


class TestReleaseVersion(unittest.TestCase):
    def test_patch_bump(self):
        self.assertEqual(select_version("2.7.0", "patch"), "2.7.1")

    def test_explicit_major_release(self):
        self.assertEqual(select_version("2.7.1", "minor", "3.0.0"), "3.0.0")

    def test_minor_default(self):
        for blank in ("", " \t"):
            self.assertEqual(select_version("2.7.1", "minor", blank), "2.8.0")

    def test_equal_explicit_version_allows_publication_retry(self):
        self.assertEqual(select_version("3.0.0", "minor", "3.0.0"), "3.0.0")

    def test_invalid_versions(self):
        for invalid in ("3.0", "v3.0.0", "03.0.0", "3.00.0", "3.0.00",
                        "3.0.0rc1", "3.0.0+local", "-1.0.0", "3.0.0\n", " 3.0.0"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    select_version("2.7.1", "minor", invalid)
                with self.assertRaises(ValueError):
                    select_version(invalid, "minor")

    def test_invalid_current_and_bump(self):
        for current in (None, 3, ""):
            with self.assertRaises(ValueError):
                select_version(current, "minor")
        with self.assertRaises(ValueError):
            select_version("2.7.1", "major")

    def test_downgrades_compare_numerically(self):
        with self.assertRaises(ValueError):
            select_version("2.10.0", "minor", "2.9.9")
        self.assertEqual(select_version("2.9.9", "minor", "2.10.0"), "2.10.0")

    def test_file_preservation(self):
        original = (b'# Keep this comment\r\n[tool.example]\r\nversion = "9.9.9"\r\n'
                    b"[project] # package\r\nname = 'example'\r\n"
                    b"version  =  '2.7.1' # retain comment\r\n"
                    b'[tool.other]\r\nversion = "8.8.8"\r\n')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pyproject.toml"
            path.write_bytes(original)
            self.assertEqual(update_project_version(path, "minor", "3.0.0"), "3.0.0")
            self.assertEqual(path.read_bytes(), original.replace(b"'2.7.1'", b"'3.0.0'"))

    def test_invalid_input_does_not_mutate_file(self):
        for source, requested in (
            ('[project]\nversion = "2.7.1"\n', "3.0"),
            ('[project]\nversion = "2.7.1"\n', "2.7.0"),
            ('[project]\nversion = "02.7.1"\n', "3.0.0"),
            ('[project]\nname = "example"\n', "3.0.0"),
            ('[project]\nversion = "2.7.1"\nbroken = [\n', "3.0.0"),
        ):
            with self.subTest(source=source, requested=requested), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "pyproject.toml"
                original = source.encode("utf-8")
                path.write_bytes(original)
                with self.assertRaises(ValueError):
                    update_project_version(path, "minor", requested)
                self.assertEqual(path.read_bytes(), original)

    def test_cli_outputs_selected_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pyproject.toml"
            path.write_text('[project]\nversion = "2.7.1"\n')
            script = Path(__file__).resolve().parents[1] / "scripts" / "set_release_version.py"
            result = subprocess.run(
                [sys.executable, str(script), "--project", str(path),
                 "--bump", "minor", "--version", "3.0.0"],
                capture_output=True, text=True, check=True,
            )
            self.assertEqual(result.stdout, "3.0.0\n")


if __name__ == "__main__":
    unittest.main()
