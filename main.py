#!/usr/bin/env python3

from flask import Flask, request, jsonify
from slave.feedback_db_helper import FeedbackDBHelper
from werkzeug.utils import secure_filename
import json
import time
import bot
import os
import random
import string
import configparser
from slave import faces

SRV_PORT = 41278
DB_NAME = "slave/feedback_db.sqlite"
UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./" + UPLOAD_FOLDER
parser = configparser.ConfigParser()
parser.read('config.ini')
tgtok = parser.get('telegram', 'token')
assert tgtok is not None
tgbot = bot.Bot(tgtok, "127.0.0.1")

def rand_str(l):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(l))

def remove_old_imgs():
    now = time.time()
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.stat(os.path.join(app.config['UPLOAD_FOLDER'], f)).st_mtime < now - 60*60:
            os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], f))

@app.route('/ring', methods = ['POST'])
def ring():
    remove_old_imgs()
    j = json.loads(request.form.get("json"))
    print(j)
    board_id = j.get("board_id")
    encoding = j.get("encoding")
    feedback = j.get("feedback")
    has_face=j.get("has_face")
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
        print (board_id, encoding, feedback, UPLOAD_FOLDER + filename, has_face)
        tgbot.send_notification(board_id, encoding, feedback, img_fd, has_face)
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
def download_embeddings(timestamp):
    faces.restore("slave/encodings.pickle")
    diff = faces.query_by_time_b64(float(timestamp))
    print(faces.data)
    print("\n\n\n")
    print(diff)
    faces.destroy()
    return json.dumps(diff)

@app.route('/download_feedbacks/<timestamp>')
def download_feedbacks(timestamp):
    db = FeedbackDBHelper(DB_NAME)
    diff = db.get_diff(float(timestamp))
    print(diff)
    db.close()
    return json.dumps(diff)

if __name__ == "__main__":
    tgbot.start()
    app.run(host="0.0.0.0", port=SRV_PORT)
