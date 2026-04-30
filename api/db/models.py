from api.db.main import Base

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship



from api.db.main import Base

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Numeric, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barcode = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Numeric(12, 2), nullable=False)
    quantity = Column(Integer, default=0)

    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    currency = relationship("Currency", back_populates="products")

    template_id = Column(Integer, ForeignKey("product_templates.id"))
    template = relationship("ProductTemplate", back_populates="products")

    attributes = Column(JSONB, server_default=text("'[]'"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String(3), unique=True, nullable=False)
    symbol = Column(String(5))

    products = relationship("Product", back_populates="currency")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProductTemplate(Base):
    __tablename__ = "product_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)

    attributes = Column(JSONB, server_default=text("'[]'"))

    products = relationship("Product", back_populates="template")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
