import hashlib


def hashed_password(password):
    password = hashlib.sha256(password.encode()).hexdigest()
    return password
