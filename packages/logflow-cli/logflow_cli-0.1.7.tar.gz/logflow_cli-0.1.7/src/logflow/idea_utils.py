# src/logflow/utils/idea_utils.py

import re
import warnings
from pathlib import Path
import yaml

# Try to import the correct slugify
try:
    from slugify import slugify as real_slugify 

    # Reject legacy slugify==0.0.1 which has no `__version__`
    if not hasattr(real_slugify, "__call__"):
        raise ImportError("Incompatible 'slugify' package detected.")

    slugify = real_slugify

except ImportError:
    warnings.warn(
        "python-slugify not found or incompatible 'slugify' installed. Falling back to basic slugifier.",
        RuntimeWarning
    )

    def slugify(value: str) -> str:
        # Fallback: lowercase, replace non-alphanumeric with hyphen
        value = re.sub(r"[^\w\s-]", "", value).strip().lower()
        return re.sub(r"[-\s]+", "-", value)

def parse_metadata(path):
    meta = {}
    in_block = False
    lines = []
    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if line == "---":
                if not in_block:
                    in_block = True
                    continue
                else:
                    break
            if in_block:
                lines.append(line)

    try:
        parsed = yaml.safe_load("\n".join(lines)) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in metadata block: {e}")

    # Normalize legacy string tags to list
    tags = parsed.get("Tags")
    if isinstance(tags, str):
        parsed["Tags"] = [tags]

    return {
        "id": str(parsed.get("ID", "?")),
        "title": parsed.get("Title", "Untitled"),
        "status": parsed.get("Status", ""),
        "tags": parsed.get("Tags", []),
    }


def write_metadata_block(path, metadata):
    # Dump frontmatter as proper YAML
    content = ["---"]
    content.append(yaml.safe_dump(metadata, sort_keys=False).strip())
    content.append("---")
    body = path.read_text().split("---", 2)[-1].strip()
    path.write_text("\n".join(content) + "\n\n" + body)


def get_tag(path):
    return parse_metadata(path).get("tags", [])

def update_metadata(path: Path, key: str, value: str):
    """Update or insert a metadata field in the markdown file header.

    Args:
        path (Path): Path to the .md file.
        key (str): Metadata key (e.g., 'Status').
        value (str): New value (e.g., 'Completed').
    """
    key = key.capitalize()
    value = value.capitalize() if key in {"Status", "Priority", "Origin"} else value

    lines = path.read_text().splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            break
        if line.lower().startswith(f"{key.lower()}:"):
            lines[i] = f"{key}: {value}"
            updated = True
            break

    if not updated:
        for i, line in enumerate(lines):
            if line.strip() == "---":
                lines.insert(i, f"{key}: {value}")
                break

    path.write_text("\n".join(lines))


def get_status(path: Path) -> str:
    """Return the current Status value from the metadata block.

    Args:
        path (Path): Path to the .md idea file.

    Returns:
        str: Status field value, or 'Unknown' if not found.
    """
    meta = parse_metadata(path)
    return meta.get("Status", "Unknown")


def set_status(path: Path, status: str):
    """Set the Status field of the idea file to the given value.

    Args:
        path (Path): Path to the idea file.
        status (str): New status value (e.g., 'Completed').
    """
    update_metadata(path, "Status", status)


def get_metadata(path: Path) -> dict:
    """Get all metadata fields from the idea file.

    Args:
        path (Path): Path to the .md idea file.

    Returns:
        dict: All top-level metadata as a dictionary.
    """
    return parse_metadata(path)


def get_tag(path: Path) -> list:
    """Return the list of tags from the metadata block.

    Args:
        path (Path): Path to the .md idea file.

    Returns:
        list: Tag list, or empty list if missing.
    """
    return parse_metadata(path).get("tags", [])
