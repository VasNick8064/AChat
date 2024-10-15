# from sqlalchemy import String, Integer
# from sqlalchemy.orm import Mapped, mapped_column
# from database import Base
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     hashed_password: Mapped[str] = mapped_column(String, nullable=False)
#     email: Mapped[str] = mapped_column(String, nullable=False)
#
# class Message(Base):
#     __tablename__ = 'messages'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     content: Mapped[str] = mapped_column(Text)