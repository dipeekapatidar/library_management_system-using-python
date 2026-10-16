"""Core logic: books, users, issue/return, due dates and fines."""
from datetime import date, timedelta
import storage
from config import LOAN_DAYS, FINE_PER_DAY, MAX_BOOKS_PER_USER


def _next_id(rows, prefix):
    nums = [int(r["id"][len(prefix):]) for r in rows]
    return f"{prefix}{(max(nums) + 1 if nums else 1):03d}"


class Library:
    def __init__(self):
        self.reload()

    # ---------- data handling ----------
    def reload(self):
        self.books = storage.load("books")
        self.users = storage.load("users")
        self.records = storage.load("records")

    def _save_all(self):
        storage.save("books", self.books)
        storage.save("users", self.users)
        storage.save("records", self.records)

    # ---------- lookups ----------
    def find_book(self, book_id):
        return next((b for b in self.books if b["id"].lower() == book_id.lower()), None)

    def find_user(self, user_id):
        return next((u for u in self.users if u["id"].lower() == user_id.lower()), None)

    def active_records(self):
        return [r for r in self.records if r["return_date"] is None]

    def user_active_count(self, user_id):
        return sum(1 for r in self.active_records() if r["user_id"] == user_id)

    # ---------- books & users ----------
    def add_book(self, title, author, copies=1):
        book = {"id": _next_id(self.books, "B"), "title": title.strip(),
                "author": author.strip(), "copies": copies, "available": copies}
        self.books.append(book)
        self._save_all()
        return book

    def add_user(self, name, contact=""):
        user = {"id": _next_id(self.users, "U"), "name": name.strip(),
                "contact": contact.strip(), "joined": date.today().isoformat()}
        self.users.append(user)
        self._save_all()
        return user

    def remove_book(self, book_id):
        book = self.find_book(book_id)
        if not book:
            return False, "Book not found."
        if book["available"] != book["copies"]:
            return False, "Some copies are still issued. Cannot remove."
        self.books.remove(book)
        self._save_all()
        return True, f"Removed '{book['title']}'."

    def remove_user(self, user_id):
        user = self.find_user(user_id)
        if not user:
            return False, "User not found."
        if self.user_active_count(user["id"]):
            return False, "User still has issued books. Cannot remove."
        self.users.remove(user)
        self._save_all()
        return True, f"Removed member '{user['name']}'."

    # ---------- search ----------
    def search_books(self, keyword):
        k = keyword.lower().strip()
        return [b for b in self.books if k in b["title"].lower() or k in b["author"].lower()]

    # ---------- issue / return ----------
    def issue_book(self, book_id, user_id, today=None):
        today = today or date.today()
        book, user = self.find_book(book_id), self.find_user(user_id)
        if not book:
            return False, "Book ID not found."
        if not user:
            return False, "User ID not found."
        if book["available"] < 1:
            return False, "No copies available right now."
        if self.user_active_count(user["id"]) >= MAX_BOOKS_PER_USER:
            return False, f"{user['name']} already has {MAX_BOOKS_PER_USER} books."
        if any(r for r in self.active_records()
               if r["book_id"] == book["id"] and r["user_id"] == user["id"]):
            return False, "This user already has this book."

        due = today + timedelta(days=LOAN_DAYS)
        self.records.append({
            "id": _next_id(self.records, "T"), "book_id": book["id"], "user_id": user["id"],
            "issue_date": today.isoformat(), "due_date": due.isoformat(),
            "return_date": None, "fine": 0})
        book["available"] -= 1
        self._save_all()
        return True, f"Issued '{book['title']}' to {user['name']}. Due on {due.isoformat()}."

    @staticmethod
    def calculate_fine(due_date, return_date):
        late_days = (return_date - due_date).days
        return max(late_days, 0) * FINE_PER_DAY

    def return_book(self, book_id, user_id, today=None):
        today = today or date.today()
        rec = next((r for r in self.active_records()
                    if r["book_id"].lower() == book_id.lower()
                    and r["user_id"].lower() == user_id.lower()), None)
        if not rec:
            return False, "No active issue found for this book and user.", 0
        fine = self.calculate_fine(date.fromisoformat(rec["due_date"]), today)
        rec["return_date"] = today.isoformat()
        rec["fine"] = fine
        self.find_book(book_id)["available"] += 1
        self._save_all()
        return True, "Book returned successfully.", fine

    # ---------- reports ----------
    def available_books(self):
        return [b for b in self.books if b["available"] > 0]

    def issued_report(self, today=None):
        """Active issues with user/book names and overdue info."""
        today = today or date.today()
        rows = []
        for r in self.active_records():
            due = date.fromisoformat(r["due_date"])
            book, user = self.find_book(r["book_id"]), self.find_user(r["user_id"])
            rows.append({
                "book_id": r["book_id"], "title": book["title"] if book else "?",
                "user_id": r["user_id"], "user": user["name"] if user else "?",
                "due_date": r["due_date"],
                "days_left": (due - today).days,
                "fine_now": self.calculate_fine(due, today)})
        return rows
