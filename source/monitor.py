from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from source.authentication import login_required
from source.database import get_db

bp = Blueprint('monitor', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT  p.id, source, created, returnCode, fileType, body '
        'FROM report p ORDER BY created DESC'
    ).fetchall()
    
    return render_template('monitor/index.html', posts=posts)

# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO report (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('monitor.index'))

#     return render_template('monitor/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, source, created, returnCode, fileType, body'
        ' FROM report p WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE report SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('monitor.index'))

    return render_template('monitor/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM report WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('monitor.index'))