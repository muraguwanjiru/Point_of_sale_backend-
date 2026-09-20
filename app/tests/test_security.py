from  app.core.security import Hash_password, Verify_password, create_access_token, decode_access_token

def test_hash_password():
    password = "testpassword"
    hashed = Hash_password(password)
    
    assert hashed != password
    assert isinstance(hashed, str)
    assert Verify_password(password, hashed) is True

def test_verify_password():
    password = "testpassword"
    hashed = Hash_password(password)
    
    assert Verify_password(password, hashed) is True
    assert Verify_password("wrongpassword", hashed) is False
