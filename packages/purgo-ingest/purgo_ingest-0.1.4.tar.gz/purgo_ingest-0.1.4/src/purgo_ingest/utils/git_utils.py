"""Utility functions for interacting with Git repositories."""

import asyncio
import sys
from typing import List, Tuple

# Import Windows-specific helper functions if on Windows
if sys.platform == 'win32':
    from purgo_ingest.utils.windows_helper import (
        run_command_windows, 
        check_git_installed_windows, 
        check_repo_exists_windows
    )


async def run_command(*args: str) -> Tuple[bytes, bytes]:
    """
    Execute a shell command asynchronously and return (stdout, stderr) bytes.

    Parameters
    ----------
    *args : str
        The command and its arguments to execute.

    Returns
    -------
    Tuple[bytes, bytes]
        A tuple containing the stdout and stderr of the command.

    Raises
    ------
    RuntimeError
        If command exits with a non-zero status.
    """
    # Use Windows-specific implementation if on Windows
    if sys.platform == 'win32':
        return await run_command_windows(*args)
    
    # Original implementation for non-Windows platforms
    # Execute the requested command
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        error_message = stderr.decode().strip()
        raise RuntimeError(f"Command failed: {' '.join(args)}\nError: {error_message}")

    return stdout, stderr


async def ensure_git_installed() -> None:
    """
    Ensure Git is installed and accessible on the system.

    Raises
    ------
    RuntimeError
        If Git is not installed or not accessible.
    """
    # Use Windows-specific implementation if on Windows
    if sys.platform == 'win32':
        is_installed = await check_git_installed_windows()
        if not is_installed:
            raise RuntimeError("Git is not installed or not accessible. Please install Git first.")
        return
    
    # Original implementation for non-Windows platforms
    try:
        await run_command("git", "--version")
    except RuntimeError as exc:
        raise RuntimeError("Git is not installed or not accessible. Please install Git first.") from exc


async def check_repo_exists(url: str) -> bool:
    """
    Check if a Git repository exists at the provided URL.

    Parameters
    ----------
    url : str
        The URL of the Git repository to check.
    Returns
    -------
    bool
        True if the repository exists, False otherwise.

    Raises
    ------
    RuntimeError
        If the curl command returns an unexpected status code.
    """
    # Use Windows-specific implementation if on Windows
    if sys.platform == 'win32':
        return await check_repo_exists_windows(url)
    
    # Original implementation for non-Windows platforms
    proc = await asyncio.create_subprocess_exec(
        "curl",
        "-I",
        url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()

    if proc.returncode != 0:
        return False  # likely unreachable or private

    response = stdout.decode()
    status_line = response.splitlines()[0].strip()
    parts = status_line.split(" ")
    if len(parts) >= 2:
        status_code_str = parts[1]
        if status_code_str in ("200", "301"):
            return True
        if status_code_str in ("302", "404"):
            return False
    raise RuntimeError(f"Unexpected status line: {status_line}")


async def fetch_remote_branch_list(url: str) -> List[str]:
    """
    Fetch the list of branches from a remote Git repository.
    Parameters
    ----------
    url : str
        The URL of the Git repository to fetch branches from.
    Returns
    -------
    List[str]
        A list of branch names available in the remote repository.
    """
    fetch_branches_command = ["git", "ls-remote", "--heads", url]
    await ensure_git_installed()
    stdout, _ = await run_command(*fetch_branches_command)
    stdout_decoded = stdout.decode()

    return [
        line.split("refs/heads/", 1)[1]
        for line in stdout_decoded.splitlines()
        if line.strip() and "refs/heads/" in line
    ]
