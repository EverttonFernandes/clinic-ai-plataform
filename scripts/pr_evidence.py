"""Collect read-only GitHub evidence for CI or a user's merged story PR."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlencode

import harness_completion as completion
import review_policy


def git(*arguments):
    return subprocess.check_output(["git", *arguments], text=True).strip()


def github_repository():
    remote = git("remote", "get-url", "origin")
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:)([\w.-]+/[\w.-]+?)(?:\.git)?/?", remote)
    if not match:
        raise ValueError("Origin must identify a GitHub repository")
    return match[1]


def api(repository, resource, parameters=None):
    endpoint = "repos/" + repository + "/" + resource
    if parameters:
        endpoint += "?" + urlencode(parameters)
    output = subprocess.check_output(["gh", "api", "--method", "GET", endpoint], text=True, timeout=45)
    return json.loads(output)


def workflow_matches(run, expected_path, event, pr_number):
    """REST can return a workflow path with @ref; HEAD/PR metadata binds the revision."""
    path, separator, reference = run.get("path", "").partition("@")
    if path != expected_path:
        return False
    if not separator:
        return True
    branch = run.get("head_branch", "")
    allowed = {branch, "refs/heads/" + branch, run.get("head_sha")}
    if event == "pull_request":
        base = review_policy.policy()["base_branch"]
        allowed.update((base, "refs/heads/" + base, f"refs/pull/{pr_number}/merge", f"refs/pull/{pr_number}/head"))
    return bool(reference) and reference in allowed


def validate_runs(payload, head, required, event="push", pr_number=None):
    if payload.get("total_count", 0) >= 100:
        raise ValueError("Too many workflow runs; cannot establish complete CI evidence")
    latest = {}
    for run in payload.get("workflow_runs", []):
        if run.get("event") != event:
            continue
        if event == "pull_request":
            if not any(pr.get("number") == pr_number and pr.get("head", {}).get("sha") == head
                       for pr in run.get("pull_requests", [])):
                continue
        elif run.get("head_sha") != head:
            continue
        name = run.get("name")
        if (name not in required or not workflow_matches(run, required[name], event, pr_number)
                or type(run.get("workflow_id")) is not int or run["workflow_id"] <= 0):
            continue
        if name not in latest or (run["id"], run.get("run_attempt", 1)) > (latest[name]["id"], latest[name].get("run_attempt", 1)):
            latest[name] = run
    if not set(required) <= latest.keys():
        raise ValueError("Required CI workflow absent: " + ", ".join(sorted(set(required) - latest.keys())))
    if not latest or any(run.get("status") != "completed" or run.get("conclusion") != "success"
                         for run in latest.values()):
        raise ValueError("CI is pending, skipped, cancelled or failed on the exact HEAD")
    return [{"name": run["name"], "id": run["id"], "url": run["html_url"],
             "head_sha": head, "run_sha": run["head_sha"], "event": event,
             "path": run["path"], "workflow_id": run["workflow_id"],
             "conclusion": "success"} for run in latest.values()]


def validate_merge(pr, head, branch, repository):
    settings = review_policy.policy()
    if (pr.get("head", {}).get("sha") != head or pr.get("head", {}).get("ref") != branch
            or pr.get("head", {}).get("repo", {}).get("full_name") != repository
            or pr.get("base", {}).get("repo", {}).get("full_name") != repository
            or pr.get("base", {}).get("ref") != settings["base_branch"]
            or pr.get("merged") is not True or not pr.get("merged_at")
            or pr.get("merged_by", {}).get("login") != settings["manual_reviewer"]):
        raise ValueError("User acceptance/merge of this exact story revision is not verified")
    return {"number": pr["number"], "url": pr["html_url"], "merged_at": pr["merged_at"],
            "merged_by": pr["merged_by"]["login"], "merge_commit_sha": pr["merge_commit_sha"]}


def collect(plan, mode):
    state, _ = completion.read_state(plan)
    repository = github_repository()
    if mode == "ci":
        branch, head = git("branch", "--show-current"), git("rev-parse", "HEAD")
        review_policy.validate_branch(state["task_key"], branch)
        if git("status", "--porcelain", "--", *state["scope"]):
            raise ValueError("Commit scoped changes before collecting CI evidence")
        if git("diff", "HEAD", "--", *state["scope"]):
            raise ValueError("Scoped changes differ from HEAD")
        payload = api(repository, "actions/runs", {"head_sha": head, "branch": branch, "per_page": 100})
        workflows = validate_runs(payload, head, review_policy.policy()["required_workflows"])
        return {"kind": "ci", "head_sha": head, "branch": branch, "repository": repository, "workflows": workflows}
    receipt = json.loads((completion.evidence_directory(state, "ci") / "latest.json").read_text())
    ci = json.loads(completion.evidence_log(state, "ci", receipt).read_text())
    if ci["repository"] != repository:
        raise ValueError("CI repository differs from origin")
    head, branch = ci["head_sha"], ci["branch"]
    review_policy.validate_branch(state["task_key"], branch)
    owner = repository.split("/")[0]
    prs = api(repository, "pulls", {"head": owner + ":" + branch, "state": "all", "per_page": 100})
    matching = [pr for pr in prs if pr["head"]["sha"] == head]
    if len(matching) != 1:
        raise ValueError("Exactly one PR for the verified HEAD is required")
    pr = api(repository, "pulls/" + str(matching[0]["number"]))
    settings = review_policy.policy()
    if (pr["head"]["sha"] != head or pr["head"]["ref"] != branch
            or pr["head"]["repo"]["full_name"] != repository
            or pr["base"]["repo"]["full_name"] != repository
            or pr["base"]["ref"] != settings["base_branch"]):
        raise ValueError("PR does not match the verified story revision/base/repository")
    # PR runs can test a synthetic merge SHA; bind them through pull_requests.head.sha.
    pr_runs = api(repository, "actions/runs", {"event": "pull_request", "branch": branch, "per_page": 100})
    workflows = validate_runs(pr_runs, head, settings["required_workflows"], "pull_request", pr["number"])
    if mode == "pr":
        return {"kind": "pr", "head_sha": head, "branch": branch, "repository": repository,
                "number": pr["number"], "url": pr["html_url"], "workflows": workflows}
    merged = validate_merge(pr, head, branch, repository)
    pr_receipt = json.loads((completion.evidence_directory(state, "pr_ci") / "latest.json").read_text())
    pr_ci = json.loads(completion.evidence_log(state, "pr_ci", pr_receipt).read_text())
    if any(pr_ci[key] != value for key, value in (("head_sha", head), ("number", pr["number"]), ("repository", repository))):
        raise ValueError("PR CI and merge evidence refer to different revisions")
    # Recheck workflows at merge time: a failed rerun cannot reuse the old green receipt.
    validate_runs(api(repository, "actions/runs", {"head_sha": head, "branch": branch, "per_page": 100}),
                  head, review_policy.policy()["required_workflows"])
    return {"kind": "merged", "head_sha": head, "branch": branch, "repository": repository, **merged}


def validate_evidence(state, gate, payload, stage):
    expected = {"ci": "ci", "pr_ci": "pr", "human_review": "merged"}[gate]
    if payload.get("kind") != expected or not re.fullmatch(r"[0-9a-f]{40}", payload.get("head_sha", "")):
        raise ValueError("Invalid GitHub collector evidence")
    review_policy.validate_branch(state["task_key"], payload["branch"])
    if payload["repository"] != github_repository():
        raise ValueError("Evidence belongs to another repository")
    if git("diff", payload["head_sha"], "--", *state["scope"]):
        raise ValueError("Verified Git revision differs from current scope")
    if stage in ("pre-pr", "post-pr") and (git("rev-parse", "HEAD") != payload["head_sha"]
                              or git("branch", "--show-current") != payload["branch"]):
        raise ValueError("Pre-PR CI must match the current HEAD and story branch")
    if gate == "human_review":
        report = json.loads((completion.evidence_directory(state, "ci") / "latest.json").read_text())
        ci = json.loads(completion.evidence_log(state, "ci", report).read_text())
        if any(ci[key] != payload[key] for key in ("head_sha", "repository", "branch")):
            raise ValueError("Merge and CI evidence refer to different revisions")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan")
    parser.add_argument("mode", choices=("ci", "pr", "merged"))
    args = parser.parse_args()
    try:
        print(json.dumps(collect(args.plan, args.mode), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("GitHub evidence pending: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
