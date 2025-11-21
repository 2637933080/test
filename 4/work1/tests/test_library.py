import pytest

from library import BorrowError, borrow_book


def make_user(user_id="user-1", borrowed=None):
    return {"id": user_id, "borrowed_books": list(borrowed or [])}


def make_book(book_id="book-1", copies=1):
    return {"id": book_id, "available_copies": copies}


def test_borrow_book_success():
    user = make_user()
    book = make_book(copies=3)

    updated_user, updated_book = borrow_book(user, book)

    assert updated_book["available_copies"] == 2
    assert updated_user["borrowed_books"] == ["book-1"]


def test_borrow_book_user_missing():
    book = make_book()

    with pytest.raises(BorrowError, match="User does not exist"):
        borrow_book(None, book)


def test_borrow_book_book_missing():
    user = make_user()

    with pytest.raises(BorrowError, match="Book does not exist"):
        borrow_book(user, None)


def test_borrow_book_no_stock():
    user = make_user()
    book = make_book(copies=0)

    with pytest.raises(BorrowError, match="not available"):
        borrow_book(user, book)


def test_borrow_book_invalid_user_structure():
    book = make_book()

    with pytest.raises(BorrowError, match="Invalid user record"):
        borrow_book({"name": "Alice"}, book)


def test_borrow_book_missing_inventory_information():
    user = make_user()
    book = {"id": "book-1"}

    with pytest.raises(BorrowError, match="inventory information"):
        borrow_book(user, book)
