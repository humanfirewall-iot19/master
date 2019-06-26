#!/usr/bin/env python3

from flask import Flask, request, jsonify
from slave.feedback_db_helper import FeedbackDBHelper
import json
import time
import bot
import os
import random
import string
import configparser

SRV_PORT = 41278
DB_NAME = "slave/feedback_db.sqlite"
UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./" + UPLOAD_FOLDER
parser = configparser.ConfigParser()
parser.read('config.ini')
tgtok = parser.get('telegram', 'token')
assert tgtok is not None
tgbot = bot.Bot(tgtok)

def rand_str(l):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(l))

def remove_old_imgs():
    now = time.time()
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.stat(os.path.join(app.config['UPLOAD_FOLDER'], f)).st_mtime < now - 60*60:
            os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], f))

@app.route('/ring', methods = ['POST'])
def ring():
    board_id = request.form.get("board_id")
    encoding = request.form.get("encoding")
    feedback = request.form.get("feedback")
    has_face=request.form.get("has_face")
    if 'file' not in request.files:
        return "no file in request"
    file = request.files['file']
    if file.filename == '':
        return jsonify(error = "no selected file name")
    if file:
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        filename = rand_str(16) + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_fd = open(UPLOAD_FOLDER + filename, "rb")
        print (board_id, encoding, feedback, BASE_URL + UPLOAD_FOLDER + filename)
        tgbot.send_notification(board_id, econding, feedback, img_fd, has_face=has_face)
        return "ok"
    return "invalid file"

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

if __name__ == "__main__":
    tgbot.start()
    app.run(host="0.0.0.0", port=SRV_PORT)
