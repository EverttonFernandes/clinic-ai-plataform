"""Story lifecycle contracts against a local Git repo and a controlled gh boundary.

These responses are test doubles, never evidence of an actual GitHub run or review.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

import test_harness_completion as fixtures


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import pr_evidence
import review_policy


class GitHubValidationTests(unittest.TestCase):
    def run_payload(self, **changes):
        return {"id": 12, "name": "Application CI", "head_sha": "a" * 40,
                "status": "completed", "conclusion": "success", "html_url": "https://example.invalid/run",
                "workflow_id": 1, "event": "push", "head_branch": "main",
                "path": ".github/workflows/application.yml", **changes}

    def test_missing_other_sha_failed_pending_and_skipped_ci_are_rejected(self):
        for runs in ([], [self.run_payload(head_sha="b" * 40)],
                     [self.run_payload(conclusion="failure")], [self.run_payload(status="in_progress")],
                     [self.run_payload(conclusion="skipped")]):
            with self.subTest(runs=runs), self.assertRaises(ValueError):
                pr_evidence.validate_runs({"workflow_runs": runs}, "a" * 40,
                                         {"Application CI": ".github/workflows/application.yml"})

    def test_latest_failed_rerun_overrides_previous_green(self):
        runs = [self.run_payload(run_attempt=1), self.run_payload(run_attempt=2, conclusion="failure")]
        with self.assertRaises(ValueError):
            pr_evidence.validate_runs({"workflow_runs": runs}, "a" * 40,
                                     {"Application CI": ".github/workflows/application.yml"})

    def test_manual_event_wrong_workflow_path_or_unknown_identity_do_not_prove_push_ci(self):
        for change in ({"event": "workflow_dispatch"}, {"path": ".github/workflows/empty.yml"}, {"workflow_id": None},
                       {"path": ".github/workflows/application.yml@"},
                       {"path": ".github/workflows/application.yml@other-branch"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                pr_evidence.validate_runs({"workflow_runs": [self.run_payload(**change)]}, "a" * 40,
                                         {"Application CI": ".github/workflows/application.yml"})

    def test_pr_run_must_belong_to_the_correct_pr_and_head(self):
        for association in ([], [{"number": 2, "head": {"sha": "a" * 40}}],
                            [{"number": 1, "head": {"sha": "b" * 40}}]):
            with self.subTest(association=association), self.assertRaises(ValueError):
                pr_evidence.validate_runs({"workflow_runs": [self.run_payload(event="pull_request", pull_requests=association)]},
                                         "a" * 40, {"Application CI": ".github/workflows/application.yml"}, "pull_request", 1)

    def test_rest_workflow_path_with_reference_suffix_is_supported(self):
        for suffix in ("main", "refs/heads/story/CT-001-ambiente-docker"):
            with self.subTest(suffix=suffix):
                runs = [self.run_payload(path=".github/workflows/application.yml@" + suffix,
                                         head_branch=suffix.removeprefix("refs/heads/"))]
                result = pr_evidence.validate_runs({"workflow_runs": runs}, "a" * 40,
                                                  {"Application CI": ".github/workflows/application.yml"})
                self.assertEqual(result[0]["path"], runs[0]["path"])

    def test_synthetic_merge_run_still_requires_correct_pr_head_association(self):
        run = self.run_payload(event="pull_request", head_sha="c" * 40,
                               path=".github/workflows/application.yml@refs/pull/1/merge",
                               pull_requests=[{"number": 1, "head": {"sha": "a" * 40}}])
        result = pr_evidence.validate_runs({"workflow_runs": [run]}, "a" * 40,
                                          {"Application CI": ".github/workflows/application.yml"}, "pull_request", 1)
        self.assertEqual(result[0]["head_sha"], "a" * 40)
        self.assertEqual(result[0]["run_sha"], "c" * 40)

    def test_story_branch_requires_its_own_identifier(self):
        review_policy.validate_branch("CT-001", "story/CT-001-ambiente-docker")
        for branch in ("main", "story/CT-002-other", "", "story/CT-001"):
            with self.subTest(branch=branch), self.assertRaises(ValueError):
                review_policy.validate_branch("CT-001", branch or "detached")


class StoryLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CompletionTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.state = self.fixture.root, self.fixture.state
        self.state["task_key"] = "CT-001"
        for gate, mode in (("ci", "ci"), ("pr_ci", "pr"), ("human_review", "merged")):
            self.state["exit_bar"][gate] = "PENDING"
            self.state["verification"][gate] = {
                "command": [sys.executable, str(SCRIPTS / "pr_evidence.py"), "IMPLEMENTATION.md", mode]}
        self.fixture.save()
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
        self.git("checkout", "-qb", "story/CT-001-ambiente-docker")
        self.git("remote", "add", "origin", "https://github.com/fixture/clinica.git")
        self.head = self.git("rev-parse", "HEAD")
        fake_bin = self.root / ".git/fixture-bin"
        fake_bin.mkdir()
        fake_gh = fake_bin / "gh"
        fake_gh.write_text("#!" + sys.executable + "\n"
                           "import json, os, sys\n"
                           "from pathlib import Path\n"
                           "endpoint=sys.argv[-1].split('?')[0]\n"
                           "payload=json.loads(Path(os.environ['GH_FIXTURE']).read_text())\n"
                           "print(json.dumps(payload[endpoint]))\n")
        fake_gh.chmod(0o700)
        self.previous_env = dict(os.environ)
        self.addCleanup(self.restore_env)
        os.environ["PATH"] = str(fake_bin) + os.pathsep + os.environ["PATH"]
        os.environ["GH_FIXTURE"] = str(self.root / ".git/github-fixture.json")
        repo = {"full_name": "fixture/clinica"}
        self.pr = {"number": 1, "html_url": "https://example.invalid/pr/1", "head": {
            "sha": self.head, "ref": "story/CT-001-ambiente-docker", "repo": repo},
            "base": {"ref": "main", "repo": repo}, "merged": False, "merged_at": None,
            "merged_by": None, "merge_commit_sha": None}
        self.payload = {"repos/fixture/clinica/actions/runs": {"total_count": 2, "workflow_runs": [
            {"id": i, "name": name, "head_sha": self.head, "status": "completed", "conclusion": "success",
             "event": "push", "workflow_id": i, "path": path + "@refs/heads/story/CT-001-ambiente-docker",
             "head_branch": "story/CT-001-ambiente-docker",
             "html_url": "https://example.invalid/run/" + str(i)}
            for i, (name, path) in enumerate(review_policy.policy()["required_workflows"].items(), 1)]},
            "repos/fixture/clinica/pulls": [self.pr], "repos/fixture/clinica/pulls/1": self.pr}
        self.save_github()
        self.fixture.approve()
        self.state["evaluation"].update(worker_model="gpt-6-astra", worker_reasoning_effort="medium",
                                        reviewer_model="gpt-6-sol")
        self.fixture.save()

    def restore_env(self):
        os.environ.clear()
        os.environ.update(self.previous_env)

    def git(self, *arguments):
        return subprocess.check_output(["git", *arguments], cwd=self.root, text=True, stderr=subprocess.DEVNULL).strip()

    def save_github(self):
        Path(os.environ["GH_FIXTURE"]).write_text(json.dumps(self.payload))

    def gate(self, name):
        result = self.fixture.cli("verify", "IMPLEMENTATION.md", name, "--timeout", "5")
        if result.returncode == 0:
            self.state["exit_bar"][name] = "PASS"
            self.fixture.save()
        return result

    def stage(self, name):
        result = self.fixture.cli("check", "IMPLEMENTATION.md", "--stage", name)
        return result, json.loads(result.stdout)

    def pr_runs(self):
        runs = self.payload["repos/fixture/clinica/actions/runs"]["workflow_runs"]
        runs.extend(dict(run, id=run["id"] + 2, event="pull_request",
                         pull_requests=[{"number": 1, "head": {"sha": self.head}}]) for run in list(runs))
        self.save_github()
        result = self.gate("pr_ci")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_local_ready_and_green_ci_do_not_authorize_done_without_user_merge(self):
        local, report = self.stage("local")
        self.assertEqual(local.returncode, 0, local.stdout)
        self.assertFalse(report["completion_allowed"])
        self.assertNotEqual(self.stage("pre-pr")[0].returncode, 0)
        self.assertEqual(self.gate("ci").returncode, 0)
        ready, report = self.stage("pre-pr")
        self.assertEqual(ready.returncode, 0, ready.stdout)
        self.assertEqual(report["status"], "READY_FOR_PR")
        self.assertFalse(report["completion_allowed"])
        self.assertNotEqual(self.fixture.check()[0].returncode, 0)
        self.assertNotEqual(self.gate("human_review").returncode, 0)

    def test_exact_revision_merged_by_user_allows_done_but_other_actor_does_not(self):
        self.assertEqual(self.gate("ci").returncode, 0)
        self.pr_runs()
        self.pr.update(merged=True, merged_at="2026-10-16T12:00:00Z", merge_commit_sha="b" * 40,
                       merged_by={"login": "automation-bot"})
        self.save_github()
        self.assertNotEqual(self.gate("human_review").returncode, 0)
        self.pr["merged_by"] = {"login": "EverttonFernandes"}
        self.save_github()
        result = self.gate("human_review")
        self.assertEqual(result.returncode, 0, result.stdout)
        result, report = self.fixture.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["completion_allowed"])

    def test_new_commit_requires_new_ci_even_if_only_unscoped_notes_changed(self):
        self.assertEqual(self.gate("ci").returncode, 0)
        (self.root / "notes.md").write_text("changed revision\n")
        self.git("add", "notes.md")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "notes")
        self.assertNotEqual(self.stage("pre-pr")[0].returncode, 0)

    def test_failed_rerun_after_pr_preparation_blocks_merge_evidence(self):
        self.assertEqual(self.gate("ci").returncode, 0)
        self.pr_runs()
        self.pr.update(merged=True, merged_at="2026-10-16T12:00:00Z", merge_commit_sha="b" * 40,
                       merged_by={"login": "EverttonFernandes"})
        self.payload["repos/fixture/clinica/actions/runs"]["workflow_runs"][0]["conclusion"] = "failure"
        self.save_github()
        self.assertNotEqual(self.gate("human_review").returncode, 0)

    def test_push_ci_cannot_substitute_for_checks_triggered_by_the_pr(self):
        self.assertEqual(self.gate("ci").returncode, 0)
        self.assertNotEqual(self.gate("pr_ci").returncode, 0)
        self.assertNotEqual(self.stage("post-pr")[0].returncode, 0)
        self.pr_runs()
        result, report = self.stage("post-pr")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["status"], "AWAITING_USER")
        self.assertFalse(report["completion_allowed"])

    def test_echo_or_pending_review_cannot_replace_the_github_collector(self):
        self.state["verification"]["ci"]["command"] = [sys.executable, "-c", "print('green')"]
        self.fixture.save()
        self.fixture.approve()
        self.assertNotEqual(self.stage("local")[0].returncode, 0)

    def tracking(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPTS / "feature_tracking.py"), "--root", "tracking", *arguments],
                              cwd=self.root, capture_output=True, text=True)

    def completed_foundation(self):
        self.assertEqual(self.gate("ci").returncode, 0)
        self.pr_runs()
        self.pr.update(merged=True, merged_at="2026-10-16T12:00:00Z", merge_commit_sha=self.head,
                       merged_by={"login": "EverttonFernandes"})
        self.save_github()
        self.assertEqual(self.gate("human_review").returncode, 0)
        (self.root / "dependent.md").write_text("- [ ] Next increment\n")
        (self.root / "board.md").write_text("## Linha principal\n"
            "| 01 | M1 | [CT-001 — Foundation](source.md) | Técnica | — | To Do |\n"
            "| 02 | M1 | [CT-002 — Consumer](dependent.md) | Técnica | CT-001 | To Do |\n")
        self.assertEqual(self.tracking("import-kanban", "board.md").returncode, 0)
        path = self.root / "tracking/CT-001.json"
        record = json.loads(path.read_text())
        record["plan_path"] = "IMPLEMENTATION.md"
        path.write_text(json.dumps(record))
        self.assertEqual(self.tracking("dependencies", "CT-001", "--reason", "Foundation").returncode, 0)
        result = self.tracking("start", "CT-001")
        self.assertEqual(result.returncode, 0, result.stderr)
        token = json.loads(result.stdout)["token"]
        result = self.tracking("finish", "CT-001", "--lock-token", token)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.tracking("dependencies", "CT-002", "CT-001", "--reason", "Consumer").returncode, 0)

    def test_accepted_dependency_survives_code_evolution_and_loss_of_local_receipts(self):
        self.completed_foundation()
        (self.root / "code.txt").write_text("legitimate next story evolution\n")
        shutil.rmtree(self.root / ".git/harness/CT-001")
        result = self.tracking("ready", "CT-002")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cached_done_does_not_replace_verified_historical_user_merge(self):
        self.completed_foundation()
        self.pr["merged_by"] = {"login": "automation-bot"}
        self.save_github()
        result = self.tracking("ready", "CT-002")
        self.assertNotEqual(result.returncode, 0)

    def test_dependency_merge_must_be_in_the_current_git_history(self):
        self.completed_foundation()
        self.git("checkout", "--orphan", "unrelated-history")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "unrelated")
        result = self.tracking("ready", "CT-002")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not contain", result.stderr)


if __name__ == "__main__":
    unittest.main()
