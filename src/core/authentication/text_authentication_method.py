from authentication_method import AuthenticationMethod, NotAuthenticatedError
import core.cryptography.cypher as cypher

class TextAuthenticationMethod(AuthenticationMethod):
    def __init__(self, encoded_key):
        self.key = None
        self.salt = encoded_key[:cypher.SALT_LENGTH]
        self.hashed_key = encoded_key[cypher.SALT_LENGTH:]
    
    def add(key):
        hashed_key, salt = cypher.derive_key(key)
        hashed_key = cypher.derive_key(hashed_key + key, salt)
        encoded_key = salt + hashed_key
        return TextAuthenticationMethod(encoded_key), encoded_key

    def authenticate(self, key):
        hashed_key = cypher.derive_key(cypher.derive_key(key, self.salt), self.salt)
        if self.hashed_key == hashed_key:
            self.key = key
            return True

        return False
    
    def check_authentication(self):
        if not self.key:
            raise NotAuthenticatedError()

    def logout(self):
        self.key = None

    def encrypt(self, text):
        self.check_authentication()
        return cypher.encrypt(text, self.key)
    
    def decrypt(self, text):
        self.check_authentication()
        return cypher.decrypt(text, self.key)