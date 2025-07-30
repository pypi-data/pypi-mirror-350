"""
Windows-specific helper functions for purgo_ingest.
This module provides Windows-compatible alternatives to asyncio subprocess functions.
"""

import subprocess
import os
import asyncio
from typing import List, Tuple, Optional, Dict, Any


def run_command_sync(*args: str) -> Tuple[bytes, bytes]:
    """
    Execute a command synchronously on Windows and return (stdout, stderr) bytes.
    
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
    try:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=False  # Keep as bytes for consistency
        )
        return process.stdout, process.stderr
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip() if isinstance(e.stderr, bytes) else str(e.stderr).strip()
        raise RuntimeError(f"Command failed: {' '.join(args)}\nError: {error_message}")


async def run_command_windows(*args: str) -> Tuple[bytes, bytes]:
    """
    Execute a command asynchronously on Windows by running in a thread pool.
    This works around Windows asyncio subprocess limitations.
    
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
    # Run the synchronous command in a thread pool to make it "async-compatible"
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: run_command_sync(*args))


def check_git_installed_sync() -> bool:
    """
    Check if Git is installed synchronously (Windows-specific).
    
    Returns
    -------
    bool
        True if Git is installed, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


async def check_git_installed_windows() -> bool:
    """
    Check if Git is installed asynchronously (Windows-specific).
    
    Returns
    -------
    bool
        True if Git is installed, False otherwise.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, check_git_installed_sync)


def check_repo_exists_sync(url: str) -> bool:
    """
    Check if a Git repository exists at the provided URL synchronously (Windows-specific).
    
    Parameters
    ----------
    url : str
        The URL of the Git repository to check.
        
    Returns
    -------
    bool
        True if the repository exists, False otherwise.
    """
    try:
        process = subprocess.run(
            ["curl", "-I", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,  # Don't raise exception for non-zero return code
            text=False
        )
        if process.returncode != 0:
            return False
            
        response = process.stdout.decode()
        status_line = response.splitlines()[0].strip()
        parts = status_line.split(" ")
        if len(parts) >= 2:
            status_code_str = parts[1]
            if status_code_str in ("200", "301"):
                return True
            if status_code_str in ("302", "404"):
                return False
        return False  # If we can't determine, assume it doesn't exist
    except Exception:
        return False


async def check_repo_exists_windows(url: str) -> bool:
    """
    Check if a Git repository exists at the provided URL asynchronously (Windows-specific).
    
    Parameters
    ----------
    url : str
        The URL of the Git repository to check.
        
    Returns
    -------
    bool
        True if the repository exists, False otherwise.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: check_repo_exists_sync(url)) 
