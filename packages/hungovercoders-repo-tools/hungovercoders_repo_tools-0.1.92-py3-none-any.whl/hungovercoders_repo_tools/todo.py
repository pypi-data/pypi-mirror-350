import os
import re
from pathlib import Path
import logging
from typing import List, Tuple, Union

def get_gitignore_patterns(gitignore_path: Path) -> List[str]:
    """
    Parse .gitignore file and return a list of ignore patterns.

    Args:
        gitignore_path (Path): Path to the .gitignore file.

    Returns:
        List[str]: List of ignore patterns.
    """
    patterns: List[str] = []
    if not gitignore_path.exists():
        return patterns
    with gitignore_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns

def is_ignored(path: Path, patterns: List[str]) -> bool:
    """
    Check if a file or directory should be ignored based on patterns and git hook rules.

    Args:
        path (Path): Path to check.
        patterns (List[str]): List of ignore patterns.

    Returns:
        bool: True if path should be ignored, False otherwise.
    """
    from fnmatch import fnmatch
    git_hooks_patterns = ['.git/hooks/', '.git/hooks/*']
    for gh_pattern in git_hooks_patterns:
        try:
            if fnmatch(str(path), gh_pattern) or fnmatch(str(path.relative_to(Path.cwd())), gh_pattern):
                return True
        except ValueError:
            # path is not relative to cwd
            continue
    for pattern in patterns:
        if pattern.endswith('/'):
            try:
                if path.is_dir() and fnmatch(str(path.relative_to(Path.cwd())), pattern.rstrip('/')):
                    return True
                if fnmatch(str(path.parent.relative_to(Path.cwd())), pattern.rstrip('/')):
                    return True
            except ValueError:
                continue
        if fnmatch(str(path.relative_to(Path.cwd())), pattern):
            return True
    return False

def find_todos(root_dir: Union[str, Path], ignore_patterns: List[str]) -> List[Tuple[str, int, str]]:
    """
    Recursively scan files for TODO comments, skipping ignored files/dirs.

    Args:
        root_dir (Union[str, Path]): Root directory to scan.
        ignore_patterns (List[str]): List of ignore patterns.

    Returns:
        List[Tuple[str, int, str]]: List of (file, line number, TODO message).
    """
    todos: List[Tuple[str, int, str]] = []
    this_file = Path(__file__).resolve()
    root_dir = Path(root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not is_ignored(Path(dirpath) / d, ignore_patterns)]
        for filename in filenames:
            file_path = Path(dirpath) / filename
            if is_ignored(file_path, ignore_patterns):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        match = re.search(r'TODO:(.*)', line)
                        # Ignore the specific instance in this file where the line contains the search pattern itself
                        if str(file_path.resolve()) == str(this_file) and "match = re.search(r'TODO:(.*)', line)" in line:
                            continue
                        if match:
                            todos.append((str(file_path.relative_to(root_dir)), i, match.group(1).strip()))
            except Exception as e:
                logging.warning(f"Failed to read {file_path}: {e}")
                continue
    return todos

def write_todo_md(todos: List[Tuple[str, int, str]], output_path: Union[str, Path]) -> None:
    """
    Write TODOs to a Markdown file in a table format.

    Args:
        todos (List[Tuple[str, int, str]]): List of TODOs.
        output_path (Union[str, Path]): Path to output Markdown file.
    """
    output_path = Path(output_path)
    with output_path.open('w', encoding='utf-8') as f:
        f.write('# TODOs in Repository\n\n')
        f.write('| File | Line | TODO Comment |\n')
        f.write('|------|------|--------------|\n')
        if todos:
            for file, line, comment in todos:
                f.write(f'| {file} | {line} | {comment} |\n')
        else:
            f.write('| _No TODOs found in tracked files (excluding .gitignore entries)._ |\n')
        f.write('\n*This list is auto-generated. Only TODOs in tracked files are shown.*\n')

def main() -> None:
    """
    CLI entry point for scanning and reporting TODOs in the repository.
    """
    # Find the repo root by walking up until .git or .gitignore is found
    current = Path(__file__).resolve().parent
    print(f"Current directory: {current}")
    repo_root = None
    for parent in [current] + list(current.parents):
        if (parent / '.gitignore').exists() or (parent / '.git').exists():
            repo_root = parent
            break
    if repo_root is None:
        repo_root = Path(__file__).resolve().parent.parent.parent  # fallback
    gitignore_path = repo_root / '.gitignore'
    docs_dir = repo_root / 'docs'
    docs_dir.mkdir(exist_ok=True)
    output_path = docs_dir / 'todo.md'
    ignore_patterns = get_gitignore_patterns(gitignore_path)
    todos = find_todos(repo_root, ignore_patterns)
    print(f"Found {len(todos)} TODOs in the repository.")
    write_todo_md(todos, output_path)
    print(f"TODOs written to {output_path.resolve()}")

if __name__ == '__main__':
    main()