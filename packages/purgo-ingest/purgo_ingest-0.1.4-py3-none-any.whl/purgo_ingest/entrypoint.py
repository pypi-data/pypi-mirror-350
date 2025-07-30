"""Main entry point for ingesting a source and processing its contents."""

import asyncio
import inspect
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from purgo_ingest.cloning import clone_repo
from purgo_ingest.config import TMP_BASE_PATH
from purgo_ingest.ingestion import ingest_query
from purgo_ingest.query_parsing import IngestionQuery, parse_query
from purgo_ingest.schemas import FileSystemNode, FileSystemNodeType


async def ingest_async(
    source: str,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    include_patterns: Optional[Union[str, Set[str]]] = None,
    exclude_patterns: Optional[Union[str, Set[str]]] = None,
    branch: Optional[str] = None,
    output: Optional[str] = None,
    git_token: Optional[str] = None,
) -> Tuple[str, str, str]:
    """
    Main entry point for ingesting a source and processing its contents.

    This function analyzes a source (URL or local path), clones the corresponding repository (if applicable),
    and processes its files according to the specified query parameters. It returns a summary, a tree-like
    structure of the files, and the content of the files. The results can optionally be written to an output file.

    Parameters
    ----------
    source : str
        The source to analyze, which can be a URL (for a Git repository) or a local directory path.
    max_file_size : int
        Maximum allowed file size for file ingestion. Files larger than this size are ignored, by default
        10*1024*1024 (10 MB).
    include_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to include. If `None`, all files are included.
    exclude_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to exclude. If `None`, no files are excluded.
    branch : str, optional
        The branch to clone and ingest. If `None`, the default branch is used.
    output : str, optional
        File path where the summary and content should be written. If `None`, the results are not written to a file.
    git_token : str, optional
        The Git token for accessing private repositories, by default None.

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing:
        - A summary string of the analyzed repository or directory.
        - A tree-like string representation of the file structure.
        - The content of the files in the repository or directory.

    Raises
    ------
    TypeError
        If `clone_repo` does not return a coroutine, or if the `source` is of an unsupported type.
    """
    repo_cloned = False

    try:
        query: IngestionQuery = await parse_query(
            source=source,
            max_file_size=max_file_size,
            from_web=False,
            include_patterns=include_patterns,
            ignore_patterns=exclude_patterns,
            git_token=git_token,
        )

        if query.url:
            selected_branch = branch if branch else query.branch  # prioritize branch argument
            query.branch = selected_branch

            clone_config = query.extract_clone_config()
            clone_coroutine = clone_repo(clone_config)

            if inspect.iscoroutine(clone_coroutine):
                if asyncio.get_event_loop().is_running():
                    await clone_coroutine
                else:
                    asyncio.run(clone_coroutine)
            else:
                raise TypeError("clone_repo did not return a coroutine as expected.")

            repo_cloned = True

        summary, tree, content = ingest_query(query)

        if output is not None:
            with open(output, "w", encoding="utf-8") as f:
                f.write(tree + "\n" + content)

        return summary, tree, content
    finally:
        # Clean up the temporary directory if it was created
        if repo_cloned:
            shutil.rmtree(TMP_BASE_PATH, ignore_errors=True)


def ingest(
    source: str,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    include_patterns: Optional[Union[str, Set[str]]] = None,
    exclude_patterns: Optional[Union[str, Set[str]]] = None,
    branch: Optional[str] = None,
    output: Optional[str] = None,
    git_token: Optional[str] = None,
) -> Tuple[str, str, str]:
    """
    Synchronous version of ingest_async.

    This function analyzes a source (URL or local path), clones the corresponding repository (if applicable),
    and processes its files according to the specified query parameters. It returns a summary, a tree-like
    structure of the files, and the content of the files. The results can optionally be written to an output file.

    Parameters
    ----------
    source : str
        The source to analyze, which can be a URL (for a Git repository) or a local directory path.
    max_file_size : int
        Maximum allowed file size for file ingestion. Files larger than this size are ignored, by default
        10*1024*1024 (10 MB).
    include_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to include. If `None`, all files are included.
    exclude_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to exclude. If `None`, no files are excluded.
    branch : str, optional
        The branch to clone and ingest. If `None`, the default branch is used.
    output : str, optional
        File path where the summary and content should be written. If `None`, the results are not written to a file.
    git_token : str, optional
        The Git token for accessing private repositories, by default None.

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing:
        - A summary string of the analyzed repository or directory.
        - A tree-like string representation of the file structure.
        - The content of the files in the repository or directory.

    See Also
    --------
    ingest_async : The asynchronous version of this function.
    """
    return asyncio.run(
        ingest_async(
            source=source,
            max_file_size=max_file_size,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            branch=branch,
            output=output,
            git_token=git_token,
        )
    )


