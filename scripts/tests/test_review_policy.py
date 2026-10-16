"""Enforce different-model review before claiming a story is reviewed."""
import unittest

import test_harness_completion as fixtures


class ModelReviewTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CompletionTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.state["review_policy"] = {"require_different_model": True}
        self.fixture.save()

    def reviewed(self, **overrides):
        self.fixture.approve()
        self.fixture.state["evaluation"].update({
            "worker_model": "gpt-6-astra", "worker_reasoning_effort": "medium",
            "reviewer_model": "gpt-6-sol", **overrides})
        self.fixture.save()
        return self.fixture.check()

    def test_configured_executor_and_distinct_reviewer_are_accepted(self):
        result, report = self.reviewed()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["completion_allowed"])

    def test_same_model_is_rejected_even_with_different_session_ids(self):
        result, report = self.reviewed(reviewer_model="gpt-6-astra")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("model", " ".join(report["errors"]).lower())

    def test_unknown_model_cannot_prove_independence(self):
        for missing in (None, "", "unknown"):
            with self.subTest(missing=missing):
                result, _ = self.reviewed(worker_model=missing)
                self.assertNotEqual(result.returncode, 0)

    def test_executor_effort_must_match_the_user_policy(self):
        result, _ = self.reviewed(worker_reasoning_effort="low")
        self.assertNotEqual(result.returncode, 0)

    def test_same_executor_fallback_is_not_accepted_for_required_review(self):
        result, _ = self.reviewed(mode="separate-review-fallback", reason="Same executor re-read code")
        self.assertNotEqual(result.returncode, 0)

    def test_canonical_story_cannot_omit_the_delivery_gates(self):
        self.fixture.state["task_key"] = "CT-001"
        self.fixture.save()
        result, report = self.reviewed()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ci", " ".join(report["errors"]).lower())


if __name__ == "__main__":
    unittest.main()
