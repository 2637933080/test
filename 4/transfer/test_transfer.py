import pytest
from transfer import Account, transfer

def test_insufficient_balance():
    a = Account(1, 50)
    b = Account(2, 0)
    with pytest.raises(ValueError, match="Insufficient balance"):
        transfer(a, b, 100)

def test_negative_amount():
    a = Account(1, 50)
    b = Account(2, 0)
    with pytest.raises(ValueError, match="Amount must be positive"):
        transfer(a, b, -10)

def test_normal_transfer():
    a = Account(1, 100)
    b = Account(2, 50)
    transfer(a, b, 30)
    assert a.balance == 70
    assert b.balance == 80