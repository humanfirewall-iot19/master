#!/usr/bin/env python3

from flask import Flask
from slave.feedback_db_helper import FeedbackDBHelper
import json

SRV_PORT = 41278
DB_NAME = "slave/feedback_db.sqlite"

app = Flask(__name__)

@app.route('/i_am_the_master')
def i_am_the_master():
    return "OK"

@app.route('/last_timestamp')
def last_timestamp():
    db = FeedbackDBHelper(DB_NAME)
    t = db.get_max_time()
    db.close()
    return str(t)

@app.route('/download_embeddings/<timestamp>')
def last_timestamp(timestamp):
    return ""

@app.route('/download_feedbacks/<timestamp>')
def last_timestamp(timestamp):
    return ""



