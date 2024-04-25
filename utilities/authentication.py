from argon2 import PasswordHasher


passwordHash = PasswordHasher()


def verify_password(plain_password, hashed_password):
    try:
        return passwordHash.verify(hashed_password, plain_password)
    except Exception as e:
        print(e)
        return False


def hash_password(password):
    try:
        return passwordHash.hash(password)
    except:
        return False
