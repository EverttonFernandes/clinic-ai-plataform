"""Behavioral adaptation tests; every Git mutation stays in a temporary repository."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest

import test_harness_completion as fixtures


REPOSITORY = Path(__file__).resolve().parents[2]
TRACKING = REPOSITORY / "scripts/feature_tracking.py"
LOCK = REPOSITORY / "scripts/orchestration_lock.py"


class ClinicaHarnessTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CompletionTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root

    def tracking(self, *arguments):
        return subprocess.run([sys.executable, str(TRACKING), "--root", "tracking", *arguments],
                              cwd=self.root, capture_output=True, text=True)

    def make_board(self):
        (self.root / "foundation.md").write_text("- [ ] Foundation\n")
        (self.root / "dependent.md").write_text("- [ ] Feature\n")
        (self.root / "board.md").write_text(
            "## Linha principal\n"
            "| 01 | M1 | [CT-001 — Foundation](foundation.md) | Técnica | — | To Do |\n"
            "| 02 | M2 | [C-001 — Feature](dependent.md) | Negócio | CT-001 | To Do |\n")
        result = self.tracking("import-kanban", "board.md")
        self.assertEqual(result.returncode, 0, result.stderr)

    def criteria_source(self, text):
        (self.root / "source.md").write_text(text)
        self.fixture.state["requirement_source"]["sha256"] = self.fixture.sha("source.md")
        self.fixture.state["requirements"]["AC1"]["description"] = "Validate command"
        self.fixture.save()

    def test_current_board_imports_all_stories_and_declared_dependencies(self):
        shutil.copytree(REPOSITORY / "docs/jira-pessoal", self.root / "docs/jira-pessoal")
        result = self.tracking("import-kanban", "docs/jira-pessoal/KANBAN-OFICIAL.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        records = [json.loads(path.read_text()) for path in (self.root / "tracking").glob("*.json")
                   if path.name != "index.json"]
        board = (self.root / "docs/jira-pessoal/KANBAN-OFICIAL.md").read_text()
        expected = set(re.findall(r"\[(C[T]?-\d+) — ", board))
        self.assertEqual({record["id"] for record in records}, expected)
        dependent = next(record for record in records if record["id"] == "CT-002")
        self.assertEqual([item["id"] for item in dependent["dependencies"]], ["CT-001"])
        self.assertTrue(all(record["status"] in ("TODO", "UNVERIFIED") for record in records))
        self.assertTrue(all(record["started_at"] is None and record["completed_at"] is None
                            for record in records))

    def test_declared_dependency_cannot_be_omitted_by_manual_review(self):
        self.make_board()
        result = self.tracking("dependencies", "C-001", "--reason", "Attempt to omit foundation")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CT-001", result.stderr)

    def test_board_dependency_change_invalidates_previous_review(self):
        self.make_board()
        self.assertEqual(self.tracking("dependencies", "CT-001", "--reason", "Foundation").returncode, 0)
        board = self.root / "board.md"
        board.write_text(board.read_text().replace("Técnica | — |", "Técnica | C-001 |"))
        self.assertNotEqual(self.tracking("start", "CT-001").returncode, 0)

    def test_omitted_original_criterion_blocks_even_with_fresh_command_and_review(self):
        self.criteria_source("- [ ] Validate command\n- [ ] Verify patient authorization\n")
        self.fixture.approve()
        self.assertNotEqual(self.fixture.check()[0].returncode, 0)

    def test_omitted_bdd_scenario_blocks_completion(self):
        self.criteria_source("- [ ] Validate command\n\n```gherkin\n"
                             "  Cenário: Isolamento\n    Dado que existem dois tenants\n"
                             "    Quando A solicita dados de B\n    Então o acesso é negado\n```\n")
        self.fixture.approve()
        self.assertNotEqual(self.fixture.check()[0].returncode, 0)

    def test_fabricated_description_cannot_replace_source_criterion(self):
        self.criteria_source("- [ ] Validate command\n")
        self.fixture.state["requirements"]["AC1"]["description"] = "Weakened requirement"
        self.fixture.save()
        self.fixture.approve()
        self.assertNotEqual(self.fixture.check()[0].returncode, 0)

    def test_complete_original_criteria_and_bdd_with_real_evidence_can_finish(self):
        self.criteria_source("- [ ] Validate command\n\n```gherkin\n"
                             "  Cenário: Isolamento\n    Dado que existem dois tenants\n"
                             "    Quando A solicita dados de B\n    Então o acesso é negado\n```\n")
        self.fixture.state["requirements"]["BDD1"] = {
            "description": "Cenário: Isolamento Dado que existem dois tenants "
                           "Quando A solicita dados de B Então o acesso é negado",
            "status": "PASS", "evidence": ["regression"]}
        self.fixture.save()
        self.fixture.approve()
        result, report = self.fixture.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["completion_allowed"])

    def test_finish_requires_active_ownership_even_with_valid_evidence(self):
        (self.root / "board.md").write_text(
            "## To Do\n| 1 | [AUDIT-1](source.md) | Technical | Harness | None |\n")
        self.tracking("import-kanban", "board.md")
        path = self.root / "tracking/AUDIT-1.json"
        record = json.loads(path.read_text())
        record["plan_path"] = "IMPLEMENTATION.md"
        path.write_text(json.dumps(record))
        self.tracking("dependencies", "AUDIT-1", "--reason", "No prerequisites")
        self.fixture.approve()
        self.assertNotEqual(self.tracking("finish", "AUDIT-1").returncode, 0)

    def test_lock_recovery_refuses_changed_heartbeat(self):
        def lock(*arguments):
            return subprocess.run([sys.executable, str(LOCK), *arguments], cwd=self.root,
                                  capture_output=True, text=True)
        acquired = lock("acquire", "AUDIT-1", "--owner", "test-execution")
        self.assertEqual(acquired.returncode, 0, acquired.stderr)
        token = json.loads(acquired.stdout)["token"]
        refused = lock("recover", "AUDIT-1", "--token", token, "--expected-heartbeat", "stale",
                       "--reason", "Fixture", "--confirm-inactive")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIsNotNone(json.loads(lock("status", "AUDIT-1").stdout))


if __name__ == "__main__":
    unittest.main()
