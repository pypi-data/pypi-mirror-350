from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")
    
class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Электронная почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Подтверждение пароля", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Войти")