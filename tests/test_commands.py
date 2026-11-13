"""Exercise command copies in temporary directories, without publishing or editing posts."""
from datetime import date
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class WriteCommandTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="write command ")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in ("scripts", "bin", "meditations"):
            (self.root / name).mkdir()
        shutil.copyfile(ROOT / "write.sh", self.root / "write.sh")
        shutil.copyfile(ROOT / "scripts/python.sh", self.root / "scripts/python.sh")
        self.editor_log = self.root / "editor-args"
        editor = self.root / "bin/nvim"
        editor.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$EDITOR_LOG"\n', encoding="utf-8")
        editor.chmod(0o755)
        self.env = {**os.environ, "PATH": str(editor.parent) + os.pathsep + os.environ["PATH"],
                    "PYTHON": sys.executable, "EDITOR_LOG": str(self.editor_log)}

    def run_write(self, *titles, **options):
        return subprocess.run(["bash", str(self.root / "write.sh"), *titles],
                              cwd=self.root / "bin", env={**self.env, **options},
                              capture_output=True, text=True)

    def test_quoted_title_date_and_editor_argument(self):
        title = 'Raj\'s "notes": [one] # two \\ three'
        before = date.today()
        result = self.run_write(title)
        after = date.today()
        self.assertEqual(result.returncode, 0, result.stderr)
        post = self.root / "meditations/raj-s-notes-one-two-three.md"
        source = post.read_text(encoding="utf-8")
        metadata = yaml.safe_load(source.split("---\n")[1])
        self.assertEqual(metadata["title"], title)
        self.assertIn(metadata["date"], (before, after))
        self.assertTrue(source.endswith("---\n\n"))
        self.assertEqual(self.editor_log.read_text().splitlines(), [str(post)])

    def test_existing_file_is_not_overwritten_or_opened(self):
        post = self.root / "meditations/existing.md"
        post.write_text("existing draft\n", encoding="utf-8")
        result = self.run_write("Existing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(post.read_text(), "existing draft\n")
        self.assertFalse(self.editor_log.exists())

    def test_empty_or_punctuation_title_is_refused(self):
        for titles in ((), ("",), ("!? --- /",)):
            with self.subTest(titles=titles):
                result = self.run_write(*titles)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list((self.root / "meditations").iterdir()), [])
                self.assertFalse(self.editor_log.exists())

    def test_reserved_slugs_are_refused_before_writing(self):
        for title in ("Search", "Logs!", " MEDITATIONS ", "Terms"):
            with self.subTest(title=title):
                result = self.run_write(title)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("reserved meditation name", result.stderr)
                self.assertEqual(list((self.root / "meditations").iterdir()), [])
                self.assertFalse(self.editor_log.exists())

    def test_python_override_is_used(self):
        interpreter = self.root / "bin/chosen python"
        interpreter.write_text('''#!/bin/sh
printf 'called\\n' > "$PYTHON_LOG"
exec "$REAL_PYTHON" "$@"
''', encoding="utf-8")
        interpreter.chmod(0o755)
        log = self.root / "python-call"
        result = self.run_write("Interpreter choice", PYTHON=str(interpreter),
                                REAL_PYTHON=sys.executable, PYTHON_LOG=str(log))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(log.read_text(), "called\n")
        self.assertTrue((self.root / "meditations/interpreter-choice.md").is_file())
        self.assertTrue(self.editor_log.exists())


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
