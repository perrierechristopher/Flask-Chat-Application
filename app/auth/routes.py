from flask import Blueprint, render_template, request, redirect, url_for, g, flash, session
from app.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import sqlite3
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = ''
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if not error:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('room'))

        flash(error, 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    
@auth_bp.route('/sign-up', methods=["GET", "POST"])
def signup():    
    if request.method == "POST":
        max_retries = 5
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = ''
        
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if not error:
            for _ in range(max_retries):
                try:
                    user_id = str(uuid.uuid4())
                    db.execute(
                        "INSERT INTO users (id, email, password) VALUES (?, ?, ?)",
                        (user_id, email, generate_password_hash(password)),
                    )
                    db.commit()
                                    
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed: users.id" in str(e):
                        # UUID collision – retry with a new one
                        continue
                    elif "UNIQUE constraint failed: users.email" in str(e):
                        error = "Email already exists"
                    else:
                        print(e)
                        error = "Internal Server Error, Contact Admin"
                else:
                    return redirect(url_for("auth.login"))

        flash(error, 'error')
    return render_template('auth/signup.html')
