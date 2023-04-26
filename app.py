from flask import Flask, abort, request, send_from_directory, make_response, render_template
from db import get_conn
from pygments.formatters import HtmlFormatter
from flask_login import login_required, login_user, logout_user, current_user
import sys
print(sys.executable)

conn = get_conn()

# Set up app
app = Flask(__name__)

from login import login, logout
from send import send
from search import get_messages
from announcements import announcements

# The secret key enables storing encrypted session data in a cookie (make a secure random key for this!)
app.secret_key = 'mY6ds6SS78waeDymArnEyWyHagOtdashDogJaf['


@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(app.root_path, 'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(app.root_path, 'static/favicon.png', mimetype='image/png')


@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return render_template('./index.html', user_id=current_user.get_id())



@app.get('/coffee/')
def nocoffee():
    abort(418)


@app.route('/coffee/', methods=['POST', 'PUT'])
def gotcoffee():
    return "Thanks!"
