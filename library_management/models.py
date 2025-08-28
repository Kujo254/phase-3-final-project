from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()

DB_PATH = os.path.join(os.path.dirname(__file__), "../library.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Integer, default=1)  # 1 = available, 0 = borrowed

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.available})>"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}')>"


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    borrow_date = Column(Date)
    return_date = Column(Date, nullable=True)

    book = relationship("Book")
    member = relationship("Member")

    def __repr__(self):
        return f"<BorrowRecord(id={self.id}, book_id={self.book_id}, member_id={self.member_id}, borrow_date={self.borrow_date}, return_date={self.return_date})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully!")
