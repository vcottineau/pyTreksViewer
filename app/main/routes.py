from flask import render_template, flash
from flask_login import login_required


from app.main import bp


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Home')