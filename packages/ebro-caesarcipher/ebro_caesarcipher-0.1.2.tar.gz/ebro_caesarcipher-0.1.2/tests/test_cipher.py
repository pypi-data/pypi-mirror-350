from caesarcipher import encrypt, decrypt

def test_encrypt():
    assert encrypt('ABC', 3) == 'DEF'
    assert encrypt('xyz', 2) == 'zab'

def test_decrypt():
    assert decrypt('DEF', 3) == 'ABC'
    assert decrypt('zab', 2) == 'xyz'
