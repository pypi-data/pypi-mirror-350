"""This module contains functions for cloning a Git repository to a local path."""

import os
from pathlib import Path
from typing import Optional

from purgo_ingest.schemas import CloneConfig
from purgo_ingest.utils.git_utils import check_repo_exists, ensure_git_installed, run_command
from purgo_ingest.utils.timeout_wrapper import async_timeout

TIMEOUT: int = 60


@async_timeout(TIMEOUT)
async def clone_repo(config: CloneConfig) -> None:
    """
    Clone a repository to a local path based on the provided configuration.

    This function handles the process of cloning a Git repository to the local file system.
    It can clone a specific branch or commit if provided, and it raises exceptions if
    any errors occur during the cloning process.

    Parameters
    ----------
    config : CloneConfig
        The configuration for cloning the repository.

    Raises
    ------
    ValueError
        If the repository is not found or if the provided URL is invalid.
    OSError
        If an error occurs while creating the parent directory for the repository.
    """
    # Extract and validate query parameters
    url: str = config.url
    local_path: str = config.local_path
    commit: Optional[str] = config.commit
    branch: Optional[str] = config.branch
    partial_clone: bool = config.subpath != "/"
    git_token: Optional[str] = config.git_token

    # Create parent directory if it doesn't exist
    parent_dir = Path(local_path).parent
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except OSError as exc:
        raise OSError(f"Failed to create parent directory {parent_dir}: {exc}") from exc

    # If a git token is provided, modify the URL
    if git_token:
        if "://" in url:
            protocol, rest_of_url = url.split("://", 1)
            url = f"{protocol}://{git_token}@{rest_of_url}"
        else:
            # Assuming https if no protocol is specified with a token
            url = f"https://{git_token}@{url}"

    # Check if the repository exists only if no token is provided
    if not git_token and not await check_repo_exists(url):
        raise ValueError("Repository not found, make sure it is public or a valid token is provided")

    clone_cmd = ["git", "clone", "--single-branch"]
    # TODO re-enable --recurse-submodules

    if partial_clone:
        clone_cmd += ["--filter=blob:none", "--sparse"]

    if not commit:
        clone_cmd += ["--depth=1"]
        if branch and branch.lower() not in ("main", "master"):
            clone_cmd += ["--branch", branch]

    clone_cmd += [url, local_path]

    # Clone the repository
    await ensure_git_installed()
    await run_command(*clone_cmd)

    if commit or partial_clone:
        checkout_cmd = ["git", "-C", local_path]

        if partial_clone:
            subpath = config.subpath.lstrip("/")
            if config.blob:
                # When ingesting from a file url (blob/branch/path/file.txt), we need to remove the file name.
                subpath = str(Path(subpath).parent.as_posix())

            checkout_cmd += ["sparse-checkout", "set", subpath]

        if commit:
            checkout_cmd += ["checkout", commit]

        # Check out the specific commit and/or subpath
        await run_command(*checkout_cmd)
