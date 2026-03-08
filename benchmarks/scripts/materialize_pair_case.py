#!/usr/bin/env python3
"""Copy a paired benchmark variant into a working directory and optionally initialize git."""

from __future__ import annotations

import argparse
import json
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


def build_variant_manifest(pair_manifest: dict, variant: str) -> dict:
    variant_manifest = dict(pair_manifest["variants"][variant])
    variant_manifest["id"] = f"{pair_manifest['id']}-{variant}"
    variant_manifest["name"] = f"{pair_manifest['name']} ({variant})"
    variant_manifest["description"] = pair_manifest.get("description", "")
    variant_manifest["stack"] = pair_manifest.get("stack", [])
    variant_manifest["pair_id"] = pair_manifest["id"]
    variant_manifest["pair_variant"] = variant
    return variant_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize a paired benchmark variant into a work directory.")
    parser.add_argument("--pair", required=True, help="Pair id under benchmarks/pairs/")
    parser.add_argument("--variant", required=True, choices=["vulnerable", "fixed"], help="Variant to materialize")
    parser.add_argument("--out", required=True, help="Destination directory")
    parser.add_argument("--skip-git", action="store_true", help="Do not initialize a git repository")
    parser.add_argument("--skip-skills", action="store_true", help="Do not copy local benchmark skills")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    pair_dir = repo_root / "benchmarks" / "pairs" / args.pair
    pair_manifest_path = pair_dir / "pair.json"
    repo_dir = pair_dir / args.variant / "repo"
    out_dir = Path(args.out).resolve()

    if not pair_manifest_path.is_file():
        raise SystemExit(f"Missing pair manifest: {pair_manifest_path}")
    if not repo_dir.is_dir():
        raise SystemExit(f"Missing repo directory: {repo_dir}")

    pair_manifest = json.loads(pair_manifest_path.read_text())
    variant_manifest = build_variant_manifest(pair_manifest, args.variant)

    if out_dir.exists():
        shutil.rmtree(out_dir)

    shutil.copytree(repo_dir, out_dir)
    (out_dir / ".agent-rock-benchmark.json").write_text(json.dumps(variant_manifest, indent=2) + "\n")
    (out_dir / ".agent-rock-pair.json").write_text(json.dumps(pair_manifest, indent=2) + "\n")

    if not args.skip_skills:
        copy_skills(repo_root, out_dir)

    if not args.skip_git:
        subprocess.run(["git", "init"], cwd=out_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=out_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"seed pair variant: {args.pair}/{args.variant}"],
            cwd=out_dir,
            check=True,
            capture_output=True,
        )

    print(f"Materialized {args.pair}/{args.variant} into {out_dir}")


if __name__ == "__main__":
    main()
