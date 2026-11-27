#!/usr/bin/env python3
"""Mirror only the public site/ directory to a GitHub Pages repository."""

import argparse
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DEFAULT_REMOTE = "git@github.com:kenost/the-darkstar.git"
DEFAULT_CHECKOUT = Path.home() / ".local/state/the-darkstar/pages-checkout"


def run(*command, cwd=None, capture=False):
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"
    return subprocess.run(command, cwd=cwd, env=env, check=True,
                          text=True, capture_output=capture)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", default=os.getenv("DARKSTAR_PAGES_REMOTE", DEFAULT_REMOTE))
    parser.add_argument("--checkout", type=Path, default=Path(os.getenv("DARKSTAR_PAGES_CHECKOUT", DEFAULT_CHECKOUT)))
    args = parser.parse_args()

    if not (SITE / "index.html").is_file() or not (SITE / "issues").is_dir():
        raise RuntimeError("A complete generated site is required before deployment")
    if any(path.is_symlink() for path in SITE.rglob("*")):
        raise RuntimeError("Refusing to publish symlinks from the static site")
    checkout = args.checkout.expanduser().resolve()
    checkout.parent.mkdir(parents=True, exist_ok=True)
    if not (checkout / ".git").is_dir():
        if checkout.exists() and any(checkout.iterdir()):
            raise RuntimeError(f"Checkout path is not an empty directory: {checkout}")
        run("git", "clone", args.remote, str(checkout))
    actual = run("git", "remote", "get-url", "origin", cwd=checkout, capture=True).stdout.strip()
    if actual != args.remote:
        raise RuntimeError(f"Refusing to use checkout with different origin: {actual}")

    run("git", "fetch", "origin", cwd=checkout)
    remote_main = run("git", "ls-remote", "--heads", "origin", "main", cwd=checkout,
                      capture=True).stdout.strip()
    if remote_main:
        run("git", "checkout", "-B", "main", "origin/main", cwd=checkout)
    else:
        run("git", "checkout", "-B", "main", cwd=checkout)
    run("rsync", "-a", "--delete", "--exclude=.git", f"{SITE}/", f"{checkout}/")
    run("git", "add", "-A", cwd=checkout)
    changed = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=checkout).returncode
    if changed == 0:
        print("Pages repository already matches the current edition")
        return
    if changed != 1:
        raise RuntimeError("Could not inspect staged static-site changes")
    run("git", "-c", "user.name=The Darkstar", "-c", "user.email=kenost@users.noreply.github.com",
        "commit", "-m", f"Publish {sorted((SITE / 'issues').iterdir())[-1].name}", cwd=checkout)
    run("git", "push", "origin", "main", cwd=checkout)
    print("Pushed the complete public archive to GitHub Pages source branch")


if __name__ == "__main__":
    main()
