from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import xmltodict, json
import time
import logging

from datetime import datetime
import xml.etree.ElementTree as ET

from source.authentication import login_required
from source.database import get_db

# Setup logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

from source.export import export_report

bp = Blueprint('input', __name__)

VALID_CONTENT_TYPES = ["text/json", "text/xml"]

def commitReportToDatabase(url, timeStamp, fileType, data):
    db = get_db()
    # According to flask documentation, 
    #  this should be immune to SQL injections 
    #  as the inputs are parametrized
    db.execute(
    'INSERT INTO report (source, created, fileType, fullBody)'
    ' VALUES (?, ?, ?, ?)',
    (url, timeStamp, fileType, data)
    )
    db.commit()

    


def validateRequest(request):
    print(request)
    print(request.data)

    if not request.data:
        return 400, "Empty request"
    
    if not request.content_type:
        return 400, "No content type given"
    if request.content_type.lower() not in VALID_CONTENT_TYPES:
        return 400, "Content type not accepted"
    
    if "json" in request.content_type.lower():
        try: json.loads(request.data)
        except ValueError:
            return 400, "Invalid JSON"
    if "xml" in request.content_type:
        try:    
            tree = ET.fromstring(request.data)
        except ET.ParseError:
            return 400, "Invalid XML"
        
    return 200, "Success"

@bp.route('/', methods=['POST'])
def index():
    returnCode, returnMessage = validateRequest(request)
    if returnCode != 200:
        return json.dumps(
            {'Result': returnMessage}
        ), returnCode, {'ContentType':'application/json'}

    assert request.content_type.lower() in VALID_CONTENT_TYPES

    if "json" in request.content_type.lower():
        json_data = json.loads(request.data)
        ## Assume ReportingAPI report
        url = json_data["url"]
        
        # Time is current time - age, given in request
        currentTimeMinusAge = int(time.time()) - json_data["age"]
        timeStamp = datetime.fromtimestamp(currentTimeMinusAge).strftime('%Y-%m-%d %H:%M:%S')

        fileType = request.content_type
        commitReportToDatabase(url, timeStamp, fileType, json.dumps(json_data, indent=4))

        json_data = {"type": "ReportingAPI", "data": json_data}
        

    elif "xml" in request.content_type.lower():
        data = request.data
        root = ET.fromstring(data)
        print("PRINTING HERE")
        print(root)
        print(len(root.findall('record')))
        for child in root.findall('record'):
            print(child.tag)
            url = child.find("identifiers").find("header_from").text
            timeStamp = datetime.fromtimestamp(int(time.time()))
            fileType = request.content_type

            ET.indent(child, space="    ")

            data = ET.tostring(child).decode()

            commitReportToDatabase(url, timeStamp, fileType, data)
            json_data = {"type": "DMARC Aggregate Report", "data": xmltodict.parse(data)}

    export_report(json_data)
    return json.dumps({'Message': "Request saved successfully"}), 200, {'ContentType':'application/json'}