from flask import Blueprint
from flask_restplus import Api

# blueprint = Blueprint('api', __name__)
# api = Api(blueprint)

api = Blueprint("api", __name__)

from . import views
from .main import routes