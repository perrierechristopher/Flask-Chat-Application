import os

from flask import Flask, render_template
from app.auth import auth_bp


def create_app(custom_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'instance', 'app.sqlite'),
    )
    
    from . import db
    db.init_app(app)
        
    if custom_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(custom_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Auth Blueprint
    app.register_blueprint(auth_bp)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, this is the home page'
    
    @app.route('/room', methods=["GET"])
    def room():
        return render_template("room/index.html")
    
    return app