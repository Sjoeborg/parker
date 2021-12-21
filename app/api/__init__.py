from flask import Blueprint

endpoints = Blueprint('api', __name__)

# Import any endpoints here to make them available
from . import main