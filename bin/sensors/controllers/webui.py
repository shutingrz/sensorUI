from flask import Blueprint, url_for, request, redirect, render_template, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from flask import Blueprint, jsonify, url_for, request, redirect, current_app
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from sensors.controllers import forms
from sensors.model.sensors import SensorsModel
from sensors.model.user import UserModel
from sensors.model.account import AccountModel
from sensors.model.device import DeviceModel
from sensors.model.sensor_temperature import SensorTemperatureModel
from sensors.model.flask_user import User as FlaskUser
from sensors.util import Util

webui = Blueprint('webui', __name__, url_prefix='/')

login_manager = LoginManager()

# flask-login用
@login_manager.user_loader
def load_user(user_hash):
    model = UserModel()
    username = model.getUsername(user_hash)

    if username is None:
        return FlaskUser(user_hash, "名無し")
    else:
        return FlaskUser(user_hash, username)


@webui.record_once
def on_load(state):
    login_manager.init_app(state.app)


@webui.route('/')
def index():
    return render_template('webui/index.html')


@webui.route('/login', methods=("GET", "POST"))
def login():
    model = UserModel()
    form = forms.LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user, code = model.user_login(
                form.username.data, form.password.data)

            if user:
                login_user(user)
                return redirect(url_for(".index"))
            else:
                return render_template('webui/login.html', description="ユーザIDまたはパスワードが違います。", form=form)
        else:
            return render_template('webui/login.html', description="フォームを正しく入力してください。", form=form)
    return render_template('webui/login.html', form=form)


@webui.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))
