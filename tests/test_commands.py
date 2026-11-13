"""Exercise release guard copies with fake Git. Never publish or touch real Git state."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseCommandTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "scripts").mkdir()
        (self.root / "bin").mkdir()
        self.log = self.root / "calls"
        # Execute a copy, not the repository's publication entry point.
        self.release = self.root / "release-fixture.sh"
        shutil.copyfile(ROOT / "publish.sh", self.release)
        git = self.root / "bin/git"
        git.write_text('''#!/bin/sh
printf 'git %s\\n' "$*" >> "$CALL_LOG"
case "$1" in
  branch) printf '%s\\n' "${TEST_BRANCH:-master}" ;;
  status)
    if [ -f "$CHECK_MARK" ]; then
      printf '%s' "${TEST_AFTER_DIRTY:-}"
    else
      printf '%s' "${TEST_DIRTY:-}"
    fi ;;
  push) exit "${TEST_PUSH_EXIT:-0}" ;;
  *) exit 99 ;;
esac
''', encoding="utf-8")
        git.chmod(0o755)
        (self.root / "scripts/verify_preparation.sh").write_text('''#!/bin/sh
printf 'verify\\n' >> "$CALL_LOG"
touch "$CHECK_MARK"
exit "${TEST_CHECK_EXIT:-0}"
''', encoding="utf-8")
        self.env = {**os.environ, "PATH": str(git.parent) + os.pathsep + os.environ["PATH"],
                    "CALL_LOG": str(self.log), "CHECK_MARK": str(self.root / "checked")}

    def run_release(self, **options):
        result = subprocess.run(["sh", str(self.release)], env={**self.env, **options},
                                capture_output=True, text=True)
        return result.returncode, self.log.read_text(encoding="utf-8").splitlines()

    def test_feature_branch_stops_before_checks_and_push(self):
        code, calls = self.run_release(TEST_BRANCH="feature/draft")
        self.assertNotEqual(code, 0)
        self.assertEqual(calls, ["git branch --show-current"])

    def test_dirty_checkout_stops_before_checks_and_push(self):
        code, calls = self.run_release(TEST_DIRTY=" M meditations/draft.md")
        self.assertNotEqual(code, 0)
        self.assertNotIn("verify", calls)
        self.assertNotIn("git push", calls)

    def test_failed_verification_stops_before_push(self):
        code, calls = self.run_release(TEST_CHECK_EXIT="1")
        self.assertNotEqual(code, 0)
        self.assertIn("verify", calls)
        self.assertNotIn("git push", calls)

    def test_changes_during_checks_stop_before_push(self):
        code, calls = self.run_release(TEST_AFTER_DIRTY=" M terms.json")
        self.assertNotEqual(code, 0)
        self.assertIn("verify", calls)
        self.assertNotIn("git push", calls)

    def test_only_clean_verified_master_reaches_fake_push(self):
        code, calls = self.run_release()
        self.assertEqual(code, 0)
        self.assertEqual(calls, ["git branch --show-current", "git status --porcelain", "verify",
                                 "git status --porcelain", "git push"])

    def test_fake_push_failure_is_reported(self):
        code, calls = self.run_release(TEST_PUSH_EXIT="7")
        self.assertEqual(code, 7)
        self.assertEqual(calls[-1], "git push")


if __name__ == "__main__":
    unittest.main()
