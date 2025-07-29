# src/logflow/status.py

from datetime import datetime
from pathlib import Path
import re
from logflow.paths import get_base

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None


def show_current_status():
    base = get_base()
    log_dir = base / "daily_logs"
    if not log_dir.exists():
        _print("No log entries found.", level="warn")
        return

    log_files = sorted(log_dir.glob("*.md"), reverse=True)
    for path in log_files:
        lines = list(reversed(path.read_text().splitlines()))
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "paused session" in line.lower():
                _print(f"💤 No active task. Last session paused at {path.name[:10]}", level="warn")
                return
            match = re.match(r"- \[(\d{2}:\d{2})\] working on (.*)", line)
            if match:
                time, task = match.groups()
                if task.lower().strip() == "status check":
                    continue
                started = datetime.strptime(time, "%H:%M")
                now = datetime.now()
                elapsed = now - now.replace(hour=started.hour, minute=started.minute, second=0, microsecond=0)
                mins = int(elapsed.total_seconds() // 60)
                _print(f"\n🔄 Currently working on: {task}", level="info")
                _print(f"⏱️ Started at: {time}  (about {mins} minutes ago)\n", level="info")
                return

    _print("No active tasks found.", level="warn")


def log_pause():
    log_dir = get_base() / "daily_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{datetime.now().date()}.md"
    timestamp = datetime.now().strftime("%H:%M")
    with log_path.open("a") as f:
        f.write(f"- [{timestamp}] paused session\n")

    _print(f"✅ Paused session at {timestamp} → {log_path}", level="success")


def _print(msg: str, level: str = "info"):
    if console:
        styles = {
            "info": "bold green",
            "warn": "yellow",
            "success": "green"
        }
        style = styles.get(level, "white")
        console.print(f"[{style}]{msg}[/{style}]")
    else:
        print(msg)