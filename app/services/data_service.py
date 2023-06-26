from app.data import session_factory
from app.data.models.poem import Poem


def is_poetry_lib_imported():
    session = session_factory.create_session()
    poem = session.query(Poem).first()
    return poem and True or False
