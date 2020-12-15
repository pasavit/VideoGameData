from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from flask_bootstrap import Bootstrap
from . import api_request

bp = Blueprint('sample', __name__)


@bp.route('/test')
def test():
    return "All good!"


@bp.route('/sample')
def index():
    message = "This text is coming from the 'sample.py' module, not the html file!"
    phrase = "Python is cool!"
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales')
    data = (
        ('Wii Sports', 'Wii', '2006', 'Sports', 'Nintendo', '82.53'),
        ('GTA', 'PS3', '2008', 'Action', 'Rockstar', '55.6')
    )
    return render_template('sample/index.html', message=message, word=phrase, headings=headings, data=data)


@bp.route('/postform', methods=('GET', 'POST'))
def other_example():
    if request.method == 'POST':
        page_title = request.form['title']
        error = None

        if not page_title:
            error = 'You must enter a title'

        if error is not None:
            flash(error)
        elif request.form['title'] == "go home":
            return redirect(url_for('sample.index'))
        else:
            return render_template('sample/postform.html', page_title=page_title)

    else:
        return render_template('sample/postform.html', page_title="PostForm from Module Function")

