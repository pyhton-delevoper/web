from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages
from .functions import validate, find
from random import randint
import json


app = Flask(__name__)

app.secret_key = 'top_secret'
 

@app.route('/')
def root():
    return ('<a href="/users"><h1>USERS</h1></a>')


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    error = validate(user)
    if error:
        return render_template('/users/new_user.html', error=error, user=user), 422
    flash('done', 'success')
    user['id'] = randint(1, 1000)
    cookie = json.loads(request.cookies.get('users', json.dumps([])))
    cookie.append(user)
    response = redirect('/users')
    response.set_cookie('users', json.dumps(cookie))
    return response, 302


@app.route('/users')
def users_get():
    message = get_flashed_messages(with_categories=True)
    users = json.loads(request.cookies.get('users'))
    page = request.args.get('page', 1, int)
    view_limit = 3
    offset = (page - 1) * view_limit
    content = users[offset:(page * view_limit)]
    return render_template('users/users.html', message=message, users=content, page=page)


@app.route('/users/new')
def user_new():
    user = request.form.to_dict()
    return render_template('users/new_user.html', user=user)


@app.route('/users/<int:id>/edit')
def user_edit(id):
    users = json.loads(request.cookies.get('users'))
    user = find(id, users)
    error = {}
    return render_template('users/edit_user.html', user=user, error=error), 422

@app.post('/users/<int:id>/patch')
def user_patch(id):
    users = json.loads(request.cookies.get('users'))
    patch = request.form.to_dict()
    error = validate(patch)
    if error:
        return render_template('users/edit_user.html', user=patch, id=patch.id, error=error)
    flash('user has been updated', 'success')
    updating_user = find(id, users)
    updating_user['name'] = patch['name']
    response = redirect('/users')
    response.set_cookie('users', json.dumps(users))
    return response, 302
