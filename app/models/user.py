from sqlalchemy import Boolean, Column, Integer, String
from app.config.database import Base


class User(Base):
    __tablename__ = 'userTable'

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    user_name = Column(String, index=True)
    role = Column(String, index=True)
    refresh_token = Column(String, index=True)
