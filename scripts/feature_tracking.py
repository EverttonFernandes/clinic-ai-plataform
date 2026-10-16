"""Operational tracking; Kanban owns priority, harness_completion owns proof of completion."""
import argparse
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

import harness_completion as completion
import orchestration_lock


def now():
    return datetime.now(timezone.utc).isoformat()


def key(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value) or value == "index":
        raise ValueError("Invalid feature ID")
    return value


def load(root):
    records = {}
    for path in sorted(root.glob("*.json")):
        if path.name == "index.json":
            continue
        record = json.loads(path.read_text())
        if record["schema_version"] != 1 or path.stem != key(record["id"]):
            raise ValueError("Unsupported or inconsistent tracking record: " + str(path))
        records[record["id"]] = record
    return records


def validate_graph(records):
    visited, active = set(), set()

    def visit(identifier):
        if identifier not in records:
            raise ValueError("Missing prerequisite: " + identifier)
        if identifier in active:
            raise ValueError("Dependency cycle: " + identifier)
        if identifier in visited:
            return
        active.add(identifier)
        for dependency in records[identifier]["dependencies"]:
            visit(dependency["id"])
        active.remove(identifier)
        visited.add(identifier)

    for identifier in records:
        visit(identifier)


def proof(record):
    report = completion.check(record["plan_path"])
    state, _ = completion.read_state(record["plan_path"])
    if (report["task_key"] != record["id"] or
            Path(state["requirement_source"]["path"]).resolve() != Path(record["story_path"]).resolve() or
            not report["completion_allowed"]):
        raise ValueError("Unverified completion: " + record["id"])
    return report


def prerequisite_proof(record):
    """Accepted stories keep historical proof; current regressions belong to the consumer."""
    if not completion.review_policy.is_story(record["id"]):
        return proof(record)
    import pr_evidence
    state, _ = completion.read_state(record["plan_path"])
    report = (record.get("completion") or {}).get("report", {})
    source = state["requirement_source"]
    review = state["evaluation"]
    if (report.get("status") != "DONE" or report.get("completion_allowed") is not True
            or report.get("task_key") != record["id"] or state["task_key"] != record["id"]
            or report.get("source_sha256") != completion.sha(record["story_path"])
            or Path(source["path"]).resolve() != Path(record["story_path"]).resolve()
            or report.get("contract_sha256") != completion.contract_digest(state)
            or report.get("scope_sha256") != review.get("scope_sha256")
            or report.get("contract_sha256") != review.get("contract_sha256")
            or report.get("source_sha256") != review.get("source_sha256")
            or report.get("evaluation_sha256") != review.get("sha256")
            or review.get("sha256") != completion.sha(completion.local_path(review["path"]))
            or review.get("status") != "PASS" or completion.review_policy.model_errors(state)):
        raise ValueError("Accepted prerequisite has no valid historical proof: " + record["id"])
    delivery = report["delivery"]
    merged = delivery["human_review"]
    repository = pr_evidence.github_repository()
    if (merged["repository"] != repository or merged["kind"] != "merged"
            or any(delivery[gate][key] != merged[key] for gate in ("ci", "pr_ci")
                   for key in ("head_sha", "branch", "repository"))
            or delivery["pr_ci"]["number"] != merged["number"]):
        raise ValueError("Historical CI/PR/merge revisions differ")
    completion.review_policy.validate_branch(record["id"], merged["branch"])
    actual = pr_evidence.validate_merge(pr_evidence.api(repository, "pulls/" + str(merged["number"])),
                                       merged["head_sha"], merged["branch"], repository)
    if any(actual[key] != merged[key] for key in actual):
        raise ValueError("Historical user merge differs from GitHub")
    ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", actual["merge_commit_sha"], "HEAD"],
                              capture_output=True, timeout=10)
    if ancestor.returncode != 0:
        raise ValueError("Current base does not contain the accepted prerequisite merge")
    return report


