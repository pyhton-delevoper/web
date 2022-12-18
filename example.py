from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages
from .validator import validate
import json


app = Flask(__name__)

app.secret_key = 'krepysh'


@app.route('/')
def root():
    return ('<a href="/users"><h1>USERS</h1></a>')


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    error = validate(user)
    if error:
        return render_template('/users/new_user.html', error=error, user=user), 422
    with open('user.txt', 'a') as file:
        user_data = json.dumps(user)
        file.write(user_data)
    return redirect('/users')


@app.route('/users')
def users_get():
    message = get_flashed_messages(with_categories=True)
    users = open('user.txt').read()[1:-1].split('}{')
    page = request.args.get('page', 1, int)
    view_limit = 3
    offset = (page - 1) * view_limit
    content = users[offset:(page * view_limit)]
    return render_template('users/users.html', message=message, users=content, page=page)


@app.route('/users/new')
def users_new():
    user = request.form.to_dict()
    flash('done', 'success')
    return render_template('users/new_user.html', user=user)
