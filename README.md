# Library Management System - Phase 3 Final Project

A Command-Line Interface (CLI) Python application to manage a library. The system allows librarians to manage books, register members, and track borrow/return records using Object-Relational Mapping (ORM) with SQLAlchemy.

## Features

- Add, list, and manage books
- Add and list library members
- Record borrowing and returning of books
- View all borrow records
- Uses SQLite database with SQLAlchemy ORM
- Fully functional CLI with commands using Click

## Project Structure

LibraryManagement/
├── library_management/
│ ├── init.py
│ ├── cli.py # CLI commands
│ ├── models.py # ORM models
│ ├── database.py # Database setup
│ ├── see.py # Seed initial data
│ └── check_seed.py # Verify seeded data
├── library.db # SQLite database
├── README.md
└── setup.py

## Installation

1. Clone the repository:

```bash
git clone git@github.com:Kujo254/phase-3-final-project.git
cd phase-3-final-project


2 .Install dependencies:

pip install -e .


3. Seed the database:

python library_management/see.py

Usage

Run CLI commands via Python module or installed library-cli:

# List all books
python -m library_management.cli list-books

# List all members
python -m library_management.cli list-members

# List all borrow records
python -m library_management.cli list-records

# Add a book
python -m library_management.cli add-book "Book Title" "Author Name"

# Add a member
python -m library_management.cli add-member "Member Name"

# Borrow a book
python -m library_management.cli borrow-book <book_id> <member_id>

# Return a book
python -m library_management.cli return-book <borrow_record_id>

Database Schema

Book: id, title, author, available

Member: id, name

BorrowRecord: id, book_id, member_id, borrow_date, return_date

Relationships:

One member can have many borrow records.

One book can appear in many borrow records.

License

This project is for academic purposes.
