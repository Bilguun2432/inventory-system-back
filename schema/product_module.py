from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from config.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import functions
from .auth_module import AuthUser


class ProductCategory(Base):
    __tablename__ = "product_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, name="is_deleted", default=False)
    userCreatedId: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("auth_user.id"), name="user_created_id", nullable=True)
    timeCreated: Mapped[Optional[datetime]] = mapped_column(DateTime, name="time_created", default=functions.now())

    userCreated: Mapped[Optional["AuthUser"]] = relationship("AuthUser", foreign_keys=[userCreatedId])


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    categoryId: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("product_category.id"), name="category_id")
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer, name="price", nullable=True)
    unit: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, name="is_deleted", default=False)
    userCreatedId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), name="user_created_id", nullable=True)
    timeCreated: Mapped[int] = mapped_column(DateTime, name="time_created", default=functions.now())

    category: Mapped[Optional["ProductCategory"]] = relationship("ProductCategory", foreign_keys=[categoryId])
    userCreated: Mapped["AuthUser"] = relationship("AuthUser")