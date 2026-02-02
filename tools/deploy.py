from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()


def _root() -> Path:
    # This file lives at <root>/tools/deploy.py
    return Path(__file__).resolve().parents[1]


def _run(cmd: list[str], cwd: Path) -> None:
    console.print(f"[bold]$[/bold] (cwd={cwd}) {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd), check=True)


def _hugo_bin() -> Path:
    # Prefer the project-pinned Hugo binary if present.
    return _root() / ".bin" / "hugo"


@app.command()
def build(
    minify: bool = True,
    gc: bool = True,
) -> None:
    """
    Build the site into academic-kickstart/public/ (the GitHub Pages repo submodule).
    """
    ak = _root()
    hugo = _hugo_bin()
    if not hugo.exists():
        raise typer.Exit(
            code=2,
            message=(
                "Missing Hugo binary at .bin/hugo.\n"
                "If you haven't already, download Hugo (v0.66.0 extended) like:\n"
                "  cd academic-kickstart\n"
                "  mkdir -p .bin\n"
                "  curl -fL \"https://github.com/gohugoio/hugo/releases/download/v0.66.0/"
                "hugo_extended_0.66.0_macOS-64bit.tar.gz\" -o .bin/hugo.tar.gz\n"
                "  tar -xzf .bin/hugo.tar.gz -C .bin\n"
                "  chmod +x .bin/hugo\n"
            ),
        )

    cmd = [str(hugo)]
    if gc:
        cmd.append("--gc")
    if minify:
        cmd.append("--minify")

    _run(cmd, cwd=ak)


@app.command()
def commit_public(message: str = "Rebuild site") -> None:
    """
    Commit the generated site changes inside academic-kickstart/public/.
    """
    public = _root() / "public"
    _run(["git", "add", "-A"], cwd=public)
    _run(["git", "commit", "-m", message], cwd=public)


@app.command()
def push_public(branch: str = "master") -> None:
    """
    Push the current public/ HEAD commit to the GitHub Pages repo branch.

    Note: This requires GitHub authentication to be configured in YOUR shell.
    """
    public = _root() / "public"
    _run(["git", "push", "origin", f"HEAD:{branch}"], cwd=public)


@app.command()
def deploy(message: str = "Rebuild site", branch: str = "master") -> None:
    """
    Build, commit, and push in one go.
    """
    build()
    commit_public(message=message)
    push_public(branch=branch)


if __name__ == "__main__":
    # Allow running without `python -m`.
    os.environ.setdefault("PYTHONUTF8", "1")
    try:
        app()
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Command failed[/red]: {e}")
        sys.exit(e.returncode)
