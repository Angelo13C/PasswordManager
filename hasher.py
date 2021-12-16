import argon2

PARAMETERS = argon2.Parameters(argon2.Type.ID, version=-1, salt_len=16,
    hash_len=32, time_cost=3, memory_cost=65536, parallelism=4)

def hash(text):
    hasher = argon2.PasswordHasher()
    hash = hasher.hash(text)
    return hash

def hash_raw(text, salt):        
    hash = argon2.low_level.hash_secret_raw(text.encode("utf-8"), 
        salt, PARAMETERS.time_cost, PARAMETERS.memory_cost,
        PARAMETERS.parallelism, PARAMETERS.hash_len, PARAMETERS.type)
    return hash

def verify(hash, text):
    hasher = argon2.PasswordHasher()
    try:
        hasher.verify(hash, text)
    except argon2.exceptions.VerifyMismatchError:
        return False
    return True

def needs_rehash(hash):
    hasher = argon2.PasswordHasher()
    return hasher.check_needs_rehash(hash)