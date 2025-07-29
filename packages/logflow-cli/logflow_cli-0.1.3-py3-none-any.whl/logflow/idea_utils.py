from pathlib import Path

def parse_metadata(path: Path) -> dict:
    """Parse the metadata block at the top of a markdown idea file.

    Args:
        path (Path): Path to the idea .md file.

    Returns:
        dict: Metadata key-value pairs (e.g., {"Status": "Completed"}).
    """
    meta = {}
    lines = path.read_text().splitlines()
    if "---" not in lines:
        raise ValueError(f"Invalid metadata format in {path.name}: missing '---' separator.")

    for line in lines:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


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


def get_tag(path: Path) -> str:
    """Return the tag/category of the idea, or 'uncategorized' if missing.

    Args:
        path (Path): Path to the .md idea file.

    Returns:
        str: Tag string.
    """
    meta = parse_metadata(path)
    return meta.get("Tags", "uncategorized")