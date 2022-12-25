from flask import (
     Flask,
     render_template,
     redirect,
     request,
     url_for,
     flash,
     get_flashed_messages,
     session)
from .functions import validate, find, get_user
from random import randint
import json


app = Flask(__name__)

app.secret_key = 'top_secret'
 

@app.route('/')
def root():
    message = get_flashed_messages(with_categories=True)
    return render_template('users/start_session.html', message=message)


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    error = validate(user)
    if error:
        return render_template('/users/new_user.html', error=error, user=user), 422
    flash('done', 'success')
    user['id'] = randint(1, 1000)
    session['users'] = session.get('users', [])
    session['users'].append(user)
    return redirect('/users', 302)


@app.route('/users')
def users_get():
    message = get_flashed_messages(with_categories=True)
    users = session.get('users', [])
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
    users = session['users']
    user = find(id, users)
    error = {}
    return render_template('users/edit_user.html', user=user, error=error)

@app.post('/users/<int:id>/patch')
def user_patch(id):
    users = session['users']
    patch = request.form.to_dict()
    error = validate(patch)
    if error:
        return render_template('users/edit_user.html', user=patch, id=patch.id, error=error)
    flash('user has been updated', 'success')
    updating_user = find(id, users)
    updating_user['name'] = patch['name']
    return redirect('/users', 302)


@app.post('/users/session')
def user_session():
    users = [{'name': 'vadim', 'email': 'vava@saas'}, {'name': 'lox', 'email': 'qaq@qa'}]
    email = request.form['email']
    user = get_user(email, users)
    if not user:
        flash('no such user', 'failed')
        return redirect('/', 422)
    session['user'] = user
    flash('success log in', 'success')
    return redirect('/users', 302)


@app.post('/users/session/clear')
def clear_session():
    session.clear()
    return redirect('/')
