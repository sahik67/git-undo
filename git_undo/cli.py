import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.status import Status
from typing import List
import subprocess
import sys
from .git import is_git_repo, get_full_context
from .ai import generate_commands

app = typer.Typer(
    name="git-undo",
    help="Fix Git mistakes using natural language",
    add_completion=False,
)
console = Console()


DESTRUCTIVE_PATTERNS = [
    "git push --force",
    "git reset --hard",
    "git branch -D",
    "git rebase --abort",
    "git clean -f",
    "git clean -fd",
    "git reflog delete",
]


def is_destructive(command: str) -> bool:
    lower_command = command.lower()
    for pattern in DESTRUCTIVE_PATTERNS:
        if pattern in lower_command:
            return True
    return False


def execute_command(command: str):
    args = command.split()
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    for line in process.stdout:
        console.print(line, end="")
    process.wait()
    if process.returncode != 0:
        console.print(f"\n[red]Command failed with exit code {process.returncode}[/red]")
        sys.exit(1)


@app.command()
def main(
    mistake: List[str] = typer.Argument(..., help="Describe your Git mistake in plain English"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Preview commands without executing them"),
):
    mistake_text = " ".join(mistake)
    
    if not is_git_repo():
        console.print(
            Panel(
                Text("Error: Not a Git repository!", style="bold red"),
                title="Git Error",
                border_style="red"
            )
        )
        raise typer.Exit(1)
        
    with Status("Collecting Git repository context...", spinner="dots"):
        git_context = get_full_context()
        
    with Status("Analyzing mistake and generating commands...", spinner="dots"):
        try:
            commands = generate_commands(mistake_text, git_context)
        except ValueError as e:
            console.print(
                Panel(
                    Text(str(e), style="bold red"),
                    title="Configuration Error",
                    border_style="red"
                )
            )
            raise typer.Exit(1)
        except Exception as e:
            console.print(
                Panel(
                    Text(f"API Error: {str(e)}", style="bold red"),
                    title="API Error",
                    border_style="red"
                )
            )
            raise typer.Exit(1)
            
    console.print("\n[bold green]Suggested Commands:[/bold green]\n")
    has_destructive = False
    
    for idx, cmd in enumerate(commands, 1):
        is_danger = is_destructive(cmd["command"])
        if is_danger:
            has_destructive = True
            
        if is_danger:
            panel_title = f"⚠️  Command {idx} (DESTRUCTIVE)"
            panel_border = "red"
        else:
            panel_title = f"Command {idx}"
            panel_border = "green"
            
        console.print(
            Panel(
                Syntax(cmd["command"], "bash", theme="monokai", line_numbers=False),
                title=panel_title,
                border_style=panel_border
            )
        )
        console.print(f"[dim]{cmd['explanation']}[/dim]\n")
        
    if has_destructive:
        console.print(
            Panel(
                Text(
                    "⚠️  WARNING: One or more commands are destructive and may result in data loss!",
                    style="bold red"
                ),
                title="Destructive Commands Detected",
                border_style="red"
            )
        )
        
    if dry_run:
        console.print("\n[yellow]Dry run complete - no commands executed[/yellow]")
        return
        
    confirm = typer.confirm("Do you want to execute these commands?", default=False)
    if not confirm:
        console.print("[yellow]Aborted - no commands executed[/yellow]")
        return
        
    console.print("\n[bold]Executing commands...[/bold]\n")
    for cmd in commands:
        console.print(f"[blue]$[/blue] {cmd['command']}")
        execute_command(cmd["command"])
        console.print()
        
    console.print("[bold green]All commands executed successfully![/bold green]")


if __name__ == "__main__":
    app()
