"""
A table or two for demonstrating the vulnerability...
"""

import hashlib


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String


SALT = '289908a3e6cb86c42efdaa4373ef2dd8'

class Base(DeclarativeBase): pass

class User(Base, MappedAsDataclass):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    secrets: Mapped[str | None] = mapped_column(String, nullable=True)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Salt and hash"""
        ENCODING = 'utf-8'
        sha256_hasher = hashlib.new('sha256')
        sha256_hasher.update(bytes(SALT, ENCODING))
        sha256_hasher.update(bytes(password, ENCODING))
        sha256_digest = sha256_hasher.digest()
        return sha256_digest.hex()