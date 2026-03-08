#!/usr/bin/env python3
"""Copy a benchmark case into a working directory and optionally initialize git."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def copy_skills(repo_root: Path, out_dir: Path) -> None:
    skill_root = repo_root / ".claude" / "skills"
    dest_root = out_dir / ".claude" / "skills"
    dest_root.mkdir(parents=True, exist_ok=True)

    for skill_name in ("agent-rock", "rock-quick", "rock-deep"):
        src = skill_root / skill_name
        dest = dest_root / skill_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)


def materialize_case(repo_root: Path, case_dir: Path, out_dir: Path, init_git: bool, copy_local_skills: bool) -> None:
    repo_dir = case_dir / "repo"
    manifest_path = case_dir / "benchmark.json"

    if not repo_dir.is_dir():
        raise SystemExit(f"Missing repo directory: {repo_dir}")
    if not manifest_path.is_file():
        raise SystemExit(f"Missing manifest: {manifest_path}")

    if out_dir.exists():
      shutil.rmtree(out_dir)

    shutil.copytree(repo_dir, out_dir)
    shutil.copy2(manifest_path, out_dir / ".agent-rock-benchmark.json")

    if copy_local_skills:
        copy_skills(repo_root, out_dir)

    if init_git:
        subprocess.run(["git", "init"], cwd=out_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=out_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "seed benchmark case"],
            cwd=out_dir,
            check=True,
            capture_output=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize a benchmark case into a work directory.")
    parser.add_argument("--case", required=True, help="Case id under benchmarks/cases/")
    parser.add_argument("--out", required=True, help="Destination directory")
    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Do not initialize a git repository in the materialized output",
    )
    parser.add_argument(
        "--skip-skills",
        action="store_true",
        help="Do not copy local benchmark skills into the materialized output",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    case_dir = repo_root / "benchmarks" / "cases" / args.case
    out_dir = Path(args.out).resolve()

    if not case_dir.is_dir():
        known = sorted(p.name for p in (repo_root / "benchmarks" / "cases").iterdir() if p.is_dir())
        raise SystemExit(f"Unknown case '{args.case}'. Known cases: {', '.join(known)}")

    materialize_case(
        repo_root=repo_root,
        case_dir=case_dir,
        out_dir=out_dir,
        init_git=not args.skip_git,
        copy_local_skills=not args.skip_skills,
    )

    print(f"Materialized {case_dir.name} into {out_dir}")


if __name__ == "__main__":
    main()
