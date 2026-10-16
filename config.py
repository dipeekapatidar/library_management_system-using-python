"""Settings for the Library Management System.
Change these values to customize the project as your own."""
import os

LIBRARY_NAME = "My Campus Library"      # <- change to your library / college name
CREATED_BY = "Your Name"                # <- put your name here
LOAN_DAYS = 14                          # days a book can be kept
FINE_PER_DAY = 2                        # fine (Rs.) for each late day
MAX_BOOKS_PER_USER = 3                  # books one member can hold at once
CURRENCY = "Rs."

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
