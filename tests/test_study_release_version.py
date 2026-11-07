from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.set_release_version import select_study_version


class TestStudyReleaseVersion(unittest.TestCase):
    def test_new_study_series(self):
        self.assertEqual(select_study_version("1.19.0", "v3.0.0"), "3.0.0")
        self.assertEqual(select_study_version("3.0.9", "v3.1.0"), "3.1.0")

    def test_independent_patches(self):
        self.assertEqual(select_study_version("3.0.4", "v3.0.1"), "3.0.5")
        self.assertEqual(select_study_version("3.0.0", "v3.0.1"), "3.0.1")

    def test_explicit_patch_and_retry(self):
        self.assertEqual(select_study_version("3.0.4", "v3.0.1", "3.0.8"), "3.0.8")
        self.assertEqual(select_study_version("3.0.4", "v3.0.1", "3.0.4"), "3.0.4")

    def test_reject_invalid_or_older_series(self):
        for tag in ("", "main", "3.0.0", "v03.0.0", "v3.0.0rc1", "v3.0.0\n", "v2.9.0"):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                select_study_version("3.0.4", tag)

    def test_reject_mismatched_or_older_exact_version(self):
        for version in ("3.1.0", "4.0.0", "2.9.0", "3.0.3", "v3.0.5"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                select_study_version("3.0.4", "v3.0.0", version)

    def test_cli_updates_project_and_rejects_mismatched_version(self):
        script = Path(__file__).resolve().parents[1] / "scripts/set_release_version.py"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "pyproject.toml"
            source = '[project]\nname = "example"\nversion = "1.19.0"\n'
            project.write_text(source)
            command = [sys.executable, str(script)] + ['--bump', 'patch']
            result = subprocess.run(command + ["--study-tag", "v3.0.0"],
                                    cwd=directory, capture_output=True, text=True, check=True)
            self.assertEqual(result.stdout, "3.0.0\n")
            expected = source.replace("1.19.0", "3.0.0")
            self.assertEqual(project.read_text(), expected)
            result = subprocess.run(command + ["--study-tag", "v3.0.0", "--version", "3.1.0"],
                                    cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(project.read_text(), expected)


if __name__ == "__main__":
    unittest.main()
