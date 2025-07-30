from hungovercoders_repo_tools import greetings
# from pathlib import Path
# import os
# import hungovercoders_repo_tools.todo

greetings.hello()

# current = Path(__file__).resolve().parent
# repo_root = None
# for parent in [current] + list(current.parents):
#     if (parent / '.gitignore').exists() or (parent / '.git').exists():
#         repo_root = parent
#         break
# if repo_root is None:
#     repo_root = Path(__file__).resolve().parent.parent.parent  # fallback
# gitignore_path = repo_root / '.gitignore'
# docs_dir = repo_root / 'docs'
# docs_dir.mkdir(exist_ok=True)
# output_path = docs_dir / 'todo.md'
# ignore_patterns = todo.get_gitignore_patterns(gitignore_path)
# todos = todo.find_todos(repo_root, ignore_patterns)
# todo.write_todo_md(todos, output_path)

# todo.main()



# print("CWD:", os.getcwd())
# print("todo.py location:", hungovercoders_repo_tools.todo.__file__)
# print("__file__:", __file__)
# current = Path(__file__).resolve().parent
# print(current)

