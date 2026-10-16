# Library Management System (Python)

A simple command-line project. No external libraries needed, only Python 3.8+.

## Run
    python main.py        (Windows)
    python3 main.py       (Mac / Linux)

## Features
- Issue and return books with due-date tracking
- Fine calculation for late returns (settings in config.py)
- Search by title or author
- Manage book and member records (add / remove)
- View available books and issued books (with overdue status)
- Backup and restore data as zip files

## Files
| File | Purpose |
|------|---------|
| main.py | Menu and user interface |
| library.py | Core logic (issue, return, fine, search) |
| storage.py | Reads/writes JSON data |
| backup.py | Backup and restore |
| config.py | Library name, loan days, fine per day |
| data/ | Saved records (JSON) |
| backups/ | Backup zip files |

## Customize
Open `config.py` and change `LIBRARY_NAME`, `CREATED_BY`, `LOAN_DAYS`, `FINE_PER_DAY`.
Tip: choose menu option "Load sample data" the first time to try it out.
# library_management_system-using-python
