from flask import Flask

app = Flask(__name__)

from . import views
from . import poetry_library