async def ingest_structured_async(
    source: str,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    include_patterns: Optional[Union[str, Set[str]]] = None,
    exclude_patterns: Optional[Union[str, Set[str]]] = None,
    branch: Optional[str] = None,
    output: Optional[str] = None,
    git_token: Optional[str] = None,
) -> Dict[str, Union[str, List[Dict]]]:
    """
    Main entry point for ingesting a source and processing its contents in a structured format.

    This function analyzes a source (URL or local path), clones the corresponding repository (if applicable),
    and processes its files according to the specified query parameters. It returns a dictionary containing 
    repository metadata and a list of files with their contents and paths.

    Parameters
    ----------
    source : str
        The source to analyze, which can be a URL (for a Git repository) or a local directory path.
    max_file_size : int
        Maximum allowed file size for file ingestion. Files larger than this size are ignored, by default
        10*1024*1024 (10 MB).
    include_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to include. If `None`, all files are included.
    exclude_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to exclude. If `None`, no files are excluded.
    branch : str, optional
        The branch to clone and ingest. If `None`, the default branch is used.
    output : str, optional
        File path where the JSON output should be written. If `None`, the results are not written to a file.
    git_token : str, optional
        The Git token for accessing private repositories, by default None.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        A dictionary containing:
        - Repository metadata (name, branch, etc.)
        - A list of files with their contents and paths

    Raises
    ------
    TypeError
        If `clone_repo` does not return a coroutine, or if the `source` is of an unsupported type.
    """
    repo_cloned = False

    try:
        query: IngestionQuery = await parse_query(
            source=source,
            max_file_size=max_file_size,
            from_web=False,
            include_patterns=include_patterns,
            ignore_patterns=exclude_patterns,
            git_token=git_token,
        )

        if query.url:
            selected_branch = branch if branch else query.branch  # prioritize branch argument
            query.branch = selected_branch

            clone_config = query.extract_clone_config()
            clone_coroutine = clone_repo(clone_config)

            if inspect.iscoroutine(clone_coroutine):
                if asyncio.get_event_loop().is_running():
                    await clone_coroutine
                else:
                    asyncio.run(clone_coroutine)
            else:
                raise TypeError("clone_repo did not return a coroutine as expected.")

            repo_cloned = True

        # Get the regular ingestion results to reuse the tree creation
        summary, tree, _ = ingest_query(query)
        
        # Create structured data by traversing the repo
        structured_data = {
            "metadata": {
                "repository": f"{query.user_name}/{query.repo_name}" if query.user_name else query.slug,
                "branch": query.branch,
                "commit": query.commit,
                "subpath": query.subpath,
            },
            "files": _gather_structured_files(query.local_path, query)
        }
        
        # Add summary and tree view for reference
        structured_data["summary"] = summary
        structured_data["tree"] = tree
        
        if output is not None:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(structured_data, f, indent=2)

        return structured_data
    finally:
        # Clean up the temporary directory if it was created
        if repo_cloned:
            shutil.rmtree(TMP_BASE_PATH, ignore_errors=True)


