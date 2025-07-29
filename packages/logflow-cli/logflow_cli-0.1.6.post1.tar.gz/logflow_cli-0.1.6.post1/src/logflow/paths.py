# src/logflow/paths.py
import os
from pathlib import Path
import tomllib
import functools


@functools.lru_cache(maxsize=1)
def load_config():
    """Load and cache the Logflow configuration from config.toml, with basic validation and warnings."""
    config_path = get_base() / "config.toml"
    if not config_path.exists():
        print("⚠️  config.toml not found. Using defaults.")
        return {}

    try:
        config = tomllib.loads(config_path.read_text())
    except Exception as e:
        print(f"⚠️  Failed to parse config.toml: {e}")
        return {}

    # Basic validation
    if "paths" not in config or "log_dir" not in config["paths"]:
        print("⚠️  Warning: config.toml is missing required [paths] log_dir. Some features may not work.")
    return config



def get_base():
    # Use override for pytest environments
    if "PYTEST_CURRENT_TEST" in os.environ:
        return Path("/tmp/logflow-test")

    search_paths = [Path.cwd()] + list(Path.cwd().parents)
    for path in search_paths:
        config_path = path / "logflow" / "config.toml"
        if config_path.exists():
            try:
                config = tomllib.loads(config_path.read_text())
                log_dir = config.get("paths", {}).get("log_dir")
                if log_dir:
                    return Path(log_dir)
            except Exception:
                continue

    raise RuntimeError("No valid logflow/config.toml found. Please run `logflow init`.")


def get_repo_root():
    """Return the root folder to scan for git repos, based on scan_root config setting."""
    config = load_config()
    base = get_base()
    root_mode = config.get("scan_root", "parent")
    if root_mode == "base":
        return base.resolve()
    elif root_mode == "grandparent":
        return base.parent.parent.resolve()
    return base.parent.resolve()
