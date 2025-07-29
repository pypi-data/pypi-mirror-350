# src/logflow/history.py

from datetime import datetime, timedelta
from pathlib import Path
import os
import re
from logflow.paths import get_base

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


def parse_log_line(line):
    match = re.match(r"- \[(.*?)\] (.*)", line)
    if match:
        return match.groups()
    return None, line


def show_history(days=1, since=None, idea=None):
    base = get_base() / "daily_logs"
    cutoff = None
    if since:
        cutoff = datetime.strptime(since, "%Y-%m-%d").date()
    elif days:
        cutoff = datetime.today().date() - timedelta(days=days-1)

    all_logs = sorted(base.glob("*.md"))
    if not all_logs:
        print("No logs found.")
        return

    if console:
        table = Table(title=f"📅 Developer Log — Last {days} Days")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Task")
    else:
        print(f"\n📅 Developer Log — Last {days} Days\n")

    for path in all_logs:
        date_str = path.stem
        log_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if cutoff and log_date < cutoff:
            continue

        for line in path.read_text().splitlines():
            timestamp, task = parse_log_line(line)
            if not timestamp:
                continue
            if idea and idea not in task:
                continue

            if console:
                table.add_row(date_str, timestamp, task)
            else:
                print(f"[{date_str}] {timestamp} - {task}")

    if console:
        console.print(table)
