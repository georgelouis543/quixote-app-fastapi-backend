import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer

from app.config.database import Base


class Newsletter(Base):
    __tablename__ = "newsletters"

    id = Column(String, primary_key=True, index=True)  # Newsletter ID
    title = Column(String)  # Newsletter subject/title
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))


class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(String, primary_key=True, index=True)  # Distribution ID
    newsletter_id = Column(String, ForeignKey("newsletters.id"))  # Linking to newsletters
    scheduled_date = Column(DateTime)
    subject = Column(String, nullable=True)
    status = Column(String, index=True)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email_address = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))


class EmailAnalytics(Base):
    __tablename__ = "email_analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    distribution_id = Column(String, ForeignKey("distributions.id"))
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))  # Reference subscribers
    opened = Column(Integer, default=0, index=True)
    clicked = Column(Integer, default=0, index=True)
    bounced = Column(Integer, default=0, index=True)
    blocked = Column(Integer, default=0, index=True)
    delivered = Column(Integer, default=0, index=True)
