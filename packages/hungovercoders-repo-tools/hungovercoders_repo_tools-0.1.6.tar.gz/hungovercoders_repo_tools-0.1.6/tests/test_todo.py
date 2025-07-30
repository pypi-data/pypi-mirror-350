from hungovercoders_repo_tools.todo import get_gitignore_patterns, is_ignored, find_todos, write_todo_md

def test_get_gitignore_patterns(tmp_path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("""
# comment
__pycache__/
*.pyc
venv/
    """)
    patterns = get_gitignore_patterns(gitignore)
    assert "__pycache__/" in patterns
    assert "*.pyc" in patterns
    assert "venv/" in patterns
    assert all(not p.startswith('#') for p in patterns)

def test_is_ignored(tmp_path):
    # Create files and dirs
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "venv").mkdir()
    (tmp_path / "foo.pyc").write_text("")
    (tmp_path / "bar.py").write_text("")
    patterns = ["__pycache__", "*.pyc", "venv/"]
    # Patch Path.cwd to tmp_path for this test to avoid ValueError
    import pathlib
    orig_cwd = pathlib.Path.cwd
    pathlib.Path.cwd = lambda: tmp_path
    try:
        assert is_ignored(tmp_path / "__pycache__", patterns)
        assert is_ignored(tmp_path / "foo.pyc", patterns)
        assert is_ignored(tmp_path / "venv", patterns)
        assert not is_ignored(tmp_path / "bar.py", patterns)
        # Test githook ignore
        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        hook_file = git_hooks / "pre-commit.sample"
        hook_file.write_text("")
        assert is_ignored(hook_file, patterns)
    finally:
        pathlib.Path.cwd = orig_cwd

def test_find_todos(tmp_path):
    import pathlib
    orig_cwd = pathlib.Path.cwd
    pathlib.Path.cwd = lambda: tmp_path
    try:
        # Create a file with TODOs
        src = tmp_path / "src"
        src.mkdir()
        file1 = src / "a.py"
        file1.write_text("""
# TODO: first
print('hi')
# TODO: second
        """)
        file2 = src / "b.py"
        file2.write_text("print('no todos')\n")
        # Add a fake todo.py with the search pattern line
        todo_py = src / "todo.py"
        todo_py.write_text("match = re.search(r'TODO:(.*)', line)\n# TODO: not this line\n")
        todos = find_todos(tmp_path, [])
        assert ("src/a.py", 2, "first") in todos
        assert ("src/a.py", 4, "second") in todos
        assert not any("b.py" in t[0] for t in todos)
        # Should not include the search pattern line from todo.py
        # But should include the actual TODO in todo.py
        assert any(t[0] == "src/todo.py" and t[2] == "not this line" for t in todos)
    finally:
        pathlib.Path.cwd = orig_cwd

def test_write_todo_md(tmp_path):
    todos = [("src/a.py", 2, "first"), ("src/a.py", 4, "second")]
    md_path = tmp_path / "todo.md"
    write_todo_md(todos, md_path)
    content = md_path.read_text()
    assert "| src/a.py | 2 | first |" in content
    assert "| src/a.py | 4 | second |" in content
    # Test empty todos
    write_todo_md([], md_path)
    content = md_path.read_text()
    assert "No TODOs found" in content
