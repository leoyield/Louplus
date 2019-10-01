from flask import render_template, Blueprint
from simpledu.models import Live

live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
    live = Live.query.order_by(Live.id.desc()).first()
    return render_template('live/index.html', live=live)
