import subprocess
from typing import List, Dict
import os


def is_git_repo() -> bool:
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True,
            cwd=os.getcwd(),
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_recent_commits(count: int = 5) -> List[Dict[str, str]]:
    commits = []
    result = subprocess.run(
        ["git", "log", f"-{count}", "--pretty=format:%h|%s"],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if line:
            parts = line.split("|", 1)
            if len(parts) == 2:
                commits.append({"hash": parts[0], "message": parts[1]})
    return commits


def get_git_status() -> str:
    result = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_stash_list() -> List[Dict[str, str]]:
    stashes = []
    try:
        result = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.strip().split("\n")
        for line in lines:
            if line:
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    stashes.append({"id": parts[0].rstrip(":"), "message": parts[2]})
    except subprocess.CalledProcessError:
        pass
    return stashes


def get_full_context() -> Dict:
    return {
        "branch": get_current_branch(),
        "commits": get_recent_commits(),
        "status": get_git_status(),
        "stashes": get_stash_list(),
    }


def run_command(command: List[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
    )
    return result.stdout.strip()
