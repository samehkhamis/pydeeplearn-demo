from flask import Flask, request, session, g, url_for, render_template, flash, jsonify
import gevent
from gevent.pywsgi import WSGIServer
from rq import Queue
from rq.job import Job
import worker

application = Flask(__name__)
application.secret_key = 'f\x96k\x07\xcel\x15\xbcm\xb6\xa77I/`\xc3\xfc\x18_E:\xdf\x02\xe0' # cookie signing
q = Queue(connection=worker.connection)

def get_job(job_id):
    try:
        job = Job.fetch(job_id, connection=worker.connection)
    except Exception:
        job = None
    return job

@application.route('/')
def index():
    session['result'] = '...'
    return render_template('index.html')

@application.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        imb64 = request.form['image']
        job = q.enqueue_call(func=worker.recognize, args=(imb64,), timeout=60, result_ttl=120)
        session['result'] = '...'
        session['job_id'] = job.get_id()
        return ''

@application.route('/result')
def result():
    # long polling on the server-side
    for i in xrange(20): # 10 seconds
        if 'job_id' in session:
            job = get_job(session['job_id'])
            if job is not None and job.is_finished:
                session.pop('job_id', None)
                session['result'] = job.meta['result']
                return jsonify(result=session['result'])
        
        # otherwise wait and retry until timeout, client will reconnect
        gevent.sleep(0.25)
    
    return jsonify(result=session['result'])

@application.errorhandler(404)
def page_not_found(error):
    return "(404) Hey! What are you trying to do?! ", 404

if __name__ == "__main__":
    server = WSGIServer(('', 80), application)
    server.serve_forever()
