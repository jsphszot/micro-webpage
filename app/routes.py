from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
def index():
    posts = [
                {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
    ]
    render_vals = {
        'title':'Home',
        'posts': posts,
    }
    
    return render_template('index.html', rv=render_vals)
    
@app.route('/Admin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    # PUT
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin')
        return redirect(next_page)
    # GET
    render_vals={'title':'Sign In', 'form':form}
    return render_template('login.html', title="Login", rv=render_vals)

@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/Menu')
def menu():
    return render_template('menu.html', title="Menu Brewpub")

@app.route('/Admin/Home')
@login_required
def admin():
    return render_template('admin_home.html', title="SZOT Admin")

@app.route('/DondeEstamos')
def dondeEstamos():
    return render_template('donde_estamos.html', title="Mapa")

@app.route('/Beer')
def beers():
    return render_template('beers.html', title="Cervezas")
