import tempfile
import unittest
from pathlib import Path

from tools_repo_readiness_check import format_text_report, run_check


class RepoReadinessCheckTests(unittest.TestCase):
    def test_run_check_reports_missing_required_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# test\n", encoding="utf-8")

            result = run_check(root)

            self.assertFalse(result.ok)
            self.assertIn("src", result.required_missing)
            self.assertIn("tests", result.required_missing)

    def test_run_check_passes_when_required_paths_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# test\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "tests").mkdir()

            result = run_check(root)

            self.assertTrue(result.ok)
            self.assertEqual([], result.required_missing)

    def test_format_text_report_contains_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# test\n", encoding="utf-8")

            result = run_check(root)
            report = format_text_report(result)

            self.assertIn("Status: FAIL", report)
            self.assertIn("Required missing", report)


if __name__ == "__main__":
    unittest.main()
