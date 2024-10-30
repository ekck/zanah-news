from flask import render_template

from . import bp


@bp.route('/')

def index():

    print("Index route accessed")  # Debug print

    return render_template('index.html')