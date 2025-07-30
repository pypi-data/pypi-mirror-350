import warnings
from pathlib import Path
from typing import Tuple, Callable, Iterable, Union
from os import PathLike

# Define types for clarity
PathType = Union[PathLike, str]
CriterionType = Union[
    Callable[[Path], bool],
    PathType,
    Iterable[PathType],
]

# Markers used to detect the root directory of a project.
PROJECT_MARKERS = [
    # Common configuration suffixes or directories
    ".git", ".idea", ".vscode",
    # Python project configuration and metadata files
    "pyproject.toml", "requirements.txt", "setup.py",
]


def path_matches_criterion(path: Path, criterion: PathType) -> bool:
    """Check if a path matches a given file, directory, or glob."""
    target = path / criterion
    if isinstance(criterion, str) and "*" in criterion:  # Treat as glob pattern
        return any(target.parent.glob(criterion))
    return target.exists()


def as_root_criterion(criterion: CriterionType) -> Callable[[Path], bool]:
    """Convert criterion or collection of criteria into a callable."""
    if callable(criterion):
        return criterion
    if isinstance(criterion, (PathLike, str)):
        return lambda path: path_matches_criterion(path, criterion)
    return lambda path: any(as_root_criterion(c)(path) for c in criterion)


def as_start_path(start: Union[None, PathType]) -> Path:
    """Convert start parameter to a Path object, defaulting to the current working directory."""
    return Path(start).resolve() if start else Path.cwd()


def iterate_parent_directories(start_path: Path) -> Iterable[Path]:
    """Iterate through a path and its parent directories."""
    return [start_path, *start_path.parents]


def find_root_with_reason(criterion: CriterionType, start: Union[None, PathType] = None) -> Tuple[Path, str]:
    """
    Recursively search for a directory matching the root criterion.
    Returns the root path and a reason.
    """
    criterion_func = as_root_criterion(criterion)
    start_path = as_start_path(start)
    for directory in iterate_parent_directories(start_path):
        if directory.is_dir() and criterion_func(directory):
            return directory, "Matched criterion"
    raise RuntimeError("Project root not found.")


def project_root(relative_project_path: PathType = "", warn_missing: bool = False) -> Path:
    """
    Returns the project root or resolves a path relative to it.
    """
    root, _ = find_root_with_reason(PROJECT_MARKERS)
    result_path = root / relative_project_path
    if warn_missing and not result_path.exists():
        warnings.warn(f"Path doesn't exist: {result_path}")
    return result_path
