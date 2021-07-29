from flask import Blueprint

api = Blueprint("api", __name__)

from . import views
from .main import routes