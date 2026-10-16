"""Story-specific review and delivery invariants; no external mutations."""
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def policy():
    return json.loads((ROOT / ".agents/harness-policy.json").read_text())


def is_story(key):
    return re.fullmatch(r"(?:CT|C)-\d+", key) is not None


def requires_model_review(state):
    return is_story(state["task_key"]) or state.get("review_policy", {}).get("require_different_model") is True


def model_errors(state):
    if not requires_model_review(state):
        return []
    expected, review = policy(), state["evaluation"]
    valid = (review.get("mode") == "independent"
             and review.get("worker_model") == expected["executor"]["model"]
             and review.get("worker_reasoning_effort") == expected["executor"]["reasoning_effort"]
             and review.get("reviewer_model") == expected["reviewer"]["model"]
             and review.get("worker_model") != review.get("reviewer_model")
             and bool(review.get("worker_id")) and bool(review.get("reviewer_id"))
             and review.get("worker_id") != review.get("reviewer_id"))
    return [] if valid else ["Independent model review must match configured executor, effort and reviewer; no fallback"]


def validate_branch(key, branch=None):
    if not is_story(key):
        return
    branch = branch or subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
    if not re.fullmatch(re.escape(policy()["branch_prefix"] + key) + r"-[a-z0-9][a-z0-9-]*", branch):
        raise ValueError("Story requires its own branch: story/" + key + "-<slug>")


def delivery_errors(state, plan):
    if not is_story(state["task_key"]):
        return []
    errors = []
    for gate, mode in (("ci", "ci"), ("pr_ci", "pr"), ("human_review", "merged")):
        command = state["verification"].get(gate, {}).get("command", [])
        if (gate not in state["exit_bar"] or len(command) != 4
                or Path(command[0]).name not in ("python", "python3", Path(sys.executable).name)
                or Path(command[1]).resolve() != (ROOT / "scripts/pr_evidence.py").resolve()
                or Path(command[2]).resolve() != Path(plan).resolve() or command[3] != mode):
            errors.append("Story requires collector-backed " + gate + " gate")
    return errors
