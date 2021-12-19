from abc import ABC, abstractmethod

class NotAuthenticatedError(Exception):
    pass

class AuthenticationMethod(ABC):
    @abstractmethod
    def authenticate(self, key):
        pass

    @abstractmethod
    def encrypt(self, text):
        pass

    @abstractmethod
    def decrypt(self, encoded_text):
        pass