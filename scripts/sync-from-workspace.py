#!/usr/bin/env python3
"""
sync-from-workspace.py

Syncs portable files from kale-workspace into this project repo.

Purpose: Pull the latest company context (commands, skills, strategy, business info)
         from kale-workspace into a Tier 3 project repo, without touching
         project-specific files.
Inputs:  Optional path to kale-workspace as a command-line argument.
Outputs: Files copied into this repo; summary printed to stdout.
Env vars: None required (operates on local filesystem only).

Usage:
    python scripts/sync-from-workspace.py
    python scripts/sync-from-workspace.py ../kale-workspace

What syncs (workspace context → context/workspace/ in this repo):
    .claude/commands/  →  <this repo>/.claude/commands/
    .claude/skills/    →  <this repo>/.claude/skills/
    reference/         →  <this repo>/reference/
    .mcp.json          →  <this repo>/.mcp.json
    MCP_SETUP.md       →  <this repo>/MCP_SETUP.md
    context/business-info.md  →  context/workspace/business-info.md
    context/clients.md        →  context/workspace/clients.md
    context/team.md           →  context/workspace/team.md
    context/strategy.md       →  context/workspace/kale-strategy.md (renamed)

What does NOT sync (workspace-only):
    context/roshan.md, context/mike.md     (personal/founder-specific)
    context/current-data.md                (workspace-specific live data)
    knowledge/ contents                    (accumulated workspace knowledge)
    automations/ contents                  (workspace-specific tools)
    plans/, outputs/                       (workspace work products)

Protected files (never overwritten in this repo):
    CLAUDE.md                              (project-specific)
    For client repos, the 6 Notion-mirrored files in context/:
    overview.md, strategy.md, customer-success.md, data.md,
    reporting.md, infra.md, current-state.md

One-time cleanup (deletes deprecated synced paths):
    context/business-info.md   (moved to context/workspace/)
    context/clients.md         (moved to context/workspace/)
    context/team.md            (moved to context/workspace/)
"""

import sys
import shutil
from pathlib import Path


SYNC_DIRS = [
    ".claude/commands",
    ".claude/skills",
    "reference",
]

# Source path in workspace → target path in this repo
# Workspace context files are namespaced under context/workspace/ in tier-3 repos
SYNC_FILES = {
    ".mcp.json": ".mcp.json",
    "MCP_SETUP.md": "MCP_SETUP.md",
    "context/business-info.md": "context/workspace/business-info.md",
    "context/clients.md": "context/workspace/clients.md",
    "context/team.md": "context/workspace/team.md",
    "context/strategy.md": "context/workspace/kale-strategy.md",
}

# Project-specific files — never overwrite these.
# Client repos use these for Notion-mirrored content; non-client repos may not have them.
PROTECTED_FILES = [
    "CLAUDE.md",
    "context/overview.md",
    "context/strategy.md",
    "context/customer-success.md",
    "context/data.md",
    "context/reporting.md",
    "context/infra.md",
    "context/current-state.md",
]

# Deprecated paths to remove on first sync after the context-mirror refactor.
# Safe to delete unconditionally — their content lives at the new workspace/ path.
# NOTE: context/strategy.md is intentionally NOT in this list — in client repos it's
# the new client strategy mirror file; in non-client repos it's stale but removing it
# blindly would clobber any manual edits. Non-client repos can clean it up manually.
DEPRECATED_PATHS = [
    "context/business-info.md",
    "context/clients.md",
    "context/team.md",
    "context/arra.md",
    "context/azhar.md",
    "context/beverly.md",
    "context/pandush.md",
    "context/umer.md",
    "context/front_end_design_skill.md",
    "context/kale_knowledge_resource_building_skill.md",
    "context/project-info.md",
    "context/project-goals.md",
]


def validate_git_repo(path: Path) -> bool:
    """Check that the path is a git repository."""
    return (path / ".git").exists()


