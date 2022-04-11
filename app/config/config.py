import os
import pathlib

from collections import namedtuple, OrderedDict

LOGGER_FORMAT = '%(levelname)s: %(message)s'
STR_ENCODING = 'utf-8'

DATASET_SOURCE_FORMAT = 'csv'

DELIMITER_CSV = ','
DECIMAL_SEPARATOR_CSV = '.'
THOUSANDS_SEPARATOR_CSV = '.' if DECIMAL_SEPARATOR_CSV == ',' else ','

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
RESOURCES_FOLDER = os.path.join(ROOT_FOLDER, 'resources')
DATASET_FOLDER = os.path.join(ROOT_FOLDER, 'resources', 'data')
DATASET_FOLDER_ZIP = os.path.join(DATASET_FOLDER, 'zip')
DATASET_FILE_ZIP = os.path.join(DATASET_FOLDER_ZIP, 'data.zip')

DELIMITER = '.||.'
LANGUAGE_WRAPPER = '||'

DATASET_FILE_NAME = 'poetry_dig_lib'
DATASET_FILE = os.path.join(DATASET_FOLDER, f'{DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

DATASET_SOURCE_CSV = 'csv'
DATASET_SOURCE_JSON = 'json'
ColumnsMapping = namedtuple('columns_mapping', [DATASET_SOURCE_CSV, DATASET_SOURCE_JSON])
COLUMNS_MAPPING = OrderedDict({
    'name': ColumnsMapping('name', 'name'),
    'author': ColumnsMapping('author', 'author'),
    'poem_id': ColumnsMapping('poem_id', 'poemId'),
    'poem_number': ColumnsMapping('poem_number', 'poemNumber'),
    'poem_count': ColumnsMapping('poem_count', 'poemCount'),
    'size_chars': ColumnsMapping('size_chars', 'sizeChars'),
    'language': ColumnsMapping('language', 'language'),
    'year': ColumnsMapping('year', 'year'),
    'body': ColumnsMapping('body', 'body'),
    'book_author': ColumnsMapping('book_author', 'bookAuthor'),
    'book_editor': ColumnsMapping('book_editor', 'bookEditor'),
    'book': ColumnsMapping('book', 'book'),
    'book_number': ColumnsMapping('book_number', 'bookNumber'),
    'book_count': ColumnsMapping('book_count', 'bookCount'),
    'book_size_chars': ColumnsMapping('book_size_chars', 'bookSizeChars'),
    'book_pages': ColumnsMapping('book_pages', 'bookPages'),
    'date_released': ColumnsMapping('date_released', 'dateReleased'),
    'date_added': ColumnsMapping('date_added', 'dateAdded'),
    'date_modified': ColumnsMapping('date_modified', 'dateModified'),
    'comments': ColumnsMapping('comments', 'comments'),
    'read_count': ColumnsMapping('read_count', 'readCount'),
    'persistent_id': ColumnsMapping('persistent_id', 'persistentId'),
    'x_id': ColumnsMapping('x_id', 'xId'),
    'location': ColumnsMapping('location', 'location'),
    'sort_book': ColumnsMapping('sort_book', 'sortBook'),
    'sort_author': ColumnsMapping('sort_author', 'sortAuthor'),
    'sort_name': ColumnsMapping('sort_name', 'sortName'),
    'is_user_added': ColumnsMapping('is_user_added', 'isUserAdded'),
    })

COLUMN_TO_GROUP_BY = 'author_and_book'

ColumnToAddToGroup = namedtuple('column_to_add_to_group', ['new_column', 'column1', 'column2'])
COLUMN_TO_ADD_TO_GROUP = ColumnToAddToGroup('author_and_book', 'book_author', 'book')

DATE_COLUMNS = ['date_released', 'date_added', 'date_modified']
AMOUNT_COLUMNS = []
COLUMNS_TO_STRIP_WHITESPACE_FROM = []

# Adjustments to a particular dataset. Added here for convenience
READ_COUNT_TO_ADD_ALL_POEMS = 0
FileLocationReplace = namedtuple('file_location_replace', ['old', 'new'])
FILE_LOCATION_REPLACE = FileLocationReplace('', '')
ALLOW_TO_IMPORT_SEVERAL_FILES = False
IS_USER_ADDED = False
# End Adjustments to a particular dataset
