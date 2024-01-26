from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import false, true

from app.data import session_factory
from app.data.models.poem import Poem
from app.data.models.book import Book


def get_total_poetry_poems():
    session = session_factory.create_session()
    return session.query(Poem).count() or 0


def get_poetry_poems(all_poems=False, name=None, author=None, book=None, book_author=None,
                    poem_body=None, language=None,
                    limit=None, start_date=None, end_date=None,
                    poem_match_method=None, poem_user_added=None, order_by=None):

    # noinspection PyComparisonWithNone
    session = session_factory.create_session()

    poems = session.query(Poem)
    # Use joined loading instead of lazy loading to prevent DetachedInstanceError error when reloading page
    poems = poems.options(joinedload(Poem.book))
    poems = poems.join(Poem.book)

    if all_poems:
        poems.filter(Poem.id > 0).all()
        return poems if poems else []

    if poem_match_method == 'poem_contains':
        poems = poems.filter(Poem.name.contains(name))
    elif poem_match_method == 'poem_starts_with':
        poems = poems.filter(Poem.name.startswith(name))
    elif poem_match_method == 'poem_exact_match':
        poems = poems.filter(Poem.name == name)

    if poem_user_added == 'Added by user':
        poems = poems.filter(Poem.is_user_added == true())
    elif poem_user_added == 'Automatically added':
        poems = poems.filter(Poem.is_user_added == false())

    if author:
        poems = poems.filter(Poem.author.contains(author))

    if book:
        poems = poems.filter(Book.name.contains(book))

    if book_author:
        poems = poems.filter(Book.author.contains(book_author))

    if poem_body:
        poems = poems.filter(Poem.body.contains(poem_body))

    if language and language != 'All':
        poems = poems.filter(Poem.language.like(language))

    if start_date and start_date[:4].isnumeric():
        poems = poems.filter(Poem.year >= int(start_date[:4]))

    if end_date and end_date[:4].isnumeric():
        poems = poems.filter(Poem.year <= int(end_date[:4]))

    if order_by == 'poemName':
        poems = poems.order_by(Poem.name)
    elif order_by == 'book,poemName':
        poems = poems.order_by(Book.name, Poem.name)
    elif order_by == 'author,book,poemName':
        poems = poems.order_by(Poem.author, Book.name, Poem.name)
    elif order_by == 'author,poemName':
        poems = poems.order_by(Poem.author, Poem.name)
    elif order_by == 'read_count,author,poemName':
        poems = poems.order_by(Poem.read_count.desc(), Poem.author, Poem.name)
    elif order_by == 'size_chars,poemName':
        poems = poems.order_by(Poem.size_chars.desc(), Poem.name)
    elif order_by == 'year,poemName':
        poems = poems.order_by(Poem.year, Poem.name)

    if limit:
        poems = poems.limit(limit)

    poems = poems.all()
    return poems if poems else []


def get_music_poems_to_export():
    poems = get_poetry_poems(all_poems=True)
    poems = poems.order_by(Poem.read_count.desc(), Poem.author, Poem.name, Poem.year)
    return poems if poems else []
