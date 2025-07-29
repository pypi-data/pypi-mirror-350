# src/logflow/cli.py

import argparse
from logflow import idea, idea_index, devloop, init, status, history, listing

parser = argparse.ArgumentParser(description="Logflow: Focused developer journaling and ideation loop")
subparsers = parser.add_subparsers(dest="command")

# Add command
add_parser = subparsers.add_parser("add", help="Log a new idea")
add_parser.add_argument("summary", help="Summary or idea text")
add_parser.add_argument("--title", help="Optional title to create an idea file")
add_parser.add_argument("--body", help="Optional body text")
add_parser.add_argument("--tag", help="Optional tag")

# Complete command
complete_parser = subparsers.add_parser("complete", help="Mark idea as completed")
complete_parser.add_argument("title_or_id", help="Title or ID of idea")

# Delete command
delete_parser = subparsers.add_parser("delete", help="Soft-delete idea to trash")
delete_parser.add_argument("title_or_id", help="Title or ID of idea")

# Focus command
subparsers.add_parser("focus", help="Daily check-in and task logging")

# Help command
subparsers.add_parser("help", help="Show CLI cheat sheet")

# History command
history_parser = subparsers.add_parser("history", help="Show developer task log")
history_parser.add_argument("--days", type=int, help="Limit to last N days")
history_parser.add_argument("--mode", choices=["full", "summary"], help="Display mode")  # still here for future use


# Index command
subparsers.add_parser("index", help="Show idea index")

# Init command
init_parser = subparsers.add_parser("init", help="Create visible logflow folder and config")
init_parser.add_argument("--force", action="store_true", help="Force reset of folders")

# List command
list_parser = subparsers.add_parser("list", help="List ideas by tag or status")
list_parser.add_argument("--tag", help="Filter by tag")
list_parser.add_argument("--status", help="Filter by status")

# Pause command
subparsers.add_parser("pause", help="Mark end of work session")

# Purge command
subparsers.add_parser("purge", help="Permanently delete trashed ideas")

# Recent command
recent_parser = subparsers.add_parser("recent", help="Show recent ideas")
recent_parser.add_argument("--n", type=int, default=5, help="Number of ideas to show")

# Status command
subparsers.add_parser("status", help="Show what you're working on")

# Where command
subparsers.add_parser("where", help="Show current log base directory")

# Note command
note_parser = subparsers.add_parser("note", help="Log a dev note")
note_parser.add_argument("text", help="The note content")
note_parser.add_argument("--id", help="Optional idea ID to attach")

# Export command
export_parser = subparsers.add_parser("export", help="Export idea summary as markdown or CSV")
export_parser.add_argument("--tag", help="Filter by tag")
export_parser.add_argument("--status", default="Active", help="Filter by status")
export_parser.add_argument("--format", choices=["table", "csv"], default="table", help="Output format")
export_parser.add_argument("--output", help="Output file (or omit for stdout)")



def main():
    """Parse CLI arguments and dispatch the appropriate Logflow command."""
    args = parser.parse_args()
    
    if args.command == "add":
        idea.log(args.summary, args.title, args.body, args.tag)
    elif args.command == "export":
        from logflow import export
        export.export_ideas(tag=args.tag, status=args.status, fmt=args.format, output=args.output)
    elif args.command == "note":
        from logflow import note
        note.log_note(args.text, args.id)
    elif args.command == "complete":
        idea.complete(args.title_or_id)
    elif args.command == "delete":
        idea.delete(args.title_or_id)
    elif args.command == "focus":
        devloop.run_focus()
    elif args.command == "help":
        print("""
📘 Logflow CLI Cheat Sheet:

logflow add "Idea text"            # Quick log
logflow add "Summary" --title T --body B --tag TAG

logflow recent                     # Show recent log entries
logflow index                      # Show full index of expanded ideas
logflow list --tag TAG             # Filter ideas by tag
logflow list --status completed    # Filter ideas by status

logflow complete 007               # Mark idea as completed
logflow delete idea_slug_or_id     # Move to trash
logflow purge                      # Permanently delete trash

logflow focus                      # Start dev session
logflow init                       # Create logflow folder and config
logflow where                      # Show base folder

logflow status                     # What are you working on?
logflow pause                      # Mark end of session
logflow history --mode summary     # View daily logs
        """)
    elif args.command == "history":
        history.show_history(days=args.days or 1) 
    elif args.command == "index":
        idea_index.show()
    elif args.command == "init":
        init.initialize_logflow(force=args.force)
    elif args.command == "list":
        listing.list_ideas(tag=args.tag, status=args.status)
    elif args.command == "pause":
        status.log_pause()
    elif args.command == "purge":
        idea.purge_trashed_ideas()
    elif args.command == "recent":
        idea.show_recent(args.n)
    elif args.command == "status":
        status.show_current_status()
    elif args.command == "where":
        from logflow.paths import get_base
        print(f"📂 Active log directory: {get_base()}")
