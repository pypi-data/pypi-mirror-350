````md
# Logflow

[![PyPI](https://img.shields.io/pypi/v/logflow-cli.svg)](https://pypi.org/project/logflow-cli/)
[![Downloads](https://static.pepy.tech/badge/logflow-cli)](https://pepy.tech/project/logflow-cli)
[![Release](https://github.com/512jay/logflow/actions/workflows/release.yml/badge.svg)](https://github.com/512jay/logflow/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[📘 Quickstart Guide](https://github.com/512jay/logflow/blob/main/docs/quickstart.md) – Learn how to install and use Logflow in minutes.


💡 **Tip:** For the best experience, install with extras:

```bash
pipx install logflow-cli[rich,slugify]
This enables rich terminal output and emoji-safe filenames.

A focused developer journaling and ideation loop.

---

## 📦 Installation (Recommended: pipx)

Logflow is a Python CLI app — install it globally without polluting your system Python:

```bash
pip install pipx
pipx ensurepath
pipx install logflow-cli
````

Then run:

```bash
logflow init
logflow help
```

---

### 🔧 Alternative (Dev Setup with Poetry)

```bash
poetry install
poetry run logflow init
poetry run logflow focus
```

---

## ✨ Optional Enhancements

Logflow works fine on its own — but these extras make it better:

* 🎨 `rich` – pretty terminal output (colors, tables)
* 🐍 `python-slugify` – better filenames (emoji and symbols allowed)

### Install with extras using pipx:

```bash
pipx install logflow-cli[rich,slugify]
```

Or with Poetry:

```bash
poetry install --extras "rich slugify"
```

---

## 🧠 How Logflow Stores Data

By default, Logflow stores data under:

```bash
~/.logflow/
```

This includes:

* `daily_logs/` – your developer logs
* `idea_log.md` – list of quick thoughts
* `ideas/` – structured .md files

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

* Solo dev journaling
* Idea tracking across projects
* Developer time tracking & status reporting
* Task queue for future sprints

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

* Work with or without Git
* Require zero setup, but allow full config
* Help developers reflect, prioritize, and focus

It's built for long-term sustainability of developer thought.

---

## 🔓 License

MIT

---

### 📣 Maintained by [Oravox LLC](mailto:oravoxco@gmail.com) — freely available for solo devs, teams, and contributors.

```

---

Let me know if you'd like:
- A PR-ready version of this
- The `quickstart.md` file scaffolded and saved
- A next-version dev checklist for `v0.1.5` planning
```


### ✨ New in v0.1.5

#### `logflow export`
Export your backlog or roadmap to a markdown table or CSV file.

```bash
logflow export --tag internal --format table
logflow export --format csv --output backlog.csv
```

#### `logflow note`
Log mid-task notes to the daily log, and optionally append them to an idea file.

```bash
logflow note "Clarified export logic"
logflow note "Linked to issue" --id 002
```

#### YAML Frontmatter Metadata
All idea files now include structured frontmatter:

```yaml
---
ID: 002
Title: Export feature
Tags: internal
Status: Active
Created: 2025-05-22 20:58
---
```