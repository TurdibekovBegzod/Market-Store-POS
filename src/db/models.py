from sqlalchemy import Column, Integer, String, Date, UUID
from src.db.data import Base
from src.utils import get_current_time
import uuid

class User(Base):
    __tablename__ = "users"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(Date, default=get_current_time)
    updated_at = Column(Date, default=get_current_time, onupdate=get_current_time)
