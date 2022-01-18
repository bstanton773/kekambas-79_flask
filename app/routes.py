from app import app
from flask import render_template
from app.forms import RegisterForm

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


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
    return render_template('register.html', form=form)