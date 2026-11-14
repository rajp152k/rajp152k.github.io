"""Exercise just recipes against isolated script stubs, including publication."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
JUST = shutil.which("just")


@unittest.skipUnless(JUST, "install just to test the command interface")
class JustfileTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="just commands ")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "scripts").mkdir()
        (self.root / "nested").mkdir()
        shutil.copyfile(ROOT / "justfile", self.root / "justfile")
        self.log = self.root / "calls"
        self.env = {**os.environ, "CALL_LOG": str(self.log)}
        for name in ("write.sh", "prepare.sh", "publish.sh",
                     "scripts/python.sh", "scripts/verify_preparation.sh"):
            script = self.root / name
            script.write_text(
                '#!/bin/sh\nprintf "%s\\0" "$0" "$@" > "$CALL_LOG"\n'
                'exit "${TEST_EXIT:-0}"\n', encoding="utf-8")
            script.chmod(0o755)

    def run_just(self, *args, **env):
        return subprocess.run([JUST, *args], cwd=self.root / "nested",
                              env={**self.env, **env}, capture_output=True, text=True)

    def calls(self):
        return self.log.read_bytes().decode().rstrip("\0").split("\0")

    def test_default_lists_commands_without_running_scripts(self):
        result = self.run_just()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.log.exists())

    def test_recipes_dispatch_from_a_subdirectory(self):
        cases = {
            "prepare": ["./prepare.sh", "build"],
            "preview": ["./prepare.sh", "preview"],
            "status": ["./prepare.sh", "status"],
            "review-check": ["./prepare.sh", "check"],
            "prune": ["./prepare.sh", "prune"],
            "check": ["scripts/verify_preparation.sh"],
            "publish": ["./publish.sh"],
            "embed": ["scripts/python.sh", "scripts/embed.py"],
            "build": ["scripts/python.sh", "scripts/publish.py"],
            "e2e": ["./prepare.sh", "preview"],
        }
        for recipe, expected in cases.items():
            with self.subTest(recipe=recipe):
                result = self.run_just(recipe)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.calls(), expected)

    def test_title_and_review_notes_pass_as_literal_arguments(self):
        text = 'Raj\'s "notes"; $(touch injected) `touch injected` $HOME * \\ end'
        for args, expected in (
            (("write", text), ["./write.sh", text]),
            (("review", "meditations/studying", "--stage", "reader", "--note", text),
             ["./prepare.sh", "review", "meditations/studying", "--stage", "reader", "--note", text]),
            (("preview", "--port", "8766"), ["./prepare.sh", "preview", "--port", "8766"]),
        ):
            with self.subTest(recipe=args[0]):
                result = self.run_just(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.calls(), expected)
                self.assertFalse((self.root / "injected").exists())

    def test_script_failure_propagates(self):
        result = self.run_just("check", TEST_EXIT="23")
        self.assertEqual(result.returncode, 23, result.stderr)
