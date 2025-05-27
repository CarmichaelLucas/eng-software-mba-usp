from passlib.context import CryptContext


class EncodeUtil:
    def __init__(self):
        self.context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def crypt(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self.context.verify(password, password_hash)
