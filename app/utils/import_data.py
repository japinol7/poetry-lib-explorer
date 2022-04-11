from collections import Counter
import logging
from zipfile import ZipFile

from app.data import session_factory
from app.data.models.poem import Poem
from app.data.models.book import Book
from app.data.models.user import User
from app.services import user_service
from app.data.dataset.csv_dataset import CsvDataset
from app.config import config
from app.config.config import ALLOW_TO_IMPORT_SEVERAL_FILES
from app.utils.utils import str_to_html

logging.basicConfig(format=config.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ImportDataException(Exception):
    pass


def import_if_empty():
    __unzip_data_files()
    __import_poetry_poems()
    __import_users()


def __unzip_data_files():
    session = session_factory.create_session()
    if session.query(Poem).count() > 0:
        return

    logger.info(f"Unzip database files")
    try:
        with ZipFile(config.DATASET_FILE_ZIP) as fin_zip:
            fin_zip.extractall(config.RESOURCES_FOLDER)
    except FileNotFoundError:
        raise ImportDataException(f"Error extracting database files. File not found: {config.DATASET_FILE_ZIP}")
    except Exception as e:
        raise ImportDataException(f"Error extracting database files from: {config.DATASET_FILE_ZIP}. Error msg: {e}")


def __get_dataset_from_csv():
    with open(config.DATASET_FILE, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data).get_grouped(config.COLUMN_TO_GROUP_BY)


def __get_dataset_from_json():
    with open(config.DATASET_FILE, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data).get_grouped(config.COLUMN_TO_GROUP_BY)


def __import_poetry_poems():
    session = session_factory.create_session()
    if not ALLOW_TO_IMPORT_SEVERAL_FILES and session.query(Poem).count() > 0:
        return

    logger.info(f"Start to Import poetry lib poems file")
    if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_CSV:
        dataset = __get_dataset_from_csv()
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_JSON:
        dataset = __get_dataset_from_json()
    else:
        raise ImportDataException(f"Internal Error extracting database files. "
                                  f"Source Format not supported: {config.DATASET_SOURCE_FORMAT}")

    count_books = 0
    count_poems = 0
    for key, rows in dataset:
        if not key:
            continue
        count_books += 1
        rows_list = list(rows)
        book = Book()
        book.name = rows_list[0]['book']
        book.author = rows_list[0]['book_author'] if rows_list[0]['book_author'] else None
        book.book_count_total = int(rows_list[0]['book_count']) if rows_list[0]['book_count'] else 0
        book.poem_count_total = int(rows_list[0]['poem_count']) if rows_list[0]['poem_count'] else 0
        book.pages = rows_list[0]['book_pages'] or None
        poem_count_total = Counter()
        book.year_max = max([x['year'] for x in rows_list])
        book.year_min = min([x['year'] for x in rows_list])
        book.year = book.year_min
        author_poems = set()
        language = set()
        language_internal = set()
        book_editor = set()
        book.poem_names = []
        book_poem_count = 0
        book.size_chars = 0
        for row in rows_list:
            if not row['name']:
                # If some required columns are missing, it is probably not an audio poem. It may be a video
                continue
            count_poems += 1
            book_poem_count += 1
            poem = Poem()
            poem.name = row['name']
            poem.book = book
            poem.author = row['author']
            poem.poem_number = int(row['poem_number']) if row['poem_number'] else 0
            poem.book_count = int(row['book_count']) if row['book_count'] else 0
            poem.poem_number = int(row['poem_number']) if row['poem_number'] else 0
            poem.poem_count = int(row['poem_count']) if row['poem_count'] else 0
            poem_count_total[poem.poem_number] = poem.poem_count
            poem.year = row['year']
            poem.book_editor = row['book_editor']
            poem.language = row['language']
            poem.body = row['body'] or ''
            poem.body_very_short = get_body_very_short_piece(poem.body)
            poem.body_short = get_body_short_piece(poem.body)
            poem.read_count = row['read_count'] and int(row['read_count']) or 0
            poem.date_released = row['date_released']
            poem.date_modified = row['date_modified']
            poem.date_added = row['date_added']
            poem.is_user_added = int(row['is_user_added'] or 0) and True or False
            poem.comments = row['comments']
            if row['location'] and config.FILE_LOCATION_REPLACE.old:
                poem.location = row['location'].replace(
                    config.FILE_LOCATION_REPLACE.old,
                    config.FILE_LOCATION_REPLACE.new)
            else:
                poem.location = row['location']
            poem.persistent_id = row['persistent_id'] if row['persistent_id'] else None
            poem.poem_id = row['poem_id']
            poem.sort_book = row['sort_book']
            poem.sort_author = row['sort_author']
            poem.sort_name = row['sort_name']
            poem.size_chars = len(row['body'])
            poem.x_id = config.DELIMITER.join([
                row['persistent_id'] or row['poem_id'] or '',
                f"{poem.size_chars or 0:07d}",
                ])
            session.add(poem)
            poem.book_name = book.name
            if poem.author:
                author_poems.add(poem.author)
            if poem.language:
                language.add(poem.language)
                language_internal.add(f'{config.LANGUAGE_WRAPPER}{poem.language}{config.LANGUAGE_WRAPPER}')
            if poem.book_editor:
                book_editor.add(poem.book_editor)
            book.poem_names += [poem.name]
            book.size_chars += poem.size_chars
            book.poem_count = book_poem_count

        book.author_poems = config.DELIMITER.join(list(author_poems))
        book.poems_on_discs = str(dict(sorted(poem_count_total.items())))
        book.poem_count_total = sum(poem_count_total.values())
        book.poem_names = '\n'.join(sorted(book.poem_names))
        book.language = ', '.join(list(language))
        book.language_internal = ', '.join(list(language_internal))
        book.book_editor = config.DELIMITER.join(list(book_editor))

        book.x_id = config.DELIMITER.join([
            str(count_books),
            book.author,
            book.name,
            ])
        logger.info(f"Adding book num {count_books:6} to database: {key}")
        session.add(book)

    logger.info("Committing to database")
    session.commit()
    logger.info(f"End Import poetry lib poems file")


def get_body_very_short_piece(text):
    max_chars_to_get = 80
    res = text.partition('\n')[0]
    if len(res) > max_chars_to_get:
        res = res[:max_chars_to_get]
    return res.strip()


def get_body_short_piece(text):
    max_chars_to_get = 320
    res = text.split('\n')
    res = '\n'.join(res[:4])
    if len(res) > max_chars_to_get:
        res = res[:max_chars_to_get]
    return res.strip()


def __import_users():
    session = session_factory.create_session()
    if session.query(User).count() > 0:
        return

    user_service.get_default_user()

    user2 = User()
    user2.email = 'test_user_2@test.test.com.test'
    user2.name = 'User 2'
    session.add(user2)
    session.commit()
