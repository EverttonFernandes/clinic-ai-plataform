"""Tracking gates must reject incomplete prerequisites, not trust a DONE label."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "feature_tracking.py"


class TrackingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tokens = {}
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "stories").mkdir()
        for key in ("A", "B"):
            (self.root / "stories" / (key + ".md")).write_text("Acceptance criteria\n")
        (self.root / "board.md").write_text(
            "## To Do\n| 1 | [A](stories/A.md) | Technical | Foundation | Base |\n"
            "## Done\n| 2 | [B](stories/B.md) | Business | Feature | Depends on A |\n")

    def cli(self, *args, owned=True):
        if owned and args[0] in ("failure", "review", "finish", "dependencies") and args[1] in self.tokens:
            args = (*args, "--lock-token", self.tokens[args[1]])
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", "tracking", *args],
                              cwd=self.root, capture_output=True, text=True,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if result.returncode == 0 and args[0] == "start":
            self.tokens[args[1]] = json.loads(result.stdout)["token"]
        return result

    def seed(self):
        result = self.cli("import-kanban", "board.md")
        self.assertEqual(result.returncode, 0, result.stderr)

    def record(self, key):
        return json.loads((self.root / "tracking" / (key + ".json")).read_text())

    def test_import_preserves_unknown_history_and_does_not_trust_done(self):
        self.seed()
        self.assertIsNone(self.record("B")["started_at"])
        self.assertEqual(self.record("B")["status"], "UNVERIFIED")
        self.assertNotEqual(self.cli("start", "A").returncode, 0)
        self.assertEqual(self.cli("dependencies", "A", "--reason", "Foundation without prerequisites").returncode, 0)
        self.assertEqual(self.cli("start", "A").returncode, 0)

    def test_missing_and_circular_dependencies_rejected_without_writing(self):
        self.seed()
        self.assertNotEqual(self.cli("dependencies", "A", "MISSING", "--reason", "Required").returncode, 0)
        self.assertEqual(self.cli("dependencies", "A", "B", "--reason", "Required").returncode, 0)
        before = self.record("B")
        self.assertNotEqual(self.cli("dependencies", "B", "A", "--reason", "Required").returncode, 0)
        self.assertEqual(self.record("B"), before)
        self.assertNotEqual(self.cli("start", "A").returncode, 0)

    def test_events_survive_reimport_and_failure_count_is_derived(self):
        self.seed()
        self.cli("dependencies", "A", "--reason", "No prerequisites")
        self.cli("start", "A")
        self.assertEqual(self.cli("failure", "A", "--reason", "Emulator OOM").returncode, 0)
        before = self.record("A")
        self.seed()
        self.assertEqual(self.record("A"), before)
        index = json.loads((self.root / "tracking/index.json").read_text())
        self.assertEqual(index["features"][0]["failure_count"], 1)
        self.assertEqual(before["status"], "BLOCKED")
        self.assertIsNotNone(before["started_at"])
        self.assertIsNone(before["completed_at"])

    def test_finish_without_plan_evidence_does_not_mark_done(self):
        self.seed()
        self.cli("dependencies", "A", "--reason", "No prerequisites")
        self.cli("start", "A")
        self.assertNotEqual(self.cli("finish", "A").returncode, 0)
        self.assertEqual(self.record("A")["status"], "IN_PROGRESS")

    def test_unsafe_key_rejected(self):
        self.seed()
        self.assertNotEqual(self.cli("start", "../outside").returncode, 0)

    def test_changed_story_requires_new_dependency_review(self):
        self.seed()
        self.cli("dependencies", "A", "--reason", "No prerequisites")
        (self.root / "stories/A.md").write_text("New technical prerequisite\n")
        self.assertNotEqual(self.cli("start", "A").returncode, 0)

    def test_start_acquires_lock_and_foreign_execution_cannot_change_task(self):
        self.seed()
        self.cli("dependencies", "A", "--reason", "No prerequisites")
        self.assertEqual(self.cli("start", "A").returncode, 0)
        self.assertNotEqual(self.cli("start", "A").returncode, 0)
        before = self.record("A")
        self.assertNotEqual(self.cli("failure", "A", "--reason", "Foreign", owned=False).returncode, 0)
        self.assertEqual(self.record("A"), before)
        self.assertEqual(self.cli("failure", "A", "--reason", "Owner reports failure").returncode, 0)

    def test_failed_dependency_check_does_not_acquire_task(self):
        self.seed()
        self.assertNotEqual(self.cli("start", "A").returncode, 0)
        self.assertFalse((self.root / ".git/harness/orchestration/A.lock").exists())

    def test_existing_writer_lock_blocks_mutation(self):
        self.seed()
        (self.root / "tracking/.writer-lock").mkdir()
        before = self.record("A")
        self.assertNotEqual(self.cli("failure", "A", "--reason", "Failure").returncode, 0)
        self.assertEqual(self.record("A"), before)

    def test_real_completion_releases_dependency_until_evidence_changes(self):
        from scripts.tests import test_harness_completion as fixtures
        fixture = fixtures.CompletionTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        (self.root / "dependent.md").write_text("Dependent criteria\n")
        (self.root / "board.md").write_text(
            "## To Do\n| 1 | [AUDIT-1](source.md) | Technical | Base | None |\n"
            "| 2 | [B](dependent.md) | Business | Feature | Requires AUDIT-1 |\n")
        self.seed()
        # Use the fixture's real plan, commands, evidence and independent-review contract.
        path = self.root / "tracking/AUDIT-1.json"
        record = json.loads(path.read_text())
        record["plan_path"] = "IMPLEMENTATION.md"
        path.write_text(json.dumps(record))
        self.cli("dependencies", "AUDIT-1", "--reason", "Foundation")
        self.cli("dependencies", "B", "AUDIT-1", "--reason", "Technical prerequisite")
        self.assertEqual(self.cli("start", "AUDIT-1").returncode, 0)
        fixture.approve()
        result = self.cli("finish", "AUDIT-1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / ".git/harness/orchestration/AUDIT-1.lock").exists())
        self.assertEqual(self.cli("ready", "B").returncode, 0)
        (self.root / "code.txt").write_text("Unverified change\n")
        self.assertNotEqual(self.cli("start", "B").returncode, 0)


if __name__ == "__main__":
    unittest.main()
