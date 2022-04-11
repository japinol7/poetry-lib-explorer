import logging
from flask import render_template, request
from app import app

from app.services import book_service, data_service
from app.utils import setup_db
from app.utils import import_data

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

setup_db.setup_db()
total_books = book_service.get_total_poetry_books()


@app.route('/poetry-lib-books', methods=['GET', 'POST'])
def poetry_lib_books():
    global total_books
    books = []
    form_executed = None
    if request.method == 'POST' and 'poetry_book_name' in request.form:
        name = request.form.get('poetry_book_name')
        author = request.form.get('poetry_author_name')
        book_author = request.form.get('poetry_book_author')
        book = request.form.get('poetry_book_name')
        poem_name = request.form.get('poetry_poem_name')
        limit = request.form.get('poetry_book_limit')
        start_date = request.form.get('poetry_book_start_date')
        end_date = request.form.get('poetry_book_end_date') or start_date
        book_match_method = request.form.get('poetry_book_title_method')
        language = request.form.get('poetry_language')
        order_by = request.form.get('poetry_book_order_by')
        books = get_poetry_books(name, author, book, book_author, limit, poem_name, language,
                                 start_date, end_date, book_match_method, order_by)
        form_executed = 'poetry_lib_form'
    elif request.method == 'POST' and 'import_data_method' in request.form:
        import_data.import_if_empty()
        error = f"Data already imported. Books in the database: " \
                f"{total_books or book_service.get_total_poetry_books()}."
        books_res = []
        books = (('', ''), len(books_res), {}, books_res, {'error': error})
        form_executed = 'poetry_lib_import_data_form'

    return render_template('poetry_lib_books.html', books=books, form_executed=form_executed)


def get_poetry_books(name, author, book, book_author, limit, poem_name, language,
                     start_date, end_date, book_match_method, order_by):
    error = ''
    books = []
    if data_service.is_poetry_lib_imported():
        books = book_service.get_poetry_books(
            all_books=False, name=name, author=author, book=book,
            book_author=book_author, poem_name=poem_name, language=language,
            limit=limit, start_date=start_date, end_date=end_date,
            book_match_method=book_match_method, order_by=order_by)
    else:
        error = 'There is no data on the database. Please, import some data.'

    poetry_gen_data = {}
    return ((name, limit, start_date, end_date, book_match_method, order_by,
             author, book, total_books or book_service.get_total_poetry_books(),
             book_author),
            len(books), poetry_gen_data, books, {'error': error})
