# src/logflow/export.py

from logflow.idea_utils import parse_metadata
from logflow.paths import get_base
from logflow.utils import printx
from pathlib import Path
import csv

def export_ideas(tag=None, status="Active", fmt="table", output=None):
    """Export ideas filtered by tag and/or status to stdout or a file.

    Args:
        tag (str, optional): Filter by a single tag (case-insensitive). Default is None.
        status (str, optional): Filter by idea status. Default is "Active".
        fmt (str): Output format: 'table' or 'csv'. Default is 'table'.
        output (str, optional): Path to output file. If None, prints to stdout.
    """
    base = get_base()
    idea_dir = base / "ideas"
    ideas = []

    for file in sorted(idea_dir.glob("*.md")):
        try:
            meta = parse_metadata(file)
            tags = meta.get("tags", "").strip()
            status_value = meta.get("status", "").strip()
            title = meta.get("title", "Untitled").strip()
            idea_id = meta.get("id", "?")
        except Exception as e:
            printx(f"⚠️ Skipped {file.name}: {e}")
            continue

        tag_matches = not tag or any(tag.lower() == t.strip().lower() for t in tags.split(",") if t.strip())
        status_matches = not status or status_value.lower() == status.lower()

        if tag_matches and status_matches:
            ideas.append((idea_id, title, tags, status_value))

    if not ideas:
        printx("⚠️ No ideas matched the given filters.")
        return

    if fmt == "csv":
        lines = export_csv(ideas)
    else:
        lines = export_markdown_table(ideas)

    if output:
        Path(output).write_text("\n".join(lines))
        printx(f"✅ Exported {len(ideas)} ideas to {output}")
    else:
        printx("\n".join(lines))


def export_markdown_table(rows):
    """Convert idea rows to a markdown table.

    Args:
        rows (list): List of (id, title, tags, status) tuples.

    Returns:
        list[str]: Markdown-formatted table lines.
    """
    table = [
        "| ID  | Title                        | Tag       | Status |",
        "|-----|------------------------------|-----------|--------|"
    ]
    for row in rows:
        table.append(f"| {row[0]:<3} | {row[1][:30]:<30} | {row[2]:<9} | {row[3]} |")
    return table


def export_csv(rows):
    """Convert idea rows to CSV format.

    Args:
        rows (list): List of (id, title, tags, status) tuples.

    Returns:
        list[str]: CSV-formatted lines.
    """
    output = ["ID,Title,Tag,Status"]
    for row in rows:
        output.append(",".join(f'"{x}"' for x in row))
    return output