import os

from flask import Flask, render_template, g, redirect, url_for
from app.auth import auth_bp
from app.auth.routes import login_required
from app.db import get_db


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
    def home():
        return redirect(url_for("auth.login"))
    
    @app.route('/room', methods=["GET"])
    @login_required
    def room():
        other_users = get_db().execute(
            'SELECT id, email FROM users WHERE email != ?',[g.user['email']]
        ).fetchall()
        
        data = {"users": []}
        
        for u in other_users:
            data["users"].append({
                "id": u["id"],
                "email": u["email"],
            })
                            
        return render_template("room/index.html", data=data)
    
    return app