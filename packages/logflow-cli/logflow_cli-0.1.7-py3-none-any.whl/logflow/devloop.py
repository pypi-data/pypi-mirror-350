# src/logflow/devloop.py

import shlex
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
from logflow.utils import printx
from logflow.paths import get_base, load_config, get_repo_root
from logflow.idea import log as log_idea

try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt
    console = Console()
except ImportError:
    console = None



def parse_focus_input(text):
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", nargs="?")
    parser.add_argument("--title")
    parser.add_argument("--tag", nargs="+")
    try:
        args, _ = parser.parse_known_args(shlex.split(text))
        return args.summary or args.title, args.title, None, args.tag
    except Exception:
        return text.strip(), None, None, []


def show_indexed_recent_ideas(n: int = 5):
    """Display the most recent N non-deleted, non-completed idea titles from the idea folder."""
    idea_dir = get_base() / "ideas"
    files = sorted(idea_dir.glob("*.md"))
    recent = []
    for file in reversed(files):
        with file.open() as f:
            lines = f.readlines()
            status_line = next((line for line in lines if line.lower().startswith("status:")), None)
            if status_line and ("completed" in status_line.lower() or "deleted" in status_line.lower()):
                continue
            title_line = next((line for line in lines if line.strip().startswith("# ")), None)
            if title_line:
                idea_id = file.stem.split("_")[0]
                title = title_line.strip("# \n")
                recent.append((idea_id, title))
        if len(recent) >= n:
            break

    header = "[bold green]📝 Recent Ideas:[/bold green]" if console else "\n📝 Recent Ideas:"
    printx(header)
    for idea_id, title in recent:
        printx(f"- [{idea_id}] {title}")


def show_git_status():
    """Scan all Git repos under the configured root and display their working directory status."""
    from logflow.paths import get_repo_root, load_config
    REPO_ROOT = get_repo_root()
    CONFIG = load_config()

    if CONFIG.get("scan_git", True) is False:
        return

    git_repos = []
    for path in REPO_ROOT.rglob(".git"):
        repo = path.parent
        if repo.is_dir():
            git_repos.append(repo)

    printx(f"[cyan]🔍 Scanning repos under: {REPO_ROOT}[/cyan]" if console else f"🔍 Scanning repos under: {REPO_ROOT}")

    if console:
        table = Table(title="📁 Repo Status", show_lines=True)
        table.add_column("Repo")
        table.add_column("Status")
    else:
        printx("\n📁 Repo Status:")

    for repo in sorted(git_repos):
        try:
            result = subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True)
            status = "✅ Clean" if result.stdout.strip() == "" else "🟡 Uncommitted changes"
        except Exception:
            status = "❌ Not a git repo"

        name = repo.relative_to(REPO_ROOT)
        if console:
            table.add_row(str(name), status)
        else:
            printx(f"{name}: {status}")

    if console:
        console.print(table)


def log_focus_task(task: str):
    """Append the active task to today's daily log with a timestamp."""
    log_dir = get_base() / "daily_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{datetime.now().date()}.md"
    timestamp = datetime.now().strftime("%H:%M")
    with log_path.open("a") as f:
        f.write(f"- [{timestamp}] working on {task}\n")
    printx(f"\n✅ Logged: working on {task} → {log_path}")


def resolve_task_input(input_str: str) -> str:
    """Resolve a user-provided input to an idea title, using idea ID or raw text."""
    trimmed = input_str.strip()
    if trimmed.isdigit():
        prefix = f"{int(trimmed):03d}"
        for file in (get_base() / "ideas").glob(f"{prefix}_*.md"):
            with file.open() as f:
                for line in f:
                    if line.strip().startswith("# "):
                        return line.strip().lstrip("# ")
        return ""  # idea not found
    return trimmed


def run_focus():
    """Main interactive loop for daily focus session: shows status, asks user for task, logs it."""
    intro = "[bold blue]🧠 Logflow Focus Mode[/bold blue]" if console else "\n🧠 Logflow Focus Mode"
    printx(intro)

    show_git_status()
    from logflow.paths import load_config
    CONFIG = load_config()
    show_indexed_recent_ideas(n=CONFIG.get("max_recent_ideas", 5))


    prompt_msg = "[bold]What are you working on?[/bold]" if console else "\nWhat are you working on today?"
    printx(prompt_msg)

    if console:
        user_input = Prompt.ask("Enter a short task description (or idea #, leave blank to log 'status check')")
    else:
        user_input = input("Enter a short task description (or idea #, leave blank to log 'status check'): ")

    task_input = user_input.strip()
    if not task_input:
        task = "status check"
    else:
        # 👇 Parse inline --title and --tag from user input
        summary, title, body, tags = parse_focus_input(task_input)

        from logflow.idea import log
        idea_file = log(summary, title=title, body=body, tags=tags)
        task = title or summary


    log_focus_task(task)
    printx(f"🧠 Focused on: {task}")

