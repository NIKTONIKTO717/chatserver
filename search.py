from flask import request
from json import dumps
from apsw import Error
from flask_login import current_user, login_required

from app import app, conn

@app.get('/messages')
@login_required
def get_messages():
    sent = request.args.get('sent', default=False, type=bool) or request.form.get('sent', default=False, type=bool)
    query = request.args.get('q') or request.form.get('q') or ''
    query_sql = '%'+query+'%'
    try:
        if sent:
            c = conn.execute('SELECT id, sender, message, timestamp, GROUP_CONCAT(recipient) FROM messages WHERE (recipient = ? OR recipient is NULL OR sender = ?) AND message like ? GROUP BY sender, message, timestamp ORDER BY id', (current_user.get_id(), current_user.get_id(), query_sql))
        else:
            c = conn.execute('SELECT * FROM messages WHERE recipient = ? OR recipient is NULL AND message like ?', (current_user.get_id(), query_sql))
        rows = c.fetchall()
        c.close()
        return rows
    except Error as e:
        return f'ERROR: Something went wrong', 500

@app.get('/messages/<message_id>')
@login_required
def get_message(message_id):
    try:
        c = conn.execute("SELECT * FROM messages WHERE (recipient = '" + current_user.get_id() + "' OR sender = '" + current_user.get_id() + "') AND id = '" + current_user.get_id() + "'")
        rows = c.fetchall()
        result = ''
        for row in rows:
            result += f'    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return f'ERROR: Something went wrong', 500