from app import app
from flask import render_template

@app.route('/')
def index():
    my_name = 'Brian'
    my_city = 'Chicago'
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black', 'magenta', 'pink']
    person = {
        'name': 'Ferris Bueller',
        'age': 18,
        'best_friend': 'Cameron'
    }
    return render_template('index.html', name=my_name, city=my_city, colors=colors, person=person)


@app.route('/name')
def name():
    my_name = 'Brian'

    return render_template('name.html', name=my_name)


@app.route('/test')
def test():
    return '<h1>This is a test</h1><h4>This is an h4</h4>'