"""Persistent task ownership for cooperating agents in a shared local Git repository."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import uuid

from harness_completion import write_json


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def task_id(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
        raise ValueError("Invalid task ID")
    return value


class Store:
    """Short OS mutex protects metadata; persistent per-task files protect executions."""

    def __enter__(self):
        if os.name != "posix":
            raise ValueError("Orchestration locks require Linux/WSL or another POSIX host")
        import fcntl
        common = subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], text=True).strip()
        self.root = Path(common) / "harness/orchestration"
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.guard = (self.root / ".metadata-mutex").open("a")
        try:
            fcntl.flock(self.guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BaseException:
            self.guard.close()
            raise
        return self

    def __exit__(self, *args):
        self.guard.close()

    def path(self, identifier):
        return self.root / (task_id(identifier) + ".lock")

    def status(self, identifier):
        path = self.path(identifier)
        if not path.exists():
            return None
        value = json.loads(path.read_text())
        if (value["schema_version"] != 1 or value["task_id"] != identifier or
                not all(isinstance(value[k], str) and value[k] for k in
                        ("token", "run_id", "owner", "acquired_at", "heartbeat_at")) or
                not all(re.fullmatch(r"[0-9a-f]{32}", value[k]) for k in ("token", "run_id"))):
            raise ValueError("Corrupt task lock; inspect manually")
        return value

    def authorize(self, identifier, token):
        current = self.status(identifier)
        if current is None:
            if token:
                raise ValueError("Execution token is stale: no active lock")
            return None
        if not token or current["token"] != token:
            raise ValueError("Task is owned by another execution: " + identifier)
        return current

    def acquire(self, identifier, owner):
        if not owner.strip():
            raise ValueError("Owner must be identified")
        if self.status(identifier) is not None:
            raise ValueError("Task already acquired: " + identifier)
        moment = timestamp()
        record = {"schema_version": 1, "task_id": identifier, "owner": owner,
                  "run_id": uuid.uuid4().hex, "token": uuid.uuid4().hex,
                  "acquired_at": moment, "heartbeat_at": moment,
                  "host": socket.gethostname(), "worktree": str(Path.cwd())}
        # Exclusive creation remains fail-closed if writing is interrupted.
        with self.path(identifier).open("x") as file:
            os.chmod(self.path(identifier), 0o600)
            json.dump(record, file, indent=2)
        return record

    def heartbeat(self, identifier, token):
        record = self.authorize(identifier, token)
        if record is None:
            raise ValueError("No execution to renew")
        record["heartbeat_at"] = timestamp()
        write_json(self.path(identifier), record)
        return record

    def release(self, identifier, token, reason="Owner released", expected_heartbeat=None):
        record = self.authorize(identifier, token)
        if record is None:
            raise ValueError("No execution to release")
        if expected_heartbeat is not None and record["heartbeat_at"] != expected_heartbeat:
            raise ValueError("Heartbeat changed; recovery refused")
        history = self.root / "history"
        history.mkdir(exist_ok=True, mode=0o700)
        write_json(history / (record["run_id"] + ".json"),
                   dict(record, released_at=timestamp(), release_reason=reason))
        self.path(identifier).unlink()
        return {"task_id": identifier, "released": True, "run_id": record["run_id"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("acquire", "status", "heartbeat", "release", "recover"):
        command = sub.add_parser(action)
        command.add_argument("id", type=task_id)
        if action == "acquire":
            command.add_argument("--owner", required=True)
        if action in ("heartbeat", "release", "recover"):
            command.add_argument("--token", required=True)
        if action == "recover":
            command.add_argument("--expected-heartbeat", required=True)
            command.add_argument("--reason", required=True)
            command.add_argument("--confirm-inactive", action="store_true")
    args = parser.parse_args()
    with Store() as store:
        if args.action == "acquire":
            result = store.acquire(args.id, args.owner)
        elif args.action == "status":
            result = store.status(args.id)
        elif args.action == "heartbeat":
            result = store.heartbeat(args.id, args.token)
        elif args.action == "release":
            result = store.release(args.id, args.token)
        else:
            if not args.confirm_inactive or not args.reason.strip():
                raise ValueError("Recovery requires explicit confirmation of an inactive owner and reason")
            result = store.release(args.id, args.token, "RECOVERY: " + args.reason, args.expected_heartbeat)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("Orchestration blocked: " + str(error), file=sys.stderr)
        sys.exit(1)
