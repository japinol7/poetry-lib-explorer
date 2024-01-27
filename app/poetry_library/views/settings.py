import io
from datetime import datetime
import logging

from flask import render_template, send_file
import xlsxwriter

from app import app
from app.config.config import (
    EXPORT_FILE_PROPERTIES,
    POEMS_EXPORT_FIELD_TITLES,
    POEMS_EXPORT_FILE_NAME,
    EXPORT_FILE_MIMETYPE,
    )
from app.services import poem_service
from app.utils import setup_db

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

setup_db.setup_db()
total_poems = poem_service.get_total_poetry_poems()


@app.route('/settings', methods=['GET'])
def settings_view():
    return render_template('settings.html')


def _get_poems_export_field_values(poem, text_left__format, date_format):
    return [
        {'val': poem.id, 'format': None},
        {'val': poem.poem_id, 'format': None},
        {'val': poem.name, 'format': text_left__format},
        {'val': poem.author, 'format': text_left__format},
        {'val': poem.year, 'format': None},
        {'val': poem.read_count, 'format': None},
        {'val': poem.size_chars, 'format': None},
        {'val': poem.language, 'format': text_left__format},
        {'val': poem.body, 'format': text_left__format},
        {'val': poem.book_name, 'format': text_left__format},
        {'val': poem.book.author, 'format': text_left__format},
        {'val': poem.book_editor, 'format': text_left__format},
        {'val': poem.book_number, 'format': None},
        {'val': poem.book_count, 'format': None},
        {'val': poem.book.size_chars, 'format': None},
        {'val': poem.book.pages, 'format': None},
        {'val': poem.location, 'format': text_left__format},
        {'val': poem.date_released, 'format': date_format},
        {'val': poem.date_added, 'format': date_format},
        {'val': poem.date_modified, 'format': date_format},
        {'val': poem.date_imported, 'format': date_format},
        {'val': poem.comments, 'format': text_left__format},
        {'val': poem.poem_number, 'format': None},
        {'val': poem.book.poem_count, 'format': None},
        {'val': poem.is_user_added, 'format': None},
    ]


def _export_poems_report():
    logger.info("Start exporting poems report")
    poems = poem_service.get_music_poems_to_export()
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    workbook.remove_timezone = True

    workbook_properties = EXPORT_FILE_PROPERTIES.copy()
    workbook_properties['created'] = datetime.now()
    workbook.set_properties(workbook_properties)

    worksheet = workbook.add_worksheet('Poems')

    for col, field_titles in enumerate(POEMS_EXPORT_FIELD_TITLES):
        worksheet.set_column(col, col, field_titles.width)

    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    title_format = workbook.add_format({'bg_color': '#BEDFFA'})
    text_left__format = workbook.add_format({'align': 'left'})

    row = 0
    for col, field_titles in enumerate(POEMS_EXPORT_FIELD_TITLES):
        worksheet.write(row, col, field_titles.name, title_format)

    row = 1
    for poem in poems:
        col_fields = _get_poems_export_field_values(poem, text_left__format, date_format)
        for col, col_field in enumerate(col_fields):
            worksheet.write(row, col, col_field['val'], col_field['format'])
        row += 1

    workbook.close()
    buffer.seek(0)
    logger.info("Exporting poems report: Report ready to send.")

    return send_file(buffer, as_attachment=True,
                     download_name=POEMS_EXPORT_FILE_NAME,
                     mimetype=EXPORT_FILE_MIMETYPE)


@app.route('/export_poems_report', methods=['GET'])
def export_poems_report():
    res, error_msg = None, None
    is_error = False
    try:
        res = _export_poems_report()
    except Exception as e:
        is_error = True
        error_msg = "Error exporting poems data"
        logger.error("%s. Error msg: %s", error_msg, e)

    return res or render_template('settings.html',
                                  is_error=is_error,
                                  error_msg=error_msg)
