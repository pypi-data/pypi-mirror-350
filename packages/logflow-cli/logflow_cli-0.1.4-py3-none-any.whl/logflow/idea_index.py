# src/logflow/idea_index.py

from pathlib import Path
from collections import defaultdict
from logflow.paths import get_base
from logflow.utils import printx
from logflow.idea_utils import get_status

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None


def extract_tag_and_title(filepath: Path):
    tag = "Uncategorized"
    title = filepath.stem.replace("_", " ").title()

    with filepath.open() as f:
        for line in f:
            if line.lower().startswith("tags:"):
                tag = line.strip().split(":", 1)[1].strip().lower()
            elif line.strip().startswith("# "):
                title = line.strip().lstrip("# ").strip()
    return tag, title


def generate():
    base = get_base()
    idea_dir = base / "ideas"
    index_file = base / "idea_index.md"

    tag_groups = defaultdict(list)
    for f in sorted(idea_dir.glob("*.md")):
        tag, title = extract_tag_and_title(f)
        id_part = f.stem.split("_")[0]
        tag_groups[tag].append((id_part, title, f.relative_to(base)))

    with index_file.open("w") as index:
        index.write("# 🧠 Idea Index\n\n")
        for tag in sorted(tag_groups.keys()):
            index.write(f"## 🏷️ {tag.title()}\n\n")
            for idea_id, title, rel_path in tag_groups[tag]:
                index.write(f"- [{idea_id} {title}]({rel_path.as_posix()})\n")
            index.write("\n")


def show():
    generate()
    base = get_base()
    index_file = base / "idea_index.md"
    if index_file.exists():
        printx("[bold blue]📚 Idea Index:[/bold blue]" if console else "\n📚 Idea Index:")
        printx(index_file.read_text())
    else:
        printx("[red]No index file found.[/red]" if console else "No index file found.")
