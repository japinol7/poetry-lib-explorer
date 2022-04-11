from app.data import session_factory
from app.data.models.book import Book
from app.config import config


def get_total_poetry_books():
    session = session_factory.create_session()
    return session.query(Book).count() or 0


def get_poetry_books(all_books=False, name=None, author=None, book=None, book_author=None,
                     poem_name=None, language=None,
                     limit=None, start_date=None, end_date=None,
                     book_match_method=None, order_by=None):
    session = session_factory.create_session()
    # noinspection PyComparisonWithNone
    if all_books:
        books = session.query(Book).filter(Book.id > 0).all()
        return books if books else []

    books = session.query(Book)
    if book_match_method == 'book_contains':
        books = books.filter(Book.name.contains(name))
    elif book_match_method == 'book_starts_with':
        books = books.filter(Book.name.startswith(name))
    elif book_match_method == 'book_exact_match':
        books = books.filter(Book.name == name)

    if author:
        books = books.filter(Book.author_poems.contains(author))

    if book_author:
        books = books.filter(Book.author.contains(book_author))

    if book:
        books = books.filter(Book.name.contains(book_author))

    if poem_name:
        books = books.filter(Book.poem_names.contains(poem_name))

    if language and language != 'All':
        books = books.filter(Book.language_internal.contains(
            f'{config.LANGUAGE_WRAPPER}{language}{config.LANGUAGE_WRAPPER}'))

    if start_date and start_date[:4].isnumeric():
        books = books.filter(Book.year >= int(start_date[:4]))

    if end_date and end_date[:4].isnumeric():
        books = books.filter(Book.year <= int(end_date[:4]))

    if order_by == 'bookName':
        books = books.order_by(Book.name)
    elif order_by == 'author,bookName':
        books = books.order_by(Book.author, Book.name)
    elif order_by == 'size_chars,bookName':
        books = books.order_by(Book.size_chars.desc(), Book.name)
    elif order_by == 'year,bookName':
        books = books.order_by(Book.year, Book.name)

    if limit:
        books = books.limit(limit)

    books = books.all()
    return books if books else []
