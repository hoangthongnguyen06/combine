from flask import Blueprint, request, jsonify
from app.services.target import *

bp_targets = Blueprint('targets', __name__)


