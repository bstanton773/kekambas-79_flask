from app import app

@app.route('/')
def index():
    return 'Hello World!!!'


@app.route('/name')
def name():
    my_name = 'Brian'

    return f"Hello {my_name}"


@app.route('/test')
def test():
    return '<h1>This is a test</h1>'