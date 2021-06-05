from flask import (
    render_template, 
    flash, 
    redirect, 
    url_for, 
    request,
    make_response,
    )
from app import app, db
from app.forms import (
    LoginForm, 
    RegistrationForm,
    NewBeerForm,
    NewPizzaForm,
    EditPizzaForm,
    EditBeerForm,
    )
from flask_login import (
    current_user, 
    login_user, 
    logout_user, 
    login_required,
    )
from app.models import User, Pizzas, Beers
from werkzeug.urls import url_parse

import json

from datetime import datetime
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
    
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    # PUT
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # if user-pwd pair not valid
            flash('Invalid username or password!')
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
    # with app.open_resource('static/json/beers.json') as f:
    #     beers = json.load(f)
    # with app.open_resource('static/json/pizzas.json') as f:
    #     pizzas = json.load(f)
    # pizzas = Pizzas.query.filter_by(available=True).all()
    # beers = Beers.query.filter_by(available=True).all()
    pizzas = Pizzas.query.all()
    beers = Beers.query.all()

    return render_template('menu.html',
        title="Menu Brewpub",
        verify=True,
        pizzas=pizzas,
        beers=beers,
        )

@app.route('/DondeEstamos')
def dondeEstamos():
    return render_template('donde_estamos.html', title="Mapa")

@app.route('/Beer')
def beers():
    return render_template('beers.html', title="Cervezas")

# redirected to beers
@app.route('/Register', methods=['GET', 'POST'])
def register():
    # # redirect GET
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = RegistrationForm()
    # # if PUT
    # if form.validate_on_submit():
    #     user = User(username=form.username.data, email=form.email.data)
    #     user.set_password(form.password.data)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Congratulations, you are now a registered user!')
    #     return redirect(url_for('login'))
    # # else GET
    # return render_template('register.html', title='Register', form=form)
    return redirect(url_for("beers"))

@app.route('/Admin')
@login_required
def admin():
    return render_template('admin_home.html', title="SZOT Admin")

# @app.errorhandler(404)
# def not_found():
#     return make_response(
#         render_template("404.html"), 
#         404
#     )

@app.route('/Admin/AgregarPizza',  methods=['GET', 'POST'])
@login_required
def new_pizza():
    form = NewPizzaForm()
    if form.validate_on_submit():
        # checkPizza = Pizzas.query.filter_by(product=form.product.data).first()
        # if checkPizza is None:
        newPizza = Pizzas(
            product = form.product.data,
            description = form.description.data,
            price = form.price.data,
            available = form.available.data,
        )
        db.session.add(newPizza)
        db.session.commit()
        return render_template('messages.html', message=f"Pizza {form.product.data} has been added")
    return render_template('agregar_productos.html', form=form, prod='PIZZA')

@app.route('/Admin/AgregarCerveza',  methods=['GET', 'POST'])
@login_required
def new_beer():
    form = NewBeerForm()
    if form.validate_on_submit():
        checkBeer = Beers.query.filter_by(product=form.product.data).first()
        if checkBeer is None:
            newBeer = Beers(
                product = form.product.data,
                description = form.description.data,
                alcohol = form.alcohol.data,
                mls = form.mls.data,
                price = form.price.data,
                available = form.available.data,
            )
            db.session.add(newBeer)
            db.session.commit()
            return render_template('messages.html', message=f"Beer {form.product.data} has been added")
    # elif request.method == 'GET':
        # form
    return render_template('agregar_productos.html', form=form, prod='BEER')

@app.route('/Admin/EditarMenu',  methods=['GET', 'POST'])
@login_required
def edit_menu():
    pizzas = Pizzas.query.all()
    beers = Beers.query.all()

    return render_template('menu_edit.html',
        title="Edit Menu Brewpub",
        verify=False,
        pizzas=pizzas,
        beers=beers,
        )

def check_if_change(old, new):
    value = new if (new != old) else old 
    return value

@app.route('/Admin/EditarMenu/pizza/<id>', methods=['GET', 'POST'])
@login_required
def edit_pizza(id):
    pizza = Pizzas.query.filter_by(id=id).first_or_404()
    # pizza_copy = pizza
    form = EditPizzaForm()
    # if get
    if form.validate_on_submit():

        pizza.product = form.product.data
        pizza.description = form.description.data
        pizza.price = form.price.data
        pizza.available = form.available.data

        db.session.commit()
        return redirect(url_for('edit_menu'))
        # return render_template(
        #     'messages.html', 
        #     message=f"Pizza name has been changed to {pizza.product}"
        #     )
    # if GET
    return render_template(
        "edit_product.html", 
        product=pizza,
        form=form
    )

@app.route('/Admin/EditarMenu/beer/<id>', methods=['GET', 'POST'])
@login_required
def edit_beer(id):
    beer = Beers.query.filter_by(id=id).first_or_404()
    # beer_copy = beer
    form = EditBeerForm()
    # if get
    if form.validate_on_submit():

        beer.product = form.product.data
        beer.description = form.description.data
        beer.price = form.price.data
        beer.available = form.available.data

        db.session.commit()
        return render_template(
            'messages.html', 
            message=f"Beer name has been changed to {beer.product}"
            )
    # if GET
    return render_template(
        "edit_product.html", 
        product=beer,
        form=form
    )
