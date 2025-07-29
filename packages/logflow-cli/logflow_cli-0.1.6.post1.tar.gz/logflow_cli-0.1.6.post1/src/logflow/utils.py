# src/logflow/utils.py

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None


def printx(msg: str):
    if console:
        console.print(msg)
    else:
        print(msg)
