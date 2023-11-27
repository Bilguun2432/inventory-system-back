from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from config.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import functions
from .auth_module import AuthUser
from .product_module import Product


class ActionStatus(Base):
    __tablename__ = "action_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(String(100))


class Action(Base):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    actionStatusId: Mapped[int] = mapped_column(Integer, ForeignKey("action_status.id"), name="action_status_id")
    authUserId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), name="auth_user_id")
    productId: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), name="product_id")
    unit: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, name="is_deleted", default=False)
    timeCreated: Mapped[int] = mapped_column(DateTime, name="time_created", default=functions.now())

    ActionStatus: Mapped[Optional["ActionStatus"]] = relationship("ActionStatus", foreign_keys=[actionStatusId])
    AuthUser: Mapped[Optional["AuthUser"]] = relationship("AuthUser", foreign_keys=[authUserId])
    Product: Mapped[Optional["Product"]] = relationship("Product", foreign_keys=[productId])