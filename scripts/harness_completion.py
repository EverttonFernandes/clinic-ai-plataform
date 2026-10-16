"""Record actual commands and check completion from IMPLEMENTATION.md, never prose alone."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import uuid

import review_policy


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_path(name):
    path = Path(name)
    if path.is_absolute() or not path.resolve().is_relative_to(Path.cwd().resolve()):
        raise ValueError("Evidence/source/scope must stay inside the repository")
    return path


def read_state(path):
    text = local_path(path).read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("Missing structured frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    try:
        state = json.loads(header)
    except ValueError as error:
        raise ValueError("Legacy YAML/unreadable state: migrate frontmatter to JSON (valid YAML subset) on resume; never infer PASS") from error
    if not isinstance(state, dict):
        raise ValueError("State must be an object")
    for key in ("task_key", "objective"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            raise ValueError("Missing " + key)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", state["task_key"]):
        raise ValueError("Invalid task key")
    for key in ("requirements", "exit_bar", "verification", "requirement_source", "evaluation"):
        if not isinstance(state.get(key), dict) or not state[key]:
            raise ValueError("Missing nonempty map: " + key)
    if not isinstance(state.get("scope"), list) or not state["scope"]:
        raise ValueError("Missing scope")
    if not isinstance(state.get("correction_queue"), list) or not isinstance(state.get("handoff"), dict):
        raise ValueError("Missing correction_queue/handoff")
    if state.get("phase") not in ("PLANNING", "EXECUTION", "AUDIT", "REVIEW", "DONE", "BLOCKED"):
        raise ValueError("Unknown phase")
    return state, body


def scope_digest(state):
    files = set()
    for name in state["scope"]:
        path = local_path(name)
        files.update(path.rglob("*") if path.is_dir() else [path])
    digest = hashlib.sha256()
    for path in sorted(files):
        local_path(str(path))
        if path.is_dir() or any(part in (".git", "__pycache__", "node_modules") for part in path.parts):
            continue
        digest.update(str(path).encode() + b"\0")
        digest.update((str(path.stat().st_mode) + sha(path)).encode() if path.is_file() else b"MISSING")
    return digest.hexdigest()


def contract_digest(state):
    contract = {key: state[key] for key in ("task_key", "objective", "scope", "requirement_source", "verification")}
    contract["requirements"] = {key: {k: v for k, v in value.items() if k != "status"}
                                for key, value in state["requirements"].items()}
    contract["required_gates"] = sorted(state["exit_bar"])
    contract["not_applicable"] = state.get("not_applicable", {})
    contract["review_policy"] = state.get("review_policy", {})
    if review_policy.requires_model_review(state):
        contract["harness_policy"] = review_policy.policy()
    return hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest()


def original_requirements(path):
    """Extract checkboxes and complete BDD scenarios, never infer fulfilled criteria."""
    text = local_path(path).read_text()
    criteria = re.findall(r"^\s*[-*]\s+\[[ xX]\]\s+(.+)$", text, re.MULTILINE)
    result = {f"AC{index}": description.strip() for index, description in enumerate(criteria, 1)}
    scenarios = re.findall(r"^  Cenário: .+(?:\n    .+)+", text, re.MULTILINE)
    result.update({f"BDD{index}": " ".join(description.split())
                   for index, description in enumerate(scenarios, 1)})
    return result


def command_for(state, name):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError("Invalid verification key")
    command = state["verification"][name]["command"]
    if not isinstance(command, list) or not command or not all(isinstance(arg, str) and arg for arg in command):
        raise ValueError("Command must be a nonempty argv array")
    return command


def evidence_directory(state, name):
    git_dir = subprocess.check_output(["git", "rev-parse", "--git-path", "harness"], text=True).strip()
    # Git owns this administrative path; linked worktrees keep it outside the checkout.
    return Path(git_dir) / state["task_key"] / name


def evidence_log(state, name, report):
    path = Path(report["log"]).resolve()
    if path.parent != evidence_directory(state, name).resolve():
        raise ValueError("Log must stay inside this task verification directory")
    return path


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    with temporary.open("x") as file:
        os.chmod(temporary, 0o600)
        json.dump(value, file, indent=2)
    temporary.replace(path)


def verify(path, name, timeout):
    state, _ = read_state(path)
    command = command_for(state, name)
    source = state["requirement_source"]
    if sha(local_path(source["path"])) != source["sha256"]:
        raise ValueError("Requirement source changed; reconcile original criteria first")
    directory = evidence_directory(state, name)
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    run_id = uuid.uuid4().hex
    log_path = directory / (run_id + ".log")
    report = {"task_key": state["task_key"], "check": name, "run_id": run_id,
              "command": command, "cwd": str(Path.cwd()), "source_sha256": source["sha256"],
              "contract_sha256": contract_digest(state),
              "scope": state["scope"], "scope_sha256": scope_digest(state), "started_at": time.time(),
              "status": "RUNNING", "exit_code": None, "log": str(log_path)}
    plan_sha = sha(path)
    for destination in (directory / (run_id + ".json"), directory / "latest.json"):
        write_json(destination, report)
    process = None
    try:
        with log_path.open("x") as log:
            os.chmod(log_path, 0o600)
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            report["exit_code"] = process.wait(timeout=timeout)
        report["status"] = "PASS" if report["exit_code"] == 0 else "FAIL"
    except (OSError, subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        if process and process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        report["status"] = "FAIL"
        report["error"] = type(error).__name__
    finally:
        report["finished_at"] = time.time()
        report["duration_seconds"] = report["finished_at"] - report["started_at"]
        if log_path.exists():
            report["log_sha256"] = sha(log_path)
        try:
            if scope_digest(state) != report["scope_sha256"] or sha(path) != plan_sha:
                report.update(status="FAIL", error="Snapshot changed during verification")
        except (OSError, ValueError):
            report.update(status="FAIL", error="Snapshot unavailable after verification")
        for destination in (directory / (run_id + ".json"), directory / "latest.json"):
            write_json(destination, report)
    return report


def check(path, stage="done"):
    state, body = read_state(path)
    errors, failed, pending = [], False, False
    errors.extend(review_policy.model_errors(state))
    errors.extend(review_policy.delivery_errors(state, path))
    deferred = {"local": {"ci", "pr_ci", "human_review"}, "pre-pr": {"pr_ci", "human_review"},
                "post-pr": {"human_review"}, "done": set()}[stage]
    source = state["requirement_source"]
    current_source = sha(local_path(source["path"]))
    scope = scope_digest(state)
    if current_source != source.get("sha256"):
        errors.append("Original requirement source changed")
    for name, description in original_requirements(source["path"]).items():
        planned = state["requirements"].get(name, {})
        if " ".join(planned.get("description", "").split()) != " ".join(description.split()):
            errors.append("Original criterion omitted or altered: " + name)
    if re.search(r"^\s*[-*]\s+\[ \]", body, re.MULTILINE):
        errors.append("Unchecked items remain in IMPLEMENTATION.md")
        pending = True
    for item in state["correction_queue"]:
        if item.get("status") != "CLOSED":
            errors.append("Open/unknown correction: " + str(item.get("id")))
            pending = True
    verified, review_gates, delivery = set(), set(), {}
    for name in state["verification"]:
        if review_policy.is_story(state["task_key"]) and name in deferred:
            continue
        try:
            command = command_for(state, name)
            report = json.loads((evidence_directory(state, name) / "latest.json").read_text())
            failed |= report.get("status") == "FAIL"
            valid = (report.get("status") == "PASS" and type(report.get("exit_code")) is int
                     and report["exit_code"] == 0 and report.get("command") == command
                     and report.get("contract_sha256") == contract_digest(state)
                     and report.get("task_key") == state["task_key"] and report.get("check") == name
                     and report.get("scope") == state["scope"] and report.get("scope_sha256") == scope
                     and report.get("source_sha256") == current_source
                     and report.get("log_sha256") == sha(evidence_log(state, name, report))
                     and 0 <= time.time() - report["finished_at"] <= 86400)
            if not valid:
                raise ValueError("Failed, incomplete, expired or stale verification")
            if review_policy.is_story(state["task_key"]) and name in ("ci", "pr_ci", "human_review"):
                import pr_evidence
                payload = json.loads(evidence_log(state, name, report).read_text())
                pr_evidence.validate_evidence(state, name, payload, stage)
                delivery[name] = payload
            verified.add(name)
        except (OSError, ValueError, KeyError, TypeError):
            errors.append("No valid command evidence: " + name)
        if state["exit_bar"].get(name) != "PASS":
            errors.append("Required verification gate must be PASS: " + name)
    for name, status in state["exit_bar"].items():
        if review_policy.is_story(state["task_key"]) and name in deferred:
            continue
        if status == "PASS":
            if name not in verified:
                review_gates.add(name)
        elif (status == "N/A" and name not in state["verification"]
              and name not in ("security", "security_review", "arch_review", "architecture_review", "final_review")
              and state.get("not_applicable", {}).get(name)):
            continue
        else:
            failed |= status == "FAIL"
            pending |= status == "PENDING"
            errors.append("Gate not satisfied: " + name + "=" + str(status))
    review = state["evaluation"]
    try:
        valid_review = (review["status"] == "PASS" and review["scope_sha256"] == scope
                        and review["contract_sha256"] == contract_digest(state)
                        and review["source_sha256"] == current_source
                        and review["sha256"] == sha(local_path(review["path"]))
                        and bool(review["worker_id"]) and bool(review["reviewer_id"]))
        if review["mode"] == "independent":
            valid_review &= review["reviewer_id"] != review["worker_id"]
        elif review["mode"] == "separate-review-fallback":
            valid_review &= bool(review.get("reason"))
        else:
            valid_review = False
        if not valid_review:
            raise ValueError("Review invalid")
        for name in review_gates - set(review.get("gates", ["final_review"])):
            errors.append("Gate has no executed verification or review: " + name)
        verified.add("evaluation")
    except (OSError, ValueError, KeyError, TypeError):
        errors.append("Evaluator missing, stale or not independent (fallback must be explicit)")
    for name, requirement in state["requirements"].items():
        refs = requirement.get("evidence", [])
        if requirement.get("status") != "PASS" or not refs or not set(refs) <= verified:
            errors.append("Criterion not verified: " + name)
            pending |= requirement.get("status") == "PENDING"
            failed |= requirement.get("status") == "FAIL"
    blocked = bool(state["handoff"].get("blockers")) or state["phase"] == "BLOCKED"
    if blocked:
        errors.append("Human/environment blockers remain")
    status = "FAILED" if failed else "BLOCKED" if blocked else "PARTIALLY_DONE" if pending else "UNVERIFIED" if errors else "DONE"
    if not errors and stage != "done":
        status = {"local": "LOCAL_READY", "pre-pr": "READY_FOR_PR", "post-pr": "AWAITING_USER"}[stage]
    return {"task_key": state["task_key"], "status": status, "completion_allowed": not errors and stage == "done",
            "stage_allowed": not errors, "stage": stage,
            "errors": errors, "scope_sha256": scope, "source_sha256": current_source,
            "contract_sha256": contract_digest(state),
            "delivery": delivery, "evaluation_sha256": review.get("sha256"),
            "evaluation_mode": review.get("mode"), "next_action": state["handoff"].get("next_action"),
            "scope": state["scope"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("check", "handoff", "verify", "criteria"):
        command = sub.add_parser(action)
        command.add_argument("plan")
        if action in ("check", "handoff"):
            command.add_argument("--stage", choices=("local", "pre-pr", "post-pr", "done"), default="done")
        if action == "verify":
            command.add_argument("name")
            command.add_argument("--timeout", type=float, default=1800)
    args = parser.parse_args()
    try:
        if args.action == "criteria":
            result = original_requirements(args.plan)
            success = bool(result)
        elif args.action == "verify":
            if not 0 < args.timeout <= 14400:
                raise ValueError("Timeout must be between 0 and 14400 seconds")
            result = verify(args.plan, args.name, args.timeout)
            success = result["status"] == "PASS"
        else:
            result = check(args.plan, args.stage)
            success = result["stage_allowed"]
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.CalledProcessError) as error:
        result = {"status": "UNVERIFIED", "completion_allowed": False, "errors": [str(error)]}
        success = False
    print(json.dumps(result, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
