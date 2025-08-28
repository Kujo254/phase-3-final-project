from models import session, Book, Member, BorrowRecord

# List all books
print("📚 Books in Library:")
for book in session.query(Book).all():
    status = "Available" if book.available else "Borrowed"
    print(f"{book.id}: {book.title} by {book.author} ({status})")

# List all members
print("\n👥 Library Members:")
for member in session.query(Member).all():
    print(f"{member.id}: {member.name}")

# List all borrow records
print("\n📝 Borrow Records:")
for record in session.query(BorrowRecord).all():
    returned = record.return_date if record.return_date else "Not returned yet"
    print(f"{record.id}: Book '{record.book.title}' borrowed by {record.member.name} on {record.borrow_date}, returned on {returned}")
