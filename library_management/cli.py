import click
from datetime import date
from .models import session, Book, Member, BorrowRecord

@click.group()
def cli():
    """Library Management System CLI"""
    pass

# ---- Utility functions ----
def list_books_table():
    books = session.query(Book).all()
    if not books:
        click.echo("No books found.")
        return
    click.echo("Books in library:")
    for b in books:
        status = "Available" if b.available else "Checked Out"
        click.echo(f"{b.id}. {b.title} by {b.author} ({status})")

def list_members_table():
    members = session.query(Member).all()
    if not members:
        click.echo("No members found.")
        return
    click.echo("Members:")
    for m in members:
        click.echo(f"{m.id}. {m.name}")

def list_records_table():
    records = session.query(BorrowRecord).all()
    if not records:
        click.echo("No records found.")
        return
    click.echo("Borrow Records:")
    for r in records:
        status = r.return_date if r.return_date else "Not returned"
        click.echo(f"{r.id}. {r.member.name} -> {r.book.title} | Borrowed: {r.borrow_date} | Returned: {status}")

# ---- CLI commands ----
@cli.command()
def list_books():
    list_books_table()

@cli.command()
def add_book():
    title = click.prompt("Enter book title")
    author = click.prompt("Enter book author")
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    click.echo(f"Added book successfully: {title} by {author}")

@cli.command()
def list_members():
    list_members_table()

@cli.command()
def add_member():
    name = click.prompt("Enter member name")
    member = Member(name=name)
    session.add(member)
    session.commit()
    click.echo(f"Added member successfully: {name}")

@cli.command()
def borrow_book():
    list_books_table()
    book_id = click.prompt("Enter book ID to borrow", type=int)
    list_members_table()
    member_id = click.prompt("Enter member ID borrowing the book", type=int)

    book = session.query(Book).filter_by(id=book_id).first()
    member = session.query(Member).filter_by(id=member_id).first()

    if not book or not member:
        click.echo("Invalid book or member ID.")
        return
    if not book.available:
        click.echo(f"'{book.title}' is already borrowed.")
        return

    book.available = 0
    record = BorrowRecord(book=book, member=member, borrow_date=date.today())
    session.add(record)
    session.commit()
    click.echo(f"{member.name} borrowed '{book.title}' successfully.")

@cli.command()
def return_book():
    list_books_table()
    book_id = click.prompt("Enter book ID to return", type=int)
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        click.echo("Invalid book ID.")
    elif book.available:
        click.echo(f"'{book.title}' is already available and cannot be returned.")
    else:
        record = session.query(BorrowRecord).filter_by(book_id=book_id, return_date=None).first()
        if not record:
            click.echo("Error: Borrow record not found.")
        else:
            record.return_date = date.today()
            book.available = 1
            session.commit()
            click.echo(f"'{book.title}' returned successfully.")

@cli.command()
def list_records():
    list_records_table()

# ---- Interactive menu ----
@click.command()
def menu():
    """Interactive menu to manage library"""
    while True:
        click.echo("\n===================================")
        click.echo("       LIBRARY MANAGEMENT SYSTEM   ")
        click.echo("===================================")
        click.echo("1. List books")
        click.echo("2. Add book")
        click.echo("3. List members")
        click.echo("4. Add member")
        click.echo("5. Borrow book")
        click.echo("6. Return book")
        click.echo("7. List borrow records")
        click.echo("0. Exit")

        choice = click.prompt("Enter choice", type=int)

        if choice == 1:
            list_books_table()
        elif choice == 2:
            title = click.prompt("Enter book title")
            author = click.prompt("Enter book author")
            book = Book(title=title, author=author)
            session.add(book)
            session.commit()
            click.echo(f"Added book successfully: {title} by {author}")
        elif choice == 3:
            list_members_table()
        elif choice == 4:
            name = click.prompt("Enter member name")
            member = Member(name=name)
            session.add(member)
            session.commit()
            click.echo(f"Added member successfully: {name}")
        elif choice == 5:
            list_books_table()
            book_id = click.prompt("Enter book ID to borrow", type=int)
            list_members_table()
            member_id = click.prompt("Enter member ID borrowing the book", type=int)

            book = session.query(Book).filter_by(id=book_id).first()
            member = session.query(Member).filter_by(id=member_id).first()

            if not book or not member:
                click.echo("Invalid book or member ID.")
            elif not book.available:
                click.echo(f"'{book.title}' is already borrowed.")
            else:
                book.available = 0
                record = BorrowRecord(book=book, member=member, borrow_date=date.today())
                session.add(record)
                session.commit()
                click.echo(f"{member.name} borrowed '{book.title}' successfully.")
        elif choice == 6:
            list_books_table()
            book_id = click.prompt("Enter book ID to return", type=int)
            book = session.query(Book).filter_by(id=book_id).first()
            if not book:
                click.echo("Invalid book ID.")
            elif book.available:
                click.echo(f"'{book.title}' is already available and cannot be returned.")
            else:
                record = session.query(BorrowRecord).filter_by(book_id=book_id, return_date=None).first()
                if not record:
                    click.echo("Error: Borrow record not found.")
                else:
                    record.return_date = date.today()
                    book.available = 1
                    session.commit()
                    click.echo(f"'{book.title}' returned successfully.")
        elif choice == 7:
            list_records_table()
        elif choice == 0:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Try again.")

cli.add_command(menu)

if __name__ == "__main__":
    cli()
