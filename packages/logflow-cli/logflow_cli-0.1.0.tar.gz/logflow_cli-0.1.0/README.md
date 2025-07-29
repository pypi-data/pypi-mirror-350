# README.md

# Logflow

A focused developer journaling and ideation loop.

## 🛠️ Features

- `logflow add` — Quick ideas or structured logs with title/body/tag
- `logflow focus` — Daily check-in: view recent ideas + start a task
- `logflow history` — See what you worked on and when
- `logflow index` — Lists all structured ideas
- `logflow complete` / `delete` / `purge` — Mark ideas as done or clean up
- `logflow pause` — Mark end of session
- `logflow status` — Show currently active task + time elapsed
- `logflow init` — Generate config.toml and folder structure
- `logflow help` — Built-in command cheat sheet

---

## 📦 Installation

This is a standalone CLI tool. You can install it via Poetry (or eventually PyPI):

```bash
poetry install
poetry run logflow help
```

---

## 🧠 How Logflow Stores Data

By default, Logflow stores data under:
```bash
~/.logflow/
```
This includes:
- `daily_logs/` – your developer logs
- `idea_log.md` – list of quick thoughts
- `ideas/` – structured .md files

You can customize this in **two ways**:

### 1. 🔧 Use `LOGFLOW_HOME`
Set a different base directory for all logs:
```bash
export LOGFLOW_HOME=/my/project/logflow_data
```

This makes all logs project-specific.


### 2. 📝 Use `config.toml`
Inside your `LOGFLOW_HOME` or `~/.logflow/`, add:
```toml
[paths]
log_dir = "/path/to/logs/folder"

[other]
scan_root = "parent"
max_recent_ideas = 5
```

This overrides even the environment variable and lets you split config from data.

To generate this file:
```bash
logflow init
```
Or forcibly regenerate:
```bash
logflow init --force
```

---

## 💡 Use Cases

- Solo dev journaling
- Idea tracking across projects
- Developer time tracking & status reporting
- Task queue for future sprints

---

## 📘 Command Cheat Sheet

```bash
logflow add "Idea"               # Quick log
logflow add "X" --title T --body B --tag TAG

logflow recent                   # Show recent ideas
logflow index                    # Structured idea index

logflow focus                    # Start dev work
logflow status                   # What am I working on?
logflow pause                    # Mark break/end of session

logflow complete 007             # Mark done
logflow delete slug_or_id        # Soft delete
logflow purge                    # Trash cleanup

logflow history --summary        # View logs
logflow init --force             # Regenerate config & folders
logflow help                     # Command list
```

---

## 🎯 Philosophy

Logflow is designed to:
- Work with or without Git
- Require zero setup, but allow full config
- Help developers reflect, prioritize, and focus

It's built for long-term sustainability of developer thought.

---


## 🚀 Optional Features

Logflow works out of the box with no dependencies, but you can enhance it with optional extras:

### 🌈 Rich Console UI
Improves CLI output with colors, tables, and interactive prompts.

```bash
poetry install --with rich
```

### ✨ Fancy Slug Support
Generates cleaner slugs for filenames, with support for emojis, accents, and non-ASCII characters.

```bash
poetry install --with fancy_slugs
```

### 🧩 Combine Extras
Install both optional features together:

```bash
poetry install --with rich,fancy_slugs
```

These extras are defined in your `pyproject.toml`:

```toml
[tool.poetry.extras]
rich = ["rich"]
fancy_slugs = ["python-slugify"]
```


## 🔓 License
MIT

---

### 📣 Maintained by [Oravox LLC](mailto:oravoxco@gmail.com) — freely available for solo devs, teams, and contributors.
