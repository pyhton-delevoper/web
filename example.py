from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


@app.route('/')
def json():
    return '<h1>SuS</h1>'


@app.route('/users')
def get_names():
    chars = request.args.get('chars')
    names = [name for name in users if str(chars) in name]
    return render_template('users/index.html', names=names, chars=chars)


