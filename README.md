# Book Compiler

Lightweight app to compile .md files from Obsidian into a single file, ordered by chapter name.

Converts the documents to pdf by default, but there is an optional --format flag that lets you specify .docx instead

Usage:
```commandline
uv run main.py "path/to/files" "book name"
```

or to make it word:
```commandline
uv run main.py "path/to/files" "book name" --format "docx"
```