from sensors.util import Util
from flask_wtf import FlaskForm
from wtforms import StringField, validators


class LoginForm(FlaskForm):
    username = StringField(
        'username', [validators.length(min=1, max=Util.MaxUsernameLength)])
    password = StringField(
        'password', [validators.length(min=1, max=Util.MaxUserPassLength)])
