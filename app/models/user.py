from sqlalchemy import Boolean, Column, Integer, String
from app.config.database import Base


class User(Base):
    __tablename__ = 'userTable'

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, unique=True, nullable=False)
    user_name = Column(String, index=True, unique=True, nullable=False)
    role = Column(String, index=True, nullable=False, default="user")
    refresh_token = Column(String, index=True)