def ready(records, identifier, seen=None):
    seen = set() if seen is None else seen
    if identifier in seen:
        return
    seen.add(identifier)
    record = records[identifier]
    completion.local_path(record["story_path"]).read_text()
    validate_declared_dependencies(record)
    if not record["dependencies_reviewed"]:
        raise ValueError("Dependencies need explicit review: " + identifier)
    if record.get("dependency_review_story_sha256") != completion.sha(record["story_path"]):
        raise ValueError("Story changed since dependency review: " + identifier)
    for dependency in record["dependencies"]:
        parent = records[dependency["id"]]
        ready(records, parent["id"], seen)
        if parent["status"] != "DONE":
            raise ValueError("Prerequisite not completed: " + parent["id"])
        prerequisite_proof(parent)  # Verify accepted history, not equality with today's code tree.


def event(record, kind, reason, reference=None):
    timestamp = now()
    record["events"].append({"at": timestamp, "type": kind, "reason": reason, "reference": reference})
    record["updated_at"] = timestamp


def board_entries(filename):
    """Read current Clínica board; keep legacy fixtures/imports explicitly distinguishable."""
    section = None
    for line in completion.local_path(filename).read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.startswith("|") or not cells[0].isdigit():
            continue
        if section == "Linha principal" and len(cells) == 6:
            order, phase, link, kind, dependencies, status = cells
        elif section == "Backlog opcional" and len(cells) == 5:
            order, link, phase, dependencies, status = cells
            kind = "Opcional"
        elif section in ("To Do", "Doing", "Review", "Backlog", "Done") and len(cells) >= 5:
            order, link, kind, phase, dependencies = cells[:5]
            status = section
        else:
            continue
        match = re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", link)
        if not match:
            raise ValueError("Unrecognized Kanban story link: " + link)
        identifier, _, title = match[1].partition(" — ")
        required = re.findall(r"\b(?:CT|C)-\d+\b", dependencies)
        yield {"id": key(identifier), "title": title or phase, "link": match[2], "type": kind,
               "order": int(order), "section": section, "status": status,
               "required": required, "dependencies_text": dependencies}


def validate_declared_dependencies(record, proposed=None):
    observation = record["kanban_observation"]
    entry = next((row for row in board_entries(observation["path"]) if row["id"] == record["id"]), None)
    if entry is None:
        raise ValueError("Story missing from current Kanban: " + record["id"])
    supplied = set(proposed if proposed is not None else [item["id"] for item in record["dependencies"]])
    missing = set(entry["required"]) - supplied
    if missing:
        raise ValueError("Declared prerequisites cannot be omitted: " + ", ".join(sorted(missing)))
    expected_path = (Path(observation["path"]).parent / entry["link"]).resolve()
    if expected_path != completion.local_path(record["story_path"]).resolve():
        raise ValueError("Kanban story path changed; reconcile tracking")
    if entry["status"] == "Backlog" and entry["section"] == "Backlog opcional":
        raise ValueError("Optional backlog must be explicitly promoted before execution")


def import_kanban(records, filename):
    board = completion.local_path(filename)
    count = 0
    for entry in board_entries(filename):
        identifier = entry["id"]
        if identifier in records:
            continue  # Import is additive: never overwrite execution history.
        story = (board.parent / entry["link"]).as_posix()
        story_exists = completion.local_path(story).is_file()
        record = {
            "schema_version": 1, "id": identifier, "title": entry["title"], "type": entry["type"],
            "story_path": story, "plan_path": f"docs/tasks/{identifier}/plano.md",
            "kanban_observation": {"path": filename, "section": entry["section"], "order": entry["order"],
                                   "relationship_text": entry["dependencies_text"], "observed_at": now()},
            "status": "TODO" if entry["status"] in ("To Do", "Backlog") else "UNVERIFIED",
            "dependencies": [{"id": value, "reason": "Declared in Kanban"} for value in entry["required"]],
            "dependencies_reviewed": False,
            "started_at": None, "completed_at": None, "updated_at": now(),
            "story_exists_at_import": story_exists,
            "history_before_import": "UNKNOWN", "completion": None, "events": [],
        }
        event(record, "IMPORTED", "Kanban observation only; execution and dependencies not verified")
        records[identifier] = record
        count += 1
    return count


@contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".writer-lock"
    lock.mkdir()  # Fail closed on simultaneous writers or an interrupted writer.
    try:
        yield
    finally:
        lock.rmdir()


