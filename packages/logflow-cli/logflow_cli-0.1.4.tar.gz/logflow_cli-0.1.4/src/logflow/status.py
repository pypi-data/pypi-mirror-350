# src/logflow/status.py

from datetime import datetime
from pathlib import Path
import os
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
        msg = "No log entries found."
        print(msg) if not console else console.print(f"[yellow]{msg}[/yellow]")
        return

    log_files = sorted(log_dir.glob("*.md"), reverse=True)
    entries = []

    for path in log_files:
        lines = list(reversed(path.read_text().splitlines()))
        for line in lines:
            if "paused session" in line.lower():
                msg = f"💤 No active task. Last session paused at {path.name[:10]}"
                print(msg) if not console else console.print(f"[yellow]{msg}[/yellow]")
                return
            match = re.match(r"- \[(\d{2}:\d{2})\] working on (.*)", line)
            if match:
                time, task = match.groups()
                if task.lower().strip() == "status check":
                    continue
                started = datetime.strptime(time, "%H:%M")
                now = datetime.now()
                elapsed = now - now.replace(hour=started.hour, minute=started.minute, second=0, microsecond=0)
                mins = elapsed.total_seconds() // 60

                if console:
                    console.print(f"\n[bold green]🔄 Currently working on:[/bold green] {task}")
                    console.print(f"⏱️ Started at: {time}  (about {int(mins)} minutes ago)\n")
                else:
                    print(f"\n🔄 Currently working on: {task}")
                    print(f"⏱️ Started at: {time}  (about {int(mins)} minutes ago)\n")
                return

    msg = "No active tasks found."
    print(msg) if not console else console.print(f"[yellow]{msg}[/yellow]")

def log_pause():
    log_dir = get_base() / "daily_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{datetime.now().date()}.md"
    timestamp = datetime.now().strftime("%H:%M")
    with log_path.open("a") as f:
        f.write(f"- [{timestamp}] paused session\n")

    msg = f"✅ Paused session at {timestamp} → {log_path}"
    print(msg) if not console else console.print(f"[green]{msg}[/green]")