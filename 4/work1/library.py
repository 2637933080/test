"""Core borrowing logic for a simple library system."""

from typing import Dict, Tuple


class BorrowError(ValueError):
    """Raised when a borrow operation fails."""


def borrow_book(user: Dict, book: Dict) -> Tuple[Dict, Dict]:
    """Borrow a book for a user.

    Args:
        user: Dictionary with at least an ``id`` and optional ``borrowed_books`` list.
        book: Dictionary with at least an ``id`` and ``available_copies`` integer.

    Returns:
        Updated ``user`` and ``book`` dictionaries to reflect the borrowing.

    Raises:
        BorrowError: When the user or book is missing/invalid, or the book cannot be borrowed.
    """

    if user is None:
        raise BorrowError("User does not exist.")
    if book is None:
        raise BorrowError("Book does not exist.")

    if not isinstance(user, dict) or "id" not in user:
        raise BorrowError("Invalid user record.")
    if not isinstance(book, dict) or "id" not in book:
        raise BorrowError("Invalid book record.")

    if "available_copies" not in book:
        raise BorrowError("Book inventory information missing.")

    available = book["available_copies"]
    if not isinstance(available, int) or available < 0:
        raise BorrowError("Invalid available copies value.")
    if available == 0:
        raise BorrowError("Book is not available.")

    borrowed_books = user.setdefault("borrowed_books", [])
    if book["id"] in borrowed_books:
        raise BorrowError("User has already borrowed this book.")

    book["available_copies"] = available - 1
    borrowed_books.append(book["id"])

    return user, book
