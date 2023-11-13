from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func, text

from config.database import Base


class AuthUserRole(Base):
    __tablename__ = "auth_user_role" 
    userId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), name="user_id", primary_key=True)
    roleId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_role.id"), name="role_id", primary_key=True)
    user: Mapped["AuthUser"] = relationship("AuthUser", foreign_keys=[userId], back_populates="roleRefs")
    role: Mapped["AuthRole"] = relationship("AuthRole", foreign_keys=[roleId])


class AuthUser(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(180))
    mobile: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(180))
    userType: Mapped[str] = mapped_column(String(20), name="user_type")
    isDeleted: Mapped[bool] = mapped_column(Boolean, name="is_deleted", default=False)
    timeCreated: Mapped[datetime] = mapped_column(name="time_created", insert_default=func.now())
    roleRefs: Mapped[List["AuthUserRole"]] = relationship("AuthUserRole", back_populates="user")
    roles: Mapped[List["AuthRole"]] = relationship("AuthRole", secondary="auth_user_role", overlaps="roleRefs,role,user")


class AuthRolePermission(Base):
    __tablename__ = "auth_role_permission"
    roleId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_role.id"), name="role_id", primary_key=True)
    permissionId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_permission.id"), name="permission_id", primary_key=True)
    role: Mapped["AuthRole"] = relationship("AuthRole", back_populates="permissionRefs")
    permission: Mapped["AuthPermission"] = relationship("AuthPermission")


class AuthRole(Base):
    __tablename__ = "auth_role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(255))
    permissionRefs: Mapped[List["AuthRolePermission"]] = relationship("AuthRolePermission", back_populates="role")
    permissions: Mapped[List["AuthPermission"]] = relationship("AuthPermission", secondary="auth_role_permission", overlaps="permissionRefs,role,permission")


class AuthPermission(Base):
    __tablename__ = "auth_permission"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    permissionKey: Mapped[str] = mapped_column(String(100), unique=True, name="permission_key")
    description: Mapped[str] = mapped_column(String(255))
    group_name: Mapped[str] = mapped_column(String(100))


class AuthUserPasswordReset(Base):
    __tablename__ = "auth_user_password_reset"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    authUserId: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), name="user_id")
    token: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(1))
    timeCreated: Mapped[datetime] = mapped_column(name="time_created", insert_default=func.now())
    timeExpire: Mapped[datetime] = mapped_column(name="time_expire", insert_default=text("(CURRENT_TIMESTAMP + INTERVAL '1 hour')"))

    authUser: Mapped["AuthUser"] = relationship("AuthUser")