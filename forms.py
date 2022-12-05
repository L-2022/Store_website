from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Incorrect email")])
    psw = PasswordField("Password: ", validators=[DataRequired(),
                                                Length(min=4, max=128,
                                                       message="Password must be between 4 - 100 characters")])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField("First name: ",
                             validators=[Length(min=4, max=100, message="First name must be between 4 - 100 characters")])

    last_name = StringField("Last name: ",
                            validators=[Length(min=4, max=100, message="last name must be between 4 - 100 characters")])
    old = IntegerField('Old', validators=[InputRequired(message="characters")])
    phone = IntegerField('Phone', validators=[InputRequired(message="characters")])

    email = StringField("Email: ", validators=[Email("Incorrect email")])
    psw = PasswordField("Password: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message="Password must be between 4 - 100 characters")])

    psw2 = PasswordField("Password repeat: ", validators=[DataRequired(), EqualTo('psw', message="Passwords does not match!")])

    submit = SubmitField("Registration")


class AddProduct(FlaskForm):
    product_name = StringField("Name product: ",
                               validators=[Length(min=4, max=100,
                                                  message="Name product must be between 4 - 100 characters")])

    characteristic = StringField("characteristic product: ",
                                 validators=[Length(min=4, max=1400,
                                                    message="characteristic product 1 - 1400")])
    categories = StringField("Categories product: ",
                             validators=[Length(min=4, max=100,
                                                message="Categories must be between 4 - 100 characters")])
    cost = IntegerField('Price', validators=[InputRequired(message="characters")])

    submit = SubmitField("Add")


class Dell_user(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=10, max=100)])

    submit = SubmitField("Add")
