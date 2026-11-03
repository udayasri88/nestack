from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Argon2 password hasher
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4
)


def hash_password(password):

    hashed_password = password_hasher.hash(password)

    return hashed_password


def verify_password(stored_hash, entered_password):

    try:

        return password_hasher.verify(
            stored_hash,
            entered_password
        )

    except VerifyMismatchError:

        return False