from flask import Flask, render_template, redirect, request
import json


app = Flask(__name__)


@app.route('/')
def root():
    return ('<a href="/users"><h1>USERS</h1></a>')


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    json.dump(user, open('user.txt', 'w'))
    return redirect('/users', 302)


@app.get('/users')
def users_get():
    return f'<a href="/users/new">new user</a> <div>{open("user.txt").read()}</div>'


@app.route('/users/new')
def users_new():
    user = json.load(open('user.html'))
    return render_template('users/index.html', user=user)