def _gather_structured_files(base_path: Path, query: IngestionQuery) -> List[Dict]:
    """
    Recursively gather file information in a structured format.
    
    Parameters
    ----------
    base_path : Path
        The base path of the repository.
    query : IngestionQuery
        The query object containing ingestion parameters.
        
    Returns
    -------
    List[Dict]
        A list of dictionaries, each containing file metadata and content.
    """
    result = []
    subpath = Path(query.subpath.strip("/")).as_posix()
    path = base_path / subpath
    
    if not path.exists():
        return result
    
    if path.is_file():
        # Handle single file case
        file_node = FileSystemNode(
            name=path.name,
            type=FileSystemNodeType.FILE,
            size=path.stat().st_size,
            file_count=1,
            path_str=str(path.relative_to(base_path)),
            path=path,
        )
        
        if file_node.content:
            result.append({
                "path": file_node.path_str,
                "size": file_node.size,
                "type": "file",
                "content": file_node.content
            })
        return result
    
    # Handle directory case - traverse recursively
    for item in path.glob("**/*"):
        # Skip directories
        if item.is_dir():
            continue
            
        # Apply include/exclude patterns
        if query.ignore_patterns and _should_exclude(item, base_path, query.ignore_patterns):
            continue
            
        if query.include_patterns and not _should_include(item, base_path, query.include_patterns):
            continue
            
        # Check file size
        if item.stat().st_size > query.max_file_size:
            continue
            
        # Create file node
        try:
            file_node = FileSystemNode(
                name=item.name,
                type=FileSystemNodeType.FILE,
                size=item.stat().st_size,
                file_count=1,
                path_str=str(item.relative_to(base_path)),
                path=item,
            )
            
            # Only include text files with valid content
            if file_node.content and file_node.content != "[Non-text file]" and not file_node.content.startswith("Error"):
                result.append({
                    "path": file_node.path_str,
                    "size": file_node.size,
                    "type": "file",
                    "content": file_node.content
                })
        except Exception as e:
            print(f"Error processing file {item}: {e}")
            
    return result


def _should_exclude(path: Path, base_path: Path, ignore_patterns: Set[str]) -> bool:
    """
    Check if a path should be excluded based on ignore patterns.
    
    This is a helper function imported from utils/ingestion_utils.py to avoid circular imports.
    """
    from purgo_ingest.utils.ingestion_utils import _should_exclude
    return _should_exclude(path, base_path, ignore_patterns)


def _should_include(path: Path, base_path: Path, include_patterns: Set[str]) -> bool:
    """
    Check if a path should be included based on include patterns.
    
    This is a helper function imported from utils/ingestion_utils.py to avoid circular imports.
    """
    from purgo_ingest.utils.ingestion_utils import _should_include
    return _should_include(path, base_path, include_patterns)


def ingest_structured(
    source: str,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    include_patterns: Optional[Union[str, Set[str]]] = None,
    exclude_patterns: Optional[Union[str, Set[str]]] = None,
    branch: Optional[str] = None,
    output: Optional[str] = None,
    git_token: Optional[str] = None,
) -> Dict[str, Union[str, List[Dict]]]:
    """
    Synchronous version of ingest_structured_async.

    This function analyzes a source (URL or local path), clones the corresponding repository (if applicable),
    and processes its files according to the specified query parameters. It returns a dictionary containing 
    repository metadata and a list of files with their contents and paths.

    Parameters
    ----------
    source : str
        The source to analyze, which can be a URL (for a Git repository) or a local directory path.
    max_file_size : int
        Maximum allowed file size for file ingestion. Files larger than this size are ignored, by default
        10*1024*1024 (10 MB).
    include_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to include. If `None`, all files are included.
    exclude_patterns : Union[str, Set[str]], optional
        Pattern or set of patterns specifying which files to exclude. If `None`, no files are excluded.
    branch : str, optional
        The branch to clone and ingest. If `None`, the default branch is used.
    output : str, optional
        File path where the JSON output should be written. If `None`, the results are not written to a file.
    git_token : str, optional
        The Git token for accessing private repositories, by default None.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        A dictionary containing:
        - Repository metadata (name, branch, etc.)
        - A list of files with their contents and paths

    See Also
    --------
    ingest_structured_async : The asynchronous version of this function.
    """
    return asyncio.run(
        ingest_structured_async(
            source=source,
            max_file_size=max_file_size,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            branch=branch,
            output=output,
            git_token=git_token,
        )
    )
