import click
from datetime import date
from .models import session, Book, Member, BorrowRecord

@click.group()
def cli():
    """Library Management System CLI"""
    pass

# ---- Book commands ----
@cli.command()
def list_books():
    books = session.query(Book).all()
    if not books:
        click.echo("No books found.")
        return
    click.echo("📚 Books in library:")
    for b in books:
        status = "Available" if b.available else "Checked Out"
        click.echo(f"{b.id}. {b.title} by {b.author} ({status})")

@cli.command()
@click.argument("title")
@click.argument("author")
def add_book(title, author):
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    click.echo(f"✅ Added book: {title} by {author}")

# ---- Member commands ----
@cli.command()
def list_members():
    members = session.query(Member).all()
    if not members:
        click.echo("No members found.")
        return
    click.echo("👤 Members:")
    for m in members:
        click.echo(f"{m.id}. {m.name}")

@cli.command()
@click.argument("name")
def add_member(name):
    member = Member(name=name)
    session.add(member)
    session.commit()
    click.echo(f"✅ Added member: {name}")

# ---- Borrow/Return commands ----
@cli.command()
@click.argument("book_id", type=int)
@click.argument("member_id", type=int)
def borrow_book(book_id, member_id):
    book = session.query(Book).filter_by(id=book_id).first()
    member = session.query(Member).filter_by(id=member_id).first()
    if not book or not member:
        click.echo("⚠️ Invalid book or member ID.")
        return
    if not book.available:
        click.echo(f"⚠️ '{book.title}' is already borrowed.")
        return
    book.available = 0
    record = BorrowRecord(book=book, member=member, borrow_date=date.today())
    session.add(record)
    session.commit()
    click.echo(f"✅ {member.name} borrowed '{book.title}'.")

@cli.command()
@click.argument("book_id", type=int)
def return_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        click.echo("⚠️ Invalid book ID.")
        return
    record = session.query(BorrowRecord).filter_by(book_id=book_id, return_date=None).first()
    if not record:
        click.echo("⚠️ This book was not borrowed.")
        return
    record.return_date = date.today()
    book.available = 1
    session.commit()
    click.echo(f"✅ '{book.title}' has been returned.")

@cli.command()
def list_records():
    records = session.query(BorrowRecord).all()
    if not records:
        click.echo("No records found.")
        return
    click.echo("📄 Borrow Records:")
    for r in records:
        status = r.return_date if r.return_date else "Not returned"
        click.echo(f"{r.id}. {r.member.name} -> {r.book.title} | Borrowed: {r.borrow_date} | Returned: {status}")

if __name__ == "__main__":
    cli()
