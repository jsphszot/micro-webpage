# login form
from babel import Locale
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, 
    PasswordField, 
    StringField, 
    TextAreaField,
    DecimalField,
    IntegerField,
    BooleanField,
    SubmitField,
    )
from wtforms.validators import (
    DataRequired,
    InputRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Optional,
    )
from app.models import User, Pizzas, Beers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# functionality to self register through a web form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # must be unique
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewPizzaForm(FlaskForm):
    product = StringField('Nombre de Pizza', validators=[InputRequired(), Length(min=1, max=Pizzas.len_product)])
    description = TextAreaField('Descripción de la Pizza', validators=[DataRequired(), Length(min=1, max=Pizzas.len_description)])
    price = IntegerField('Precio CLP sin separador de miles', validators=[DataRequired(), NumberRange(min=0, message="Debe ser mayor a 0")])
    available = BooleanField('marcar como Disponible', default=True)
    submit = SubmitField('Crear Pizza')

    # validate_[fieldname]
    # https://wtforms.readthedocs.io/en/3.0.x/forms/#inline-validators
    def validate_product(self, product):
        # must be unique
        checkPizza = Pizzas.query.filter_by(product=product.data).first()
        if checkPizza is not None:
            raise ValidationError('Este nombre de Pizza ya existe - Usa otro.')

class NewBeerForm(FlaskForm):
    product = StringField('Nombre de Cerveza', validators=[DataRequired(), Length(min=1, max=Beers.len_product)])
    description = TextAreaField('Descripción de la Cerveza', validators=[DataRequired(), Length(min=1, max=Beers.len_description)])
    alcohol = DecimalField('grados de alcohol (usa "." para decimal)', validators=[DataRequired(), NumberRange(min=0, message="Debe ser mayor a 0")], places=1)
    mls = IntegerField('mls (sin separador de miles)', validators=[DataRequired(), NumberRange(min=0, message="Debe ser mayor a 0")])
    price = IntegerField('Precio CLP (sin separador de miles)', validators=[DataRequired(), NumberRange(min=0, message="Debe ser mayor a 0")])
    available = BooleanField('marcar como Disponible', default=True)
    submit = SubmitField('Crear Cerveza')

    def validate_product(self, product):
        # must be unique
        beer = Beers.query.filter_by(product=product.data).first()
        if beer is not None:
            raise ValidationError('Este nombre de Cerveza ya existe - Usa otro.')

class EditBeerForm(FlaskForm):
    product = StringField('Nuevo Nombre', validators=[Length(min=1, max=Beers.len_product)])
    description = TextAreaField('Descripción', validators=[Length(min=1, max=Beers.len_description)])
    alcohol = DecimalField('grados de alcohol (usa "." para decimal)', validators=[NumberRange(min=0, message="Debe ser mayor a 0")], places=1)
    mls = IntegerField('mls (sin separador de miles)', validators=[NumberRange(min=0, message="Debe ser mayor a 0")])
    price = IntegerField('Precio CLP (sin separador de miles)', validators=[NumberRange(min=0, message="Debe ser mayor a 0")])
    available = BooleanField('marcar como Disponible', validators=[])
    submit = SubmitField('Editar')

class EditPizzaForm(FlaskForm):
    product = StringField('Nuevo Nombre', validators=[Length(min=1, max=Pizzas.len_product)])
    description = TextAreaField('Descripción', validators=[Length(min=1, max=Pizzas.len_description)])
    price = IntegerField('Precio CLP (sin separador de miles)', validators=[NumberRange(min=0, message="Debe ser mayor a 0")])
    available = BooleanField('marcar como Disponible', validators=[])
    submit = SubmitField('Editar')
