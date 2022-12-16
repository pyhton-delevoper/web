from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages
import json


app = Flask(__name__)

app.secret_key = 'krepysh'


@app.route('/')
def root():
    return ('<a href="/users"><h1>USERS</h1></a>')


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    with open('user.txt', 'a') as file:
        user_data = json.dumps(user)
        file.write(user_data)
    return redirect(url_for("users_get"))


@app.route('/users')
def users_get():
    message = get_flashed_messages(with_categories=True)
    users = open('user.txt').read()[1:-1].split('}{')
    return render_template('users/user.html', message=message, users=users)


@app.route('/users/new')
def users_new():
    user = request.args.to_dict()
    flash('done', 'success')
    return render_template('users/index.html', user=user)
