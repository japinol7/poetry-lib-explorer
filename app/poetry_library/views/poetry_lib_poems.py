import logging
import pyperclip

from flask import render_template, request
from app import app

from app.services import data_service, poem_service
from app.utils import setup_db
from app.utils import import_data

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

setup_db.setup_db()
total_poems = poem_service.get_total_poetry_poems()


@app.route('/poetry-lib-poems', methods=['GET', 'POST'])
def poetry_lib_poems():
    global total_poems
    poems = []
    form_executed = None
    if request.method == 'POST' and 'poetry_poem_title' in request.form:
        name = request.form.get('poetry_poem_title')
        author = request.form.get('poetry_author_name')
        book_author = request.form.get('poetry_book_author')
        book = request.form.get('poetry_book_name')
        limit = request.form.get('poetry_poem_limit')
        start_date = request.form.get('poetry_poem_start_date')
        end_date = request.form.get('poetry_poem_end_date') or start_date
        poem_match_method = request.form.get('poetry_poem_title_method')
        poem_user_added = request.form.get('poetry_poem_user_added')
        poem_body = request.form.get('poetry_poem_body')
        language = request.form.get('poetry_language')
        order_by = request.form.get('poetry_poem_order_by')
        poems = get_poetry_poems(name, author, book, book_author, limit, poem_body, language,
                                 start_date, end_date, poem_match_method, poem_user_added, order_by)
        form_executed = 'poetry_lib_form'
    elif request.method == 'POST' and 'import_data_method' in request.form:
        import_data.import_if_empty()
        error = f"Data already imported. Poems in the database: {total_poems or poem_service.get_total_poetry_poems()}."
        poems_res = []
        poems = (('', ''), len(poems_res), {}, poems_res, {'error': error})
        form_executed = 'poetry_lib_import_data_form'
    elif request.method == 'POST' and 'poetry_poem_full_body' in request.form:
        poem_name = request.form.get('poetry_poem_cp_title') or '[no poem title]'
        poem_body = request.form.get('poetry_poem_full_body') or ''
        poem_author = request.form.get('poetry_author_cp_name') or ''
        poem_year = request.form.get('poetry_poem_cp_year') or ''
        if poem_body:
            pyperclip.copy(get_poem_to_str(poem_name, poem_body, poem_year, poem_author))
        form_executed = 'poetry_poem_copy_body_form'
    return render_template('poetry_lib_poems.html', poems=poems, form_executed=form_executed)


def get_poetry_poems(name, author, book, book_author, limit, poem_body, language,
                     start_date, end_date, poem_match_method, poem_user_added, order_by):
    error = ''
    poems = []
    if data_service.is_poetry_lib_imported():
        poems = poem_service.get_poetry_poems(
                    all_poems=False, name=name, author=author, book=book,
                    book_author=book_author, poem_body=poem_body, language=language,
                    limit=limit, start_date=start_date, end_date=end_date,
                    poem_match_method=poem_match_method, poem_user_added=poem_user_added,
                    order_by=order_by)
    else:
        error = 'There is no data on the database. Please, import some data.'

    poetry_gen_data = {}
    return ((name, limit, start_date, end_date, poem_match_method, order_by,
             author, book, total_poems or poem_service.get_total_poetry_poems(),
             book_author, poem_user_added, poem_body, language),
            len(poems), poetry_gen_data, poems, {'error': error})


def get_poem_to_str(name, body, year, author):
    return ''.join([name,
                    '\n',
                    '-' * len(name),
                    '\n\n',
                    body,
                    f"\n(c) {year} {author}\n"
                    ])
