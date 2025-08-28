from datetime import date
from library_management.models import session, Book, Member, BorrowRecord, Base, engine

def seed_data():
    # Drop all tables and recreate them for a clean slate
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create books
    book1 = Book(title="1984", author="George Orwell")
    book2 = Book(title="To Kill a Mockingbird", author="Harper Lee")
    book3 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald")

    # Create members
    member1 = Member(name="Alice Johnson")
    member2 = Member(name="Bob Smith")

    # Create borrow records
    record1 = BorrowRecord(book=book1, member=member1, borrow_date=date(2025, 8, 1))
    record2 = BorrowRecord(book=book2, member=member2, borrow_date=date(2025, 8, 5), return_date=date(2025, 8, 20))

    # Add all to session
    session.add_all([book1, book2, book3, member1, member2, record1, record2])
    session.commit()
    print("Database seeded with fresh data!")

if __name__ == "__main__":
    seed_data()
