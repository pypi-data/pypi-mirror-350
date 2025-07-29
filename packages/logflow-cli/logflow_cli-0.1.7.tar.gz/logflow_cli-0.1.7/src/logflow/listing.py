# src/logflow/listing.py

from logflow.paths import get_base
from logflow.idea_utils import get_metadata
from logflow.utils import printx
from pathlib import Path


def list_ideas(tag: str = None, status: str = None):
    """List idea files with optional tag and status filtering.

    Args:
        tag (str, optional): Filter by tag.
        status (str, optional): Filter by status (Active, Completed, Deleted).
    """
    idea_dir = get_base() / "ideas"
    files = sorted(f for f in idea_dir.glob("*.md"))

    matching = []
    for f in files:
        meta = get_metadata(f)
        if tag and meta.get("Tags", "").lower() != tag.lower():
            continue
        if status and meta.get("Status", "").lower() != status.lower():
            continue
        title = f.read_text().splitlines()[0].lstrip("# ").strip()
        matching.append((f.stem.split("_")[0], title, meta.get("Tags", ""), meta.get("Status", "")))

    if not matching:
        printx("No matching ideas found.")
        return

    printx("[bold blue]🗂 Matching Ideas:[/bold blue]")
    for idea_id, title, tag_val, status_val in matching:
        printx(f"[{idea_id}] {title}  ({tag_val}, {status_val})")
