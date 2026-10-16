"""Library Management System - command line menu.
Run with:  python main.py
"""
from datetime import date
from library import Library
import backup
from config import LIBRARY_NAME, CREATED_BY, LOAN_DAYS, FINE_PER_DAY, CURRENCY

lib = Library()


def banner():
    print("\n" + "=" * 56)
    print(f"  {LIBRARY_NAME.upper()}")
    print(f"  Library Management System  |  by {CREATED_BY}")
    print("=" * 56)


def show_table(headers, rows):
    if not rows:
        print("  (nothing to show)")
        return
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "  " + " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("  " + "-+-".join("-" * w for w in widths))
    for r in rows:
        print("  " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))


def ask_int(prompt, default=1):
    try:
        v = int(input(prompt) or default)
        return v if v > 0 else default
    except ValueError:
        return default


def books_table(books):
    show_table(["ID", "Title", "Author", "Available/Total"],
               [(b["id"], b["title"], b["author"], f"{b['available']}/{b['copies']}") for b in books])


# ---------- menu actions ----------
def add_book():
    title = input("  Title: ").strip()
    author = input("  Author: ").strip()
    if not title or not author:
        print("  Title and author are required.")
        return
    copies = ask_int("  Copies [1]: ")
    b = lib.add_book(title, author, copies)
    print(f"  Added book {b['id']} - {b['title']}")


def add_user():
    name = input("  Member name: ").strip()
    if not name:
        print("  Name is required.")
        return
    u = lib.add_user(name, input("  Phone/Email (optional): "))
    print(f"  Member created with ID {u['id']}")


def issue():
    ok, msg = lib.issue_book(input("  Book ID: ").strip(), input("  User ID: ").strip())
    print("  " + msg)


def return_():
    ok, msg, fine = lib.return_book(input("  Book ID: ").strip(), input("  User ID: ").strip())
    print("  " + msg)
    if ok:
        if fine:
            print(f"  Late return! Fine to pay: {CURRENCY} {fine}")
        else:
            print("  Returned on time. No fine.")


def search():
    kw = input("  Enter title or author: ")
    if not kw.strip():
        return
    books_table(lib.search_books(kw))


def issued():
    rows = lib.issued_report()
    table = []
    for r in rows:
        status = f"{r['days_left']} days left" if r["days_left"] >= 0 else f"OVERDUE {-r['days_left']}d"
        table.append((r["book_id"], r["title"], f"{r['user_id']} {r['user']}",
                      r["due_date"], status, f"{CURRENCY} {r['fine_now']}"))
    show_table(["Book", "Title", "Member", "Due", "Status", "Fine now"], table)


def users():
    show_table(["ID", "Name", "Contact", "Joined", "Books held"],
               [(u["id"], u["name"], u["contact"], u["joined"], lib.user_active_count(u["id"]))
                for u in lib.users])


def remove_book():
    print("  " + lib.remove_book(input("  Book ID to remove: ").strip())[1])


def remove_user():
    print("  " + lib.remove_user(input("  User ID to remove: ").strip())[1])


def do_backup():
    print("  Backup saved:", backup.create_backup())


def do_restore():
    files = backup.list_backups()
    if not files:
        print("  No backups found.")
        return
    for i, f in enumerate(files, 1):
        print(f"   {i}. {f}")
    try:
        choice = files[int(input("  Choose number to restore: ")) - 1]
    except (ValueError, IndexError):
        print("  Invalid choice.")
        return
    if input(f"  Restore {choice}? Current data will be replaced (y/n): ").lower() == "y":
        backup.restore_backup(choice)
        lib.reload()
        print("  Data restored.")


def sample_data():
    if lib.books or lib.users:
        print("  Sample data is only added to an empty library.")
        return
    for t, a, c in [("Wings of Fire", "A.P.J. Abdul Kalam", 2), ("The Alchemist", "Paulo Coelho", 1),
                    ("Clean Code", "Robert C. Martin", 2), ("Python Crash Course", "Eric Matthes", 3)]:
        lib.add_book(t, a, c)
    lib.add_user("Rahul Sharma", "rahul@example.com")
    lib.add_user("Priya Verma", "9999900000")
    print("  Sample books and members added.")


MENU = [
    ("Add book", add_book), ("Add member", add_user), ("Issue book", issue),
    ("Return book", return_), ("Search books (title/author)", search),
    ("Show available books", lambda: books_table(lib.available_books())),
    ("Show issued books", issued), ("Show all books", lambda: books_table(lib.books)),
    ("Show all members", users), ("Remove book", remove_book), ("Remove member", remove_user),
    ("Backup data", do_backup), ("Restore data", do_restore), ("Load sample data", sample_data),
]


def main():
    banner()
    print(f"  Loan period: {LOAN_DAYS} days | Fine: {CURRENCY} {FINE_PER_DAY}/day | Today: {date.today()}")
    while True:
        print("\n  MAIN MENU")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"   {i:>2}. {label}")
        print("    0. Exit")
        choice = input("\n  Your choice: ").strip()
        if choice == "0":
            print("  Thank you for using the library system. Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            print()
            MENU[int(choice) - 1][1]()
        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    main()
