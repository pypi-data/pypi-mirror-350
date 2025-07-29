import os

from datetime import timedelta

from flask import Flask, render_template

secret_key = os.environ.get('SECRET_KEY', 'ThisIsNotSecret')

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=secret_key,
    PERMANENT_SESSION_LIFETIME=timedelta(days=365),
)

from . import lesson1
app.register_blueprint(lesson1.bp, url_prefix='/lesson1')
from . import lesson2
app.register_blueprint(lesson2.bp, url_prefix='/lesson2')
from . import lesson3
app.register_blueprint(lesson3.bp, url_prefix='/lesson3')
from . import lesson4
app.register_blueprint(lesson4.bp, url_prefix='/lesson4')
from . import lesson10
app.register_blueprint(lesson10.bp, url_prefix='/lesson10')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


def run():
    host_name = os.environ.get('HOST', '127.0.0.1')
    port_num = int(os.environ.get('PORT', '5000'))
    debug_flag = bool(os.environ.get('DEBUG', False))
    app.run(host=host_name, port=port_num, debug=debug_flag)
