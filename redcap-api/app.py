import time
import pycurl
from io import BytesIO
import urllib

from flask import Flask

app = Flask(__name__)

TOKEN = '1B8263FE00A21A63CC66D4A4533C47E2'


def getInfo(): 
    data = {
        'content': 'project',
    }
    return sendRequest(data)
    
def getEvents():
    data = {
        'content': 'event',
    }
    return sendRequest(data)
    
def getFields():
    data = {
        'content': 'exportFieldNames',
    }
    return sendRequest(data)
    
def getRecords(): 
    data = {
        'content': 'record',
        'records[0]': '1',
        'records[1]': '1-1',
        'records[2]': '1-2',
        'records[3]': '1-3',
        'records[4]': '1-4',
        'records[5]': '1-5',
        'records[6]': '2',
        'records[7]': '2-10001',
        'records[8]': '2-10002',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
    }
    return sendRequest(data)
    
def getMetadata():
    data = {
        'content': 'metadata',
    }
    return sendRequest(data)

    
def sendRequest(data):
    data = prepData(data)
    buf = BytesIO()
    ch = pycurl.Curl()
    ch.setopt(ch.URL, 'https://redcap.kpmp.org/api/')
    ch.setopt(ch.POSTFIELDS, urllib.parse.urlencode(data))
    ch.setopt(ch.WRITEDATA, buf)
    ch.perform()
    ch.close()
    results = buf.getvalue()
    buf.close()
    return results

def prepData(data):
    data['token'] = TOKEN
    data['format'] = 'json'
    data['returnFormat'] = 'json'
    return data;
    
@app.route('/')
def getHomepage():
    return '''
        <h2>REDCap API Demo</h2>
        <section>
            <article>
                <h3>Example Queries</h3>
                <ul>
                    <li><a href="info">project info</a></li>
                    <li><a href="records">some records</a></li>
                    <li><a href="fields">fields</a></li>
                    <li><a href="events">events</a></li>
                    <li><a href="metadata">metadata</a></li>
                </ul>
            </article>
        </section>

    '''
    
@app.route('/info')
def getInfoRoute():
    return getInfo()
    
@app.route('/records')
def getRecordsRoute():
    return getRecords()
    
@app.route('/fields')
def getFieldsRoute():
    return getFields()
    
@app.route('/events')
def getEventsRoute():
    return getEvents()
    
@app.route('/metadata')
def getMetadataRoute():
    return getMetadata()
    
    