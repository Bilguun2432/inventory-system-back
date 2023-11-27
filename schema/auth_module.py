from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func, text
from config.database import Base


class AuthRole(Base):
    __tablename__ = "auth_role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(255))


class AuthUser(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(180))
    mobile: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(180))
    isDeleted: Mapped[bool] = mapped_column(Boolean, name="is_deleted", default=False)
    timeCreated: Mapped[datetime] = mapped_column(name="time_created", insert_default=func.now())
    authRoleId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_role.id"), name="auth_role_id")
    
    authRole: Mapped[Optional["AuthRole"]] = relationship("AuthRole", foreign_keys=[authRoleId])


class AuthUserPasswordReset(Base):
    __tablename__ = "auth_user_password_reset"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    authUserId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), name="user_id")
    token: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(1))
    timeCreated: Mapped[datetime] = mapped_column(name="time_created", insert_default=func.now())
    timeExpire: Mapped[datetime] = mapped_column(name="time_expire", insert_default=text("(CURRENT_TIMESTAMP + INTERVAL '1 hour')"))

    authUser: Mapped["AuthUser"] = relationship("AuthUser")