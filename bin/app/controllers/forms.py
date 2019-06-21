from app.util import Util
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators


class LoginForm(FlaskForm):
    username = StringField(
        'username', [validators.length(min=3, max=Util.MaxUsernameLength)])
    password = PasswordField(
        'password', [validators.length(min=3, max=Util.MaxUserPassLength)])

class UserRegisterForm(FlaskForm):
    username = StringField(
        'username', [validators.length(min=3, max=Util.MaxUsernameLength)])
    password = PasswordField(
        "Set a Password", [
        validators.length(min=3, max=Util.MaxUserPassLength),
        validators.DataRequired(),
        validators.EqualTo("confirm", message="パスワードが一致しません")
    ])
    confirm = PasswordField("Repeat Password")

class DeviceRegisterForm(FlaskForm):
    device_name = StringField('device name', [validators.length(min=3, max=Util.MaxUsernameLength)])
    sensor_type = SelectField('SensorType', coerce=int, validators=[validators.Optional()], default='')
