import datetime

import sqlalchemy
from sqlalchemy.orm import relationship

from app.data.sqlalchemybase import SqlAlchemyBase


class Poem(SqlAlchemyBase):
    __tablename__ = 'poem'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    poem_id = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True, unique=True)
    persistent_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)
    x_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)

    # Foreign keys
    book_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('book.id'))
    book = relationship('Book', back_populates='poems', lazy='joined')

    # Normal columns
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    poem_number = sqlalchemy.Column(sqlalchemy.Integer)
    poem_count = sqlalchemy.Column(sqlalchemy.Integer)
    size_chars = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    language = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body_very_short = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body_short = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    book_name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    book_author = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    book_editor = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    book_number = sqlalchemy.Column(sqlalchemy.Integer)
    book_count = sqlalchemy.Column(sqlalchemy.Integer)
    book_size_chars = sqlalchemy.Column(sqlalchemy.Integer)
    book_pages = sqlalchemy.Column(sqlalchemy.Integer)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_released = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_modified = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_imported = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    read_count = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    sort_book = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_user_added = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f"Poem(id={self.id!r}, " \
               f"poem_id={self.poem_id!r}, " \
               f"name={self.name!r}, " \
               f"author={self.author!r})"
