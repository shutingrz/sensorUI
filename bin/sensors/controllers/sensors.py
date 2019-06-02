from flask import Blueprint, url_for, request, redirect, render_template, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from sensors.controllers import forms
from sensors.model.sensors import SensorsModel
from sensors.model.user import UserModel
from sensors.model.account import AccountModel
from sensors.model.flask_user import User as FlaskUser
from sensors.util import Util

sensors = Blueprint('sensors', __name__, url_prefix='/')

login_manager = LoginManager()

#user_idをidとして用いる
@login_manager.user_loader
def load_user(user_id):
	return FlaskUser(user_id)

@sensors.record_once
def on_load(state):
	login_manager.init_app(state.app)

@sensors.route('/')
def index():
	return render_template('sensors/index.html')

@sensors.route('/login', methods=("GET", "POST"))
def login():
	model = UserModel()
	form = forms.LoginForm(request.form)

	if request.method == 'POST':
		if form.validate():
			user, code = model.user_login(form.user_id.data, form.password.data)

			if user:
				login_user(user)
				return redirect(url_for(".index"))
			else:
				return render_template('sensors/login.html', description="ユーザIDまたはパスワードが違います。", form=form)
		else:
			return render_template('sensors/login.html', description="フォームを正しく入力してください。", form=form)
	return render_template('sensors/login.html', form=form)

@sensors.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for(".index"))

@sensors.route('/list')
def user_list():
	model = UserModel()

	page = request.args.get('page', None)
	user_list, code = model.user_list(page)

	return render_template('sensors/list.html', user_list=user_list)

@sensors.route('/user/<user_id>')
def user_profile(user_id):
	model = UserModel()

	return render_template('sensors/profile.html')
