from datetime import datetime
from pathlib import Path
import shutil
import re
import os
import hashlib

from logflow import idea_index
from logflow.utils import printx
from logflow.paths import get_base
from logflow.idea_utils import set_status, get_status

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None

def ensure_dirs():
    base = get_base()
    (base / "ideas" / "completed").mkdir(parents=True, exist_ok=True)
    (base / "ideas" / "trash").mkdir(parents=True, exist_ok=True)
    (base / "daily_logs").mkdir(parents=True, exist_ok=True)
    (base / "idea_log.md").touch(exist_ok=True)
    (base / "completed_log.md").touch(exist_ok=True)
    (base / "next_id.txt").touch(exist_ok=True)

def find_next_available_id():
    base = get_base()
    ideas_dir = base / "ideas"
    used_ids = set()
    for file in ideas_dir.glob("*.md"):
        try:
            id_str = file.stem.split("_")[0]
            used_ids.add(int(id_str))
        except (IndexError, ValueError):
            continue

    current_id = 1
    while current_id in used_ids:
        current_id += 1
    return current_id

def get_next_id():
    base = get_base()
    path = base / "next_id.txt"
    if not path.exists():
        path.write_text("1")
    next_id = find_next_available_id()
    path.write_text(str(next_id + 1))
    return next_id

def slugify(text: str) -> str:
    try:
        from slugify import slugify as std_slugify
        return std_slugify(text)[:40]
    except ImportError:
        slug = re.sub(r'\W+', '_', text.strip().lower())
        return slug.strip("_")[:40]

def compute_hash(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:6]

def log(summary: str, title: str = "", body: str = "", tag: str = ""):
    ensure_dirs()
    base = get_base()
    now = datetime.now()
    timestamp = now.strftime("[%Y-%m-%d %H:%M]")
    tag_str = f" [{tag}]" if tag else ""
    with (base / "idea_log.md").open("a") as f:
        f.write(f"{timestamp}{tag_str} {summary}\n")

    printx(f"✅ Logged: {summary} → {base / 'idea_log.md'}")

    idea_id = get_next_id()
    id_prefix = f"{idea_id:03d}" if idea_id < 1000 else str(idea_id)
    slug = slugify(title or summary)
    filename = f"{id_prefix}_{slug}.md"
    path = base / "ideas" / filename

    hash_str = compute_hash(f"{title}{summary}{body}")

    with path.open("w") as f:
        f.write(f"# {title or summary}\n\n")
        if tag:
            f.write(f"Tags: {tag}\n")
        f.write(f"Created: {now.isoformat()}\n")
        f.write(f"Hash: {hash_str}\n")
        f.write(f"Status: Active\n")
        f.write(f"Priority: normal\n")
        f.write(f"Origin: manual\n\n")
        f.write("---\n\n")
        f.write(f"{summary}\n\n")
        if body:
            f.write("---\n\n")
            f.write(f"{body}\n")

    printx(f"📄 Created: {filename}")
    return path

def complete(identifier: str):
    ensure_dirs()
    base = get_base()
    ideas_dir = base / "ideas"
    completed_dir = ideas_dir / "completed"

    ident = identifier.strip().lower()
    if ident.isdigit():
        ident = f"{int(ident):03d}"

    active_candidates = list(ideas_dir.glob(f"{ident}*.md"))
    if active_candidates:
        path = active_candidates[0]
        set_status(path, "Completed")
        shutil.move(str(path), completed_dir / path.name)
        printx(f"✅ Moved and marked as completed: {path.name}")
        idea_index.generate()
        return

    completed_candidates = list(completed_dir.glob(f"{ident}*.md"))
    if completed_candidates:
        printx(f"⚠️ Idea '{identifier}' is already marked as completed.")
        return

    printx(f"❌ No matching idea found for '{identifier}'")

def delete(identifier: str):
    ensure_dirs()
    base = get_base()
    ideas_dir = base / "ideas"
    completed_dir = ideas_dir / "completed"
    trash_dir = ideas_dir / "trash"

    ident = identifier.strip().lower()
    if ident.isdigit():
        ident = f"{int(ident):03d}"

    candidates = (
        list(ideas_dir.glob(f"{ident}*.md")) +
        list(completed_dir.glob(f"{ident}*.md"))
    )

    if not candidates:
        printx(f"❌ No matching idea found for '{identifier}'")
        return

    path = candidates[0]
    set_status(path, "Deleted")
    shutil.move(str(path), trash_dir / path.name)
    idea_index.generate()

    printx(f"🗑️ Moved to trash: {path.name}")

def purge_trash():
    base = get_base()
    trash_dir = base / "ideas" / "trash"
    if not trash_dir.exists():
        printx("❌ Trash folder does not exist.")
        return

    for file in trash_dir.glob("*.md"):
        file.unlink()
    printx("🧹 Trash purged.")

def show_recent(n=5):
    ensure_dirs()
    base = get_base()
    log_path = base / "idea_log.md"
    idea_dir = base / "ideas"

    if log_path.exists():
        header = "\n📝 Last Logged Ideas:" if not console else "\n[bold green]📝 Last Logged Ideas:[/bold green]"
        print(header) if not console else console.print(header)
        lines = log_path.read_text().strip().splitlines()

        for line in lines[-n:]:
            match = re.match(r"^(\[.*?\])(?: \[.*\])? (.*)$", line)
            ts, summary = match.groups() if match else ("", line)
            found_id = ""
            for file in idea_dir.glob("*.md"):
                title = file.read_text().split("\n", 1)[0].lstrip("# ").strip().lower()
                if title.startswith(summary.strip().lower()[:20]):
                    found_id = file.stem.split("_")[0]
                    break
            out = f"{ts} [{found_id}] {summary}" if found_id else line
            print(f"- {out}") if not console else console.print(f"- {out}")
    else:
        print("No idea log found.") if not console else console.print("[red]No idea log found.[/red]")