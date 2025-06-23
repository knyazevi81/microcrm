from sqlalchemy import String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String,)
    role: Mapped[int] = mapped_column(Integer, ForeignKey("user_roles.id"))

    role_obj: Mapped["UserRole"] = relationship("UserRole", back_populates="users")
    deals: Mapped[list["Deal"]] = relationship(back_populates="user") # type: ignore  # noqa: F821

class UserRole(Base):
    __tablename__ = "user_roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="role_obj")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String,)
    username: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String,)

    deals: Mapped[list["Deal"]] = relationship(back_populates="client")


class Deal(Base):
    __tablename__ = 'deals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[int] = mapped_column(Integer, ForeignKey("deals_status.id"))
    topic: Mapped[str] = mapped_column(String,)

    client: Mapped["Client"] = relationship("Client", back_populates="deals")  # noqa: F821
    user: Mapped["User"] = relationship("User", back_populates="deals")
    status_obj: Mapped["DealStatus"] = relationship("DealStatus", back_populates="deals")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="deal")


class DealStatus(Base):
    __tablename__ = "deals_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

    deals: Mapped[list["Deal"]] = relationship(back_populates="status_obj")


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(Integer, ForeignKey("deals.id", ondelete="CASCADE"))
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    sender_type: Mapped[str] = mapped_column(String, nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="messages")
