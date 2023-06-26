import datetime
import sqlalchemy
from sqlalchemy import orm

from app.data.sqlalchemybase import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'book'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    x_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)

    # Foreign keys
    poems = orm.relationship("Poem", back_populates="book", lazy='select')

    # Normal columns
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    author_poems = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    language = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    language_internal = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    poem_count = sqlalchemy.Column(sqlalchemy.Integer)
    poem_count_total = sqlalchemy.Column(sqlalchemy.Integer)
    books_count_total = sqlalchemy.Column(sqlalchemy.Integer)
    poem_names = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size_chars = sqlalchemy.Column(sqlalchemy.Integer)
    pages = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    year_min = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    year_max = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    date_imported = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    def __repr__(self):
        return f"Book(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"author={self.author!r})"
