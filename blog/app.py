import logging

from flask import Flask, request, g
from time import time
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


@app.route('/greet/<name>')
def index(name:str):
    return f'Hello, {name}'



@app.route('/user/')
def read_user():
    name = request.args.get('name')
    surname = request.args.get('surname')
    return f'User {name or "[no name]"} {surname or "[no surname]"}'

@app.route('/status/', methods = ['GET', 'POST'])
def custom_status_code():
    if request.method == 'GET':
        return '''
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData  
        '''
    print(f'raw butes data', request.data)

    if request.form and 'code' in request.form:
        return 'code from form', request.form['code']
    data = request.get_json(silent=True) # исключает падение ошибки 415, если json нет или он неправильный
    if data and 'code' in data:
        return 'code from json', int(data['code'])
    else:
        return f'JSON отсутствует или некорректный'


@app.before_request
def process_before_request():
    """
    Sets start_time to 'g' object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, 'start_time'):
        response.headers['process-time'] = time() - g.start_time
    return response

app.logger.setLevel(logging.DEBUG)

@app.route('/power/')
def power_value():
    x = request.args.get('x') or ''
    y = request.args.get('y') or ''
    if not (x.isdigit() and y.isdigit()):
        app.logger.info(f'invalid values for power: x={x}, y={y}')
        raise BadRequest(f'please, input correct values')
    x, y = int(x), int(y)
    result = x ** y
    app.logger.debug(f'x ** y == {result}')
    return str(result)


@app.route('/divide-by-zero')
def do_zero_division():
    return 1/0


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error)
    app.logger.exception('trace zero')
    return f'never divide by zero', 400
