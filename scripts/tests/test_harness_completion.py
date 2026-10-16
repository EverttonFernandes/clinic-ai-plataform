"""GIVEN observable task states WHEN evaluated THEN reject unsupported completion."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "harness_completion.py"


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "source.md").write_text("AC1: validate the actual command result\n")
        (self.root / "code.txt").write_text("implementation\n")
        (self.root / "review.md").write_text("Independent inspection: AC1 has command evidence.\n")
        self.state = {
            "task_key": "AUDIT-1", "phase": "AUDIT", "objective": "Prevent false DONE",
            "scope": ["code.txt"],
            "requirement_source": {"path": "source.md", "sha256": self.sha("source.md")},
            "requirements": {"AC1": {"status": "PASS", "evidence": ["regression"]}},
            "exit_bar": {"regression": "PASS"},
            "verification": {"regression": {"command": [sys.executable, "-c", "print('verified')"]}},
            "evaluation": {"status": "PENDING"}, "correction_queue": [],
            "handoff": {"next_action": "Review evidence", "blockers": []},
        }
        self.save()

    def sha(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def save(self, body="\n# Plan\n- [x] AC1 verified\n"):
        (self.root / "IMPLEMENTATION.md").write_text("---\n" + json.dumps(self.state, indent=2) + "\n---\n" + body)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.root, text=True, capture_output=True,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))

    def check(self):
        result = self.cli("check", "IMPLEMENTATION.md")
        return result, json.loads(result.stdout)

    def verify(self):
        result = self.cli("verify", "IMPLEMENTATION.md", "regression", "--timeout", "2")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return json.loads(result.stdout)

    def approve(self):
        evidence = self.verify()
        self.state["evaluation"] = {
            "status": "PASS", "mode": "independent", "reviewer_id": "reviewer-thread",
            "worker_id": "worker-thread", "scope_sha256": evidence["scope_sha256"],
            "contract_sha256": evidence["contract_sha256"],
            "source_sha256": self.sha("source.md"), "path": "review.md", "sha256": self.sha("review.md"),
        }
        self.save()

    def test_given_pass_claim_without_execution_then_not_done(self):
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_log_outside_verification_directory_is_rejected_even_with_matching_hash(self):
        self.approve()
        receipt = self.root / ".git/harness/AUDIT-1/regression/latest.json"
        report = json.loads(receipt.read_text())
        report["log"] = str(self.root / "code.txt")
        report["log_sha256"] = self.sha("code.txt")
        receipt.write_text(json.dumps(report))
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_linked_worktree_can_verify_and_check_its_own_evidence(self):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "commit", "-qm", "fixture"], cwd=self.root, check=True)
        with tempfile.TemporaryDirectory() as directory:
            linked = Path(directory) / "linked"
            subprocess.run(["git", "worktree", "add", "--detach", str(linked)],
                           cwd=self.root, check=True, capture_output=True)
            self.root = linked
            self.approve()
            result, report = self.check()
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertTrue(report["completion_allowed"])

    def test_given_real_verification_and_independent_review_then_done(self):
        self.approve()
        result, report = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["completion_allowed"])
        self.assertEqual(report["status"], "DONE")

    def test_given_failed_command_then_exit_nonzero_and_persist_failure(self):
        self.state["verification"]["regression"]["command"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.save()
        result = self.cli("verify", "IMPLEMENTATION.md", "regression")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["exit_code"], 7)
        self.assertEqual(self.check()[1]["status"], "FAILED")

    def test_given_pending_failed_unknown_or_na_criterion_then_block(self):
        self.approve()
        for status in ("PENDING", "FAIL", "UNKNOWN", "N/A", "READY"):
            with self.subTest(status=status):
                self.state["requirements"]["AC1"]["status"] = status
                self.save()
                self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_unknown_or_missing_evidence_reference_then_block(self):
        self.approve()
        for evidence in ([], ["invented-check"]):
            self.state["requirements"]["AC1"]["evidence"] = evidence
            self.save()
            self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_unchecked_body_or_open_correction_then_block(self):
        self.approve()
        self.save("\n- [ ] Still pending\n")
        self.assertNotEqual(self.check()[0].returncode, 0)
        self.state["correction_queue"] = [{"id": "C1", "status": "OPEN"}]
        self.save()
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_changed_code_source_command_or_log_then_evidence_stale(self):
        for change in ("code", "source", "command", "log"):
            with self.subTest(change=change):
                self.setUp()
                self.approve()
                if change == "command":
                    self.state["verification"]["regression"]["command"] = ["false"]
                    self.save()
                elif change == "log":
                    log = next((self.root / ".git/harness/AUDIT-1/regression").glob("*.log"))
                    log.write_text("altered log")
                else:
                    (self.root / ("code.txt" if change == "code" else "source.md")).write_text("changed")
                self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_same_worker_as_reviewer_then_reject_independence(self):
        self.approve()
        self.state["evaluation"]["reviewer_id"] = "worker-thread"
        self.save()
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_criterion_removed_after_review_then_reject(self):
        self.state["requirements"]["AC2"] = {"status": "PASS", "evidence": ["regression"]}
        self.save()
        self.approve()
        del self.state["requirements"]["AC2"]
        self.save()
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_fallback_without_reason_then_reject(self):
        self.approve()
        self.state["evaluation"]["mode"] = "separate-review-fallback"
        self.save()
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_timeout_or_missing_executable_then_never_pass(self):
        for command in (["missing-harness-executable"], [sys.executable, "-c", "import time; time.sleep(10)"]):
            self.state["verification"]["regression"]["command"] = command
            self.save()
            result = self.cli("verify", "IMPLEMENTATION.md", "regression", "--timeout", "0.05")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_task_mutated_during_test_then_reject_snapshot(self):
        self.state["verification"]["regression"]["command"] = [sys.executable, "-c",
            "from pathlib import Path; Path('code.txt').write_text('mutated')"]
        self.save()
        self.assertNotEqual(self.cli("verify", "IMPLEMENTATION.md", "regression").returncode, 0)

    def test_given_legacy_yaml_or_malformed_state_then_unverified_not_crash(self):
        for text in ("---\nphase: DONE\n---\n- [ ] Pending\n", "---\n[]\n---\n"):
            (self.root / "IMPLEMENTATION.md").write_text(text)
            result, report = self.check()
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(report["status"], "UNVERIFIED")

    def test_given_na_verification_then_cannot_hide_required_test(self):
        self.approve()
        self.state["exit_bar"]["regression"] = "N/A"
        self.state["not_applicable"] = {"regression": "No local device"}
        self.save()
        self.assertNotEqual(self.check()[0].returncode, 0)

    def test_given_mandatory_review_marked_na_then_cannot_close(self):
        for gate in ("security", "arch_review", "final_review"):
            with self.subTest(gate=gate):
                self.state["exit_bar"][gate] = "N/A"
                self.state["not_applicable"] = {gate: "No sensitive change"}
                self.save()
                self.approve()
                self.assertNotEqual(self.check()[0].returncode, 0)
                del self.state["exit_bar"][gate]

    def test_given_optional_gate_na_with_reason_then_review_can_close(self):
        self.state["exit_bar"]["sonar"] = "N/A"
        self.state["not_applicable"] = {"sonar": "No Sonar configuration for this task"}
        self.save()
        self.approve()
        self.assertEqual(self.check()[0].returncode, 0)

    def test_given_handoff_then_show_actual_pending_work_without_logs(self):
        result = self.cli("handoff", "IMPLEMENTATION.md")
        report = json.loads(result.stdout)
        self.assertEqual(report["next_action"], "Review evidence")
        self.assertFalse(report["completion_allowed"])


if __name__ == "__main__":
    unittest.main()