def sync_directory(src: Path, dst: Path) -> list[str]:
    """Merge workspace files into dst, preserving project-specific files. Returns list of copied paths."""
    copied = []
    if not src.exists():
        print(f"  SKIP (not found in workspace): {src.name}/")
        return copied

    dst.mkdir(parents=True, exist_ok=True)
    for f in src.rglob("*"):
        if f.is_file():
            rel = f.relative_to(src)
            dst_file = dst / rel
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst_file)
            copied.append(str(rel))
    return copied


def sync_file(src: Path, dst: Path, rel_path: str) -> bool:
    """Copy a single file from src to dst. Returns True if copied."""
    if not src.exists():
        print(f"  SKIP (not found in workspace): {rel_path}")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def cleanup_deprecated_paths(repo_path: Path) -> list[str]:
    """Remove deprecated synced paths if they exist. Returns list of removed paths."""
    removed = []
    for rel_path in DEPRECATED_PATHS:
        target = repo_path / rel_path
        if target.exists() and target.is_file():
            target.unlink()
            removed.append(rel_path)
    return removed


def main():
    if len(sys.argv) > 2:
        print("Usage: python scripts/sync-from-workspace.py [path-to-kale-workspace]")
        sys.exit(1)

    if len(sys.argv) == 2:
        workspace_path = Path(sys.argv[1]).resolve()
    else:
        workspace_path = (Path(__file__).parent.parent.parent / "kale-workspace").resolve()

    repo_path = Path(__file__).parent.parent.resolve()

    print(f"\nkale-workspace -> project repo sync")
    print(f"  Source:  {workspace_path}")
    print(f"  Target:  {repo_path}")
    print()

    if workspace_path == repo_path:
        print("ERROR: Source and destination are the same directory.")
        print("       This script must be run from a project repo, not from kale-workspace.")
        sys.exit(1)

    if not workspace_path.exists():
        print(f"ERROR: Workspace path does not exist: {workspace_path}")
        print(f"       Pass the path explicitly: python scripts/sync-from-workspace.py <path-to-kale-workspace>")
        sys.exit(1)

    if not validate_git_repo(workspace_path):
        print(f"ERROR: Workspace path is not a git repository (no .git found): {workspace_path}")
        sys.exit(1)

    copied_dirs = []
    copied_files = []
    skipped = []

    # Sync directories
    print("Syncing directories:")
    for rel_dir in SYNC_DIRS:
        src = workspace_path / rel_dir
        dst = repo_path / rel_dir
        if src.exists():
            sync_directory(src, dst)
            copied_dirs.append(rel_dir)
            print(f"  + {rel_dir}/")
        else:
            skipped.append(rel_dir)
            print(f"  - {rel_dir}/ (not found in workspace, skipped)")

    # Sync individual files (with re-routing)
    print("\nSyncing files (workspace -> repo):")
    for src_rel, dst_rel in SYNC_FILES.items():
        src = workspace_path / src_rel
        dst = repo_path / dst_rel
        if sync_file(src, dst, src_rel):
            copied_files.append(dst_rel)
            if src_rel == dst_rel:
                print(f"  + {dst_rel}")
            else:
                print(f"  + {dst_rel}  (from {src_rel})")
        else:
            skipped.append(src_rel)

    # One-time cleanup of deprecated paths
    removed = cleanup_deprecated_paths(repo_path)
    if removed:
        print("\nCleanup (deprecated paths removed):")
        for p in removed:
            print(f"  - {p}")

    # Report protected files (never touched)
    print("\nProtected files (not touched by this sync):")
    for f in PROTECTED_FILES:
        status = "exists" if (repo_path / f).exists() else "missing"
        print(f"  . {f}  [{status}]")

    print()
    print(f"Done. Synced {len(copied_dirs)} directories, {len(copied_files)} files.")
    if removed:
        print(f"Removed {len(removed)} deprecated paths.")
    if skipped:
        print(f"Skipped {len(skipped)} items (not found in workspace): {', '.join(skipped)}")
    print()
    print("Next: review changes with `git diff` and `git status`, then:")
    print('  git add -A && git commit -m "chore: sync company context from kale-workspace"')
    print("  git push")


if __name__ == "__main__":
    main()
