from cheers.util import Util
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class LoginForm(FlaskForm):
	user_id = StringField('user_id', [validators.length(min=1, max=Util.MaxUserIdLength)])
	password = StringField('password', [validators.length(min=1, max=Util.MaxUserPassLength)])

