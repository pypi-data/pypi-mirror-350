# src/logflow/init.py

from pathlib import Path
import shutil
import os
from logflow.paths import get_base


def initialize_logflow(force=False):
    base = Path.cwd() / "logflow"

    if force and base.exists():
        shutil.rmtree(base)

    (base / "ideas" / "completed").mkdir(parents=True, exist_ok=True)
    (base / "ideas" / "trash").mkdir(parents=True, exist_ok=True)
    (base / "daily_logs").mkdir(parents=True, exist_ok=True)

    (base / "idea_log.md").touch()
    (base / "completed_log.md").touch()

    if not (base / "next_id.txt").exists():
        (base / "next_id.txt").write_text("1\n")

    config_path = base / "config.toml"
    if not config_path.exists() or force:
        config_path.write_text(f"""
[paths]
log_dir = "{base}"

[other]
scan_root = "parent"
max_recent_ideas = 5
""")



    print(f"✅ Logflow initialized in {base}")
    print("Created:")
    print("- idea_log.md")
    print("- completed_log.md")
    print("- next_id.txt")
    print("- config.toml")
    print("You can customize settings in config.toml\n")
