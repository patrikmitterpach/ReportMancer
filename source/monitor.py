from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify
)
from werkzeug.exceptions import abort

import configparser
import xmltodict, json
import time
from datetime import datetime

from source.authentication import login_required
from source.database import get_db

bp = Blueprint('monitor', __name__)

config = configparser.ConfigParser()
config.read('config.ini')

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT  p.id, source, created, fileType, fullBody '
        'FROM report p ORDER BY id DESC'
    ).fetchall()
    print(posts[0]["fullBody"])
    return render_template('monitor/index.html', posts=posts, download=(config["Export"]["download_available"] == "True"))

@bp.route('/export_all', methods=['GET'])
@login_required
def download_all():
    db = get_db()
    posts = db.execute(
        'SELECT  p.id, source, created, fileType, fullBody '
        'FROM report p ORDER BY id DESC'
    ).fetchall()
    
    data = {}
    print(posts[1]["fullBody"])
    for post in posts:
        if "xml" in post["fileType"]:
            data.update({str(post["id"]): {"date": post["created"].strftime("%Y-%m-%d %H-%M-%S"), "type": "DMARC Aggregate Report", "data": xmltodict.parse(post["fullBody"].replace("\n", ""))}})
        else:
            data.update({str(post["id"]):{"date": post["created"].strftime("%Y-%m-%d %H-%M-%S"), "type": "ReportingAPI", "data": json.loads(post["fullBody"].strip())}})


    date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    return jsonify(data)
    return render_template('base.html')



@bp.route('/<int:id>', methods=['GET'])
@login_required
def view_full(id):
    report = get_db().execute(
        'SELECT p.id, source, created, fileType, fullBody'
        ' FROM report p WHERE p.id = ?',
        (id,)
    ).fetchone()
    return render_template('monitor/view.html', report=report)
