# src/logflow/note.py

from datetime import datetime
from logflow.paths import get_base
from logflow.utils import printx
from logflow.idea_utils import parse_metadata
from pathlib import Path

def log_note(text: str, idea_id: str = None):
    """Log a development note to today's daily log, and optionally to an idea file.

    If an idea ID is provided, the note is also appended to the corresponding
    idea markdown file under a `## Notes` section.

    Args:
        text (str): The body of the note to be logged.
        idea_id (str, optional): Optional idea ID to associate the note with.
            If provided, the note will be added to the corresponding idea file.

    Example:
        log_note("Clarified export logic")
        log_note("Refactored status block", idea_id="003")
    """
    base = get_base()
    now = datetime.now()
    timestamp = now.strftime("%H:%M")
    today = now.date()
    log_path = base / "daily_logs" / f"{today}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Daily log entry
    if idea_id:
        entry = f"- [{timestamp}] note ({idea_id}): {text}"
    else:
        entry = f"- [{timestamp}] note: {text}"

    with log_path.open("a") as f:
        f.write(entry + "\n")

    printx(f"📝 Logged note to {log_path}")

    # Append to idea file if ID is provided
    if idea_id:
        idea_dir = base / "ideas"
        idea_file = next((f for f in idea_dir.glob(f"{idea_id}*.md")), None)

        if idea_file and idea_file.exists():
            lines = idea_file.read_text().splitlines()
            note_block_header = "## Notes"
            timestamp_line = f"- [{today} {timestamp}] {text}"

            if note_block_header in lines:
                idx = lines.index(note_block_header)
                lines.insert(idx + 1, timestamp_line)
            else:
                lines.append("")
                lines.append(note_block_header)
                lines.append(timestamp_line)

            idea_file.write_text("\n".join(lines))
            printx(f"🧷 Also added note to {idea_file.name}")
        else:
            printx(f"⚠️ Idea file not found for ID: {idea_id}")