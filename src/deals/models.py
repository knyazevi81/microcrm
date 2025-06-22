from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class Deal(Base):
    __tablename__ = 'deals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[int] = mapped_column(Integer, ForeignKey("deals_status.id"))
    topic: Mapped[str] = mapped_column(String,)

    client: Mapped["Client"] = relationship("Client", back_populates="deals")  # noqa: F821
    manager: Mapped["User"] = relationship("User", back_populates="deals")
    status_obj: Mapped["DealStatus"] = relationship("DealStatus", back_populates="deals")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="deal")



class DealStatus(Base):
    __tablename__ = "deals_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(Integer, ForeignKey("deals.id", ondelete="CASCADE"))
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    sender_type: Mapped[str] = mapped_column(String, nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="messages")