def save(root, records):
    for identifier, record in records.items():
        path = root / (identifier + ".json")
        if not path.exists() or json.loads(path.read_text()) != record:
            completion.write_json(path, record)
    index = {"schema_version": 1, "generated_at": now(), "authoritative_for_priority": False,
             "features": [{"id": r["id"], "title": r["title"], "status": r["status"],
                           "path": r["id"] + ".json", "started_at": r["started_at"],
                           "completed_at": r["completed_at"],
                           "failure_count": sum(e["type"] == "FAILURE" for e in r["events"])}
                          for r in sorted(records.values(), key=lambda r: (r["kanban_observation"]["order"], r["id"]))]}
    completion.write_json(root / "index.json", index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="docs/tracking")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("import-kanban").add_argument("board")
    for action in ("dependencies", "ready", "start", "failure", "review", "finish"):
        command = sub.add_parser(action)
        command.add_argument("id", type=key)
        if action != "ready":
            command.add_argument("--lock-token")
        if action == "start":
            command.add_argument("--owner", default="local-agent")
        if action == "dependencies":
            command.add_argument("prerequisites", nargs="*", type=key)
        if action in ("dependencies", "failure", "review"):
            command.add_argument("--reason", required=True)
            command.add_argument("--reference")
    sub.add_parser("index")
    args = parser.parse_args()
    root = completion.local_path(args.root)
    ownership = orchestration_lock.Store() if hasattr(args, "lock_token") else nullcontext()
    with ownership as locks, locked(root):
        records = load(root)
        current_lock = locks.authorize(args.id, args.lock_token) if locks else None
        if args.action in ("failure", "review", "finish") and current_lock is None:
            raise ValueError("Mutation requires active task ownership")
        if args.action == "import-kanban":
            imported = import_kanban(records, args.board)
            print(f"Imported {imported} stories without inferring historical completion")
        elif args.action != "index":
            record = records[args.id]
            reason = getattr(args, "reason", "")
            if hasattr(args, "reason") and not reason.strip():
                raise ValueError("Reason is required")
            if args.action == "dependencies":
                validate_declared_dependencies(record, args.prerequisites)
                record["dependencies"] = [{"id": value, "reason": reason} for value in sorted(set(args.prerequisites))]
                validate_graph(records)
                record["dependencies_reviewed"] = True
                record["dependency_review_story_sha256"] = completion.sha(record["story_path"])
                event(record, "DEPENDENCIES_REVIEWED", reason, args.reference)
            elif args.action in ("ready", "start", "finish"):
                validate_graph(records)
                ready(records, args.id)
                if args.action == "ready":
                    print("Prerequisites verified; consult current Kanban priority before starting")
                    return 0
                if args.action == "start":
                    completion.review_policy.validate_branch(args.id)
                    if record["status"] == "DONE":
                        raise ValueError("Completed story must be explicitly reviewed before reopening")
                    current_lock = current_lock or locks.acquire(args.id, args.owner)
                    record["last_execution"] = {k: current_lock[k] for k in ("run_id", "owner", "worktree")}
                    record["status"] = "IN_PROGRESS"
                    record["started_at"] = record["started_at"] or now()
                    record["completed_at"] = None
                    event(record, "STARTED", "Prerequisites checked")
                else:
                    report = proof(record)
                    record["status"] = "DONE"
                    record["completed_at"] = record["completed_at"] or now()
                    record["completion"] = {"verified_at": now(), "plan_path": record["plan_path"], "report": report}
                    event(record, "COMPLETED", "Existing completion gate approved")
            else:
                record["status"] = "BLOCKED" if args.action == "failure" else "IN_REVIEW"
                record["completed_at"] = None
                record["completion"] = None
                event(record, "FAILURE" if args.action == "failure" else "REVIEW", reason, args.reference)
        validate_graph(records)
        save(root, records)
        if args.action == "start":
            print(json.dumps(current_lock, indent=2))
        elif args.action == "finish" and current_lock:
            locks.release(args.id, args.lock_token, "Tracking completion persisted")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("Tracking blocked: " + str(error), file=sys.stderr)
        sys.exit(1)
