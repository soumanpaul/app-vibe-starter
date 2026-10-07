"""Project-local starter checks, explicit bootstrap and serialized native commands."""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ARCHIVED = {
    "docs/engineering/state.md": "state.md",
    "docs/engineering/agent-workflow.md": "agent-workflow.md",
    "docs/plans/v1-build.md": "v1-build.md",
    "docs/plans/agent-prompts.md": "agent-prompts.md",
}


def read_json(path):
    return json.loads(path.read_text())


def owners(root, relative):
    lanes = read_json(root / "docs/hackathon/ownership.json")["lanes"]
    return [lane for lane, data in lanes.items()
            if any(fnmatch.fnmatchcase(relative, pattern) for pattern in data["paths"])
            or relative == f"docs/hackathon/status/{lane}.md"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root):
    errors = []
    required = ["AGENTS.md", "docs/engineering/state.md", "docs/hackathon/README.md",
                "docs/hackathon/lanes.md", "docs/hackathon/prompts.md", "docs/hackathon/contracts.md",
                "docs/hackathon/preflight.md", "docs/hackathon/release-gates.md"]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"Missing {relative}")
    manifest = read_json(root / ".starter/source-manifest.json")
    for entry in manifest["files"]:
        relative = entry["path"]
        actual = root / entry["target"]
        if not actual.is_file() or digest(actual) != entry["sha256"]:
            errors.append(f"Preserved snapshot changed/missing: {relative} -> {entry['target']}")
        if entry["category"] == "implementation":
            assignment = owners(root, relative)
            if len(assignment) != 1:
                errors.append(f"Ownership must be unique: {relative}: {assignment}")
    coverage = read_json(root / "docs/hackathon/coverage.json")["features"]
    ids = set()
    requirements = set()
    for feature in coverage:
        if feature["id"] in ids:
            errors.append(f"Duplicate feature {feature['id']}")
        ids.add(feature["id"])
        requirements.update(feature["requirements"])
        if feature["owner"] not in read_json(root / "docs/hackathon/ownership.json")["lanes"]:
            errors.append(f"Unknown feature owner: {feature['id']}")
        for relative in feature["ux"]:
            if not (root / relative).is_file():
                errors.append(f"Missing UX for {feature['id']}: {relative}")
        if not feature["acceptance"] or not feature["paths"]:
            errors.append(f"Missing acceptance/paths: {feature['id']}")
    for number in range(1, 15):
        if f"R{number:02}" not in requirements:
            errors.append(f"Unmapped requirement R{number:02}")
    for lane in read_json(root / "docs/hackathon/ownership.json")["lanes"]:
        if not (root / f"docs/hackathon/status/{lane}.md").is_file():
            errors.append(f"Missing status for {lane}")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"PASS: {len(manifest['files'])} preserved files, unique source ownership, {len(coverage)} feature rows, R01–R14. Runtime/device gates NOT evaluated.")


def bootstrap(root, mode, bundle_id, apply):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z][A-Za-z0-9]*){2,}", bundle_id):
        raise ValueError("Use a reverse-domain ID such as org.yourteam.gurukulhackathon")
    if bundle_id == "org.gurukul.t0":
        raise ValueError("Choose a distinct bundle ID; do not overwrite the existing source app.")
    source = root / ".starter/reference-app"
    scaffold = {"package.json", "package-lock.json", "app.json", "tsconfig.json",
                "eslint.config.mjs", ".nvmrc", "scripts/private-llama.mjs", "src/t0/model.json"}
    excluded = {"scripts/check_harness.py", "tests/test_harness.py"}
    candidates = [path for path in sorted(source.rglob("*")) if path.is_file()
                  and path.relative_to(source).as_posix() not in excluded
                  and (mode == "reuse" or path.relative_to(source).as_posix() in scaffold)]
    if not candidates:
        raise ValueError("No reference snapshot found")
    collisions = [path.relative_to(source).as_posix() for path in candidates
                  if (root / path.relative_to(source)).exists()]
    record = root / ".starter/run.json"
    if record.exists():
        collisions.append(".starter/run.json")
    if collisions:
        raise ValueError("Refusing to overwrite existing paths:\n" + "\n".join(collisions))
    print(f"Mode={mode}; files={len(candidates)}; bundle={bundle_id}; no dependency installation, model download or build.")
    if not apply:
        print("Dry run only. Add --apply after checking hackathon reuse rules and preflight.")
        return
    for path in candidates:
        destination = root / path.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    config = read_json(root / "app.json")
    config["expo"]["slug"] = "gurukul-hackathon"
    config["expo"]["ios"]["bundleIdentifier"] = bundle_id
    config["expo"]["android"]["package"] = bundle_id
    (root / "app.json").write_text(json.dumps(config, indent=2) + "\n")
    for path in [root / "tests/ios/T7UITests.swift", root / "scripts/ios-t7-tests.rb"]:
        if path.exists():
            path.write_text(path.read_text().replace("org.gurukul.t0", bundle_id))
    record.write_text(json.dumps({"mode": mode, "bundleId": bundle_id,
                                 "evidence": "unverified", "nativeProject": "not generated",
                                 "warning": "Inspect generated scheme/target names before UI-test setup; old GurukulT0 names are reference-only."}, indent=2) + "\n")
    print("Bootstrap complete. Coordinator freezes contracts before worker writes. No inherited phone result is a target pass.")


def native_run(root, owner, command):
    if owner not in {"A", "LEAD"}:
        raise ValueError("Only A or LEAD may hold the native/toolchain lease")
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise ValueError("Provide a command after --")
    directory = root / ".starter/locks"
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / "native.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as failure:
        raise ValueError(f"Native lease occupied: {lock}. Inspect holder; never remove an active lock.") from failure
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump({"owner": owner, "pid": os.getpid(), "command": command}, stream)
        return subprocess.run(command, cwd=root, check=False).returncode
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("check")
    owner = commands.add_parser("owner")
    owner.add_argument("path")
    seed = commands.add_parser("bootstrap")
    seed.add_argument("--mode", choices=["reuse", "fresh"], required=True)
    seed.add_argument("--bundle-id", required=True)
    seed.add_argument("--apply", action="store_true")
    native = commands.add_parser("native-run")
    native.add_argument("--owner", choices=["A", "LEAD"], required=True)
    native.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == "check":
            check(ROOT)
        elif args.action == "owner":
            result = owners(ROOT, args.path)
            if len(result) != 1:
                raise ValueError(f"Unassigned/ambiguous path {args.path}: {result}; coordinator allocation required")
            print(result[0])
        elif args.action == "bootstrap":
            bootstrap(ROOT, args.mode, args.bundle_id, args.apply)
        else:
            return native_run(ROOT, args.owner, args.command)
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as failure:
        print(str(failure), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
