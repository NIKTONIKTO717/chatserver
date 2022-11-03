from flask import request
from apsw import Error
from flask_login import current_user, login_required
import re
import html
from app import app, conn

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')


@app.route('/new', methods=['POST'])
@login_required
def send():
    try:
        recipients = request.args.get('recipients') or request.form.get('recipients')
        message = request.args.get('message') or request.args.get('message')
        ### thanks rescdsk for solution: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
        message = tag_re.sub('', message)
        message = html.escape(message)
        ###
        sender = current_user.get_id()
        if not message:
            return f'ERROR: missing message'
        if recipients == '' or recipients is None:
            conn.execute('INSERT INTO messages (sender, message, recipient) values (?, ?, null);',
                         (sender, message))
        else:
            recipients = tag_re.sub('', recipients)
            recipients = html.escape(recipients)
            recipients_list = recipients.strip().split(",")
            for recipient in recipients_list:
                conn.execute('INSERT INTO messages (sender, message, recipient) values (?, ?, ?);',
                             (sender, message, recipient))
        c = conn.execute('SELECT * FROM messages WHERE sender = ? ORDER BY id DESC LIMIT 1',
                         (current_user.get_id(),))
        rows = c.fetchall()
        c.close()
        return rows
    except Error as e:
        return f'ERROR: Message was not send.'
