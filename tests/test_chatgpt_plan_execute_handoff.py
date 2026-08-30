from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/chatgpt-plan-execute/scripts/prepare_handoff.py"


class HandoffScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        (self.workspace / "src").mkdir()
        (self.workspace / "task.md").write_text("Plan the change.\n", encoding="utf-8")
        (self.workspace / "facts.md").write_text(
            "Repository Fact: src/service.py owns behavior.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def create(self, entries: list[str], *extra: str) -> subprocess.CompletedProcess[str]:
        selected = self.workspace / "selected.txt"
        selected.write_text("\n".join(entries) + "\n", encoding="utf-8")
        return self.run_script(
            "create",
            "--workspace",
            str(self.workspace),
            "--task-file",
            str(self.workspace / "task.md"),
            "--facts-file",
            str(self.workspace / "facts.md"),
            "--file-list",
            str(selected),
            *extra,
        )

    def handoff_dir(self, result: subprocess.CompletedProcess[str]) -> Path:
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        return Path(payload["handoff_dir"])

    def test_create_packages_only_exact_selected_files(self) -> None:
        (self.workspace / "src/service.py").write_text(
            "def run():\n    return 1\n",
            encoding="utf-8",
        )
        (self.workspace / "src/unrelated.py").write_text(
            "UNRELATED = True\n",
            encoding="utf-8",
        )

        result = self.create(["src/service.py"])

        self.assertEqual(0, result.returncode, result.stderr)
        handoff = self.handoff_dir(result)
        manifest = json.loads((handoff / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("ready", manifest["status"])
        self.assertTrue(manifest["submission_allowed"])
        self.assertEqual(
            ["src/service.py"],
            [item["path"] for item in manifest["included"]],
        )
        with zipfile.ZipFile(handoff / manifest["archive"]) as archive:
            self.assertEqual(["src/service.py"], archive.namelist())

    def test_secret_path_blocks_archive(self) -> None:
        (self.workspace / ".env.production").write_text(
            "SAFE_LOOKING=value\n",
            encoding="utf-8",
        )

        result = self.create([".env.production"])

        self.assertEqual(3, result.returncode)
        handoff = self.handoff_dir(result)
        manifest = json.loads((handoff / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("blocked", manifest["status"])
        self.assertFalse(list(handoff.glob("context-*.zip")))
        self.assertFalse((handoff / "prompt.md").exists())

    def test_sensitive_content_blocks_archive(self) -> None:
        (self.workspace / "src/config.txt").write_text(
            "api_key = supersecretvalue123\n",
            encoding="utf-8",
        )

        result = self.create(["src/config.txt"])

        self.assertEqual(3, result.returncode)
        manifest = json.loads(
            (self.handoff_dir(result) / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertIn("sensitive-content", manifest["blocked"][0]["reason"])

    def test_path_traversal_is_blocked(self) -> None:
        result = self.create(["../outside.txt"])

        self.assertEqual(3, result.returncode)
        manifest = json.loads(
            (self.handoff_dir(result) / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertIn("unsafe selected path", manifest["blocked"][0]["reason"])

    def test_task_or_facts_secret_blocks_handoff(self) -> None:
        (self.workspace / "src/service.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.workspace / "facts.md").write_text(
            "access_token = supersecretvalue123\n",
            encoding="utf-8",
        )

        result = self.create(["src/service.py"])

        self.assertEqual(3, result.returncode)
        manifest = json.loads(
            (self.handoff_dir(result) / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("blocked", manifest["status"])
        self.assertTrue(
            any(item["path"] == "repository-facts.md" for item in manifest["blocked"])
        )

    def test_dry_run_prevents_session_submission(self) -> None:
        (self.workspace / "src/service.py").write_text("VALUE = 1\n", encoding="utf-8")
        created = self.create(["src/service.py"], "--dry-run")

        self.assertEqual(0, created.returncode, created.stderr)
        handoff = self.handoff_dir(created)
        manifest = json.loads((handoff / "manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["submission_allowed"])
        recorded = self.run_script(
            "record-session",
            "--handoff-dir",
            str(handoff),
            "--chat-url",
            "https://chatgpt.com/c/abc",
            "--actual-mode",
            "Pro",
        )
        self.assertEqual(2, recorded.returncode)

    def test_record_session_requires_chatgpt_url(self) -> None:
        (self.workspace / "src/service.py").write_text("VALUE = 1\n", encoding="utf-8")
        created = self.create(["src/service.py"])
        handoff = self.handoff_dir(created)

        bad = self.run_script(
            "record-session",
            "--handoff-dir",
            str(handoff),
            "--chat-url",
            "https://example.com/c/abc",
            "--actual-mode",
            "Pro",
        )
        good = self.run_script(
            "record-session",
            "--handoff-dir",
            str(handoff),
            "--chat-url",
            "https://chatgpt.com/c/abc",
            "--actual-mode",
            "Pro",
        )

        self.assertEqual(2, bad.returncode)
        self.assertEqual(0, good.returncode, good.stderr)
        session = json.loads((handoff / "session.json").read_text(encoding="utf-8"))
        self.assertEqual("https://chatgpt.com/c/abc", session["chat_url"])
        self.assertEqual("submitted", session["status"])

    def test_import_response_requires_exact_marker_pair(self) -> None:
        (self.workspace / "src/service.py").write_text("VALUE = 1\n", encoding="utf-8")
        created = self.create(["src/service.py"])
        handoff = self.handoff_dir(created)
        raw = self.workspace / "raw.md"
        raw.write_text(
            "BEGIN_CHATGPT_PLAN_RESPONSE\n# Plan\nDo the work.\nEND_CHATGPT_PLAN_RESPONSE\n",
            encoding="utf-8",
        )

        imported = self.run_script(
            "import-response",
            "--handoff-dir",
            str(handoff),
            "--response-file",
            str(raw),
            "--kind",
            "plan",
        )
        self.assertEqual(0, imported.returncode, imported.stderr)
        self.assertEqual(
            "# Plan\nDo the work.\n",
            (handoff / "response.md").read_text(encoding="utf-8"),
        )

        raw.write_text(
            "BEGIN_CHATGPT_PLAN_RESPONSE\nA\nBEGIN_CHATGPT_PLAN_RESPONSE\nB\nEND_CHATGPT_PLAN_RESPONSE\n",
            encoding="utf-8",
        )
        duplicated = self.run_script(
            "import-response",
            "--handoff-dir",
            str(handoff),
            "--response-file",
            str(raw),
        )
        self.assertEqual(2, duplicated.returncode)


if __name__ == "__main__":
    unittest.main()
