from http import HTTPStatus

import bcrypt
from flask import abort, request, render_template
from werkzeug.datastructures import WWWAuthenticate
import flask
from login_form import LoginForm
from db import get_conn
from base64 import b64decode
from login_form import LoginForm
from app import app, conn
import flask_login
from flask_login import login_required, login_user, logout_user
from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    pass


# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    c = conn.execute('SELECT * FROM users WHERE id = ?', [user_id])
    rows = c.fetchall()
    c.close()
    if len(rows) == 0:
        return

    # For a real app, we would load the User from a database or something
    user = User()
    user.id = user_id
    return user


def get_user(user_id):
    c = conn.execute('SELECT * FROM users WHERE id = ?', [user_id])
    rows = c.fetchall()
    c.close()
    if len(rows) == 0:
        return

    # For a real app, we would load the User from a database or something
    user = user_id
    return user


def check_password(user_id, passwd):
    c = conn.execute('SELECT passwd FROM users WHERE id = ?', [user_id])
    rows = c.fetchall()
    c.close()
    print(len(rows))
    if bcrypt.checkpw(passwd.encode('utf8'), rows[0][0].encode('utf8')): #thanks to Chris Dutrow, copied from: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
        return user_id
    else:
        return False


# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the user name the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request):
    # Even though this HTTP header is primarily used for *authentication*
    # rather than *authorization*, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is not Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid, passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        print(f'Basic auth: {uid}:{passwd}')
        u = get_user(uid)
        if u and check_password(u, passwd):
            return user_loader(uid)
    # For other authentication schemes, see
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication

    # If we failed to find a valid Authorized header or valid credentials, fail
    # with "401 Unauthorized" and a list of valid authentication schemes
    # (The presence of the Authorized header probably means we're talking to
    # a program and not a user in a browser, so we should send a proper
    # error message rather than redirect to the login page.)
    # (If an authenticated user doesn't have authorization to view a page,
    # Flask will send a "403 Forbidden" response, so think of
    # "Unauthorized" as "Unauthenticated" and "Forbidden" as "Unauthorized")
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate=WWWAuthenticate('Basic realm=inf226, Bearer'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        # TODO: we must check the username and password
        username = form.username.data
        password = form.password.data
        u = get_user(username)
        if u and check_password(u, password):
            user = user_loader(username)

            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')

            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index_html'))
    return render_template('./login.html', form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))
