from flask import Blueprint, url_for, request, redirect, render_template, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask import Blueprint, jsonify, url_for, request, redirect, current_app
from app.controllers import forms
from app.model import FlaskUser, SensorModel, UserModel, DeviceModel, SensorTemperatureModel
from app.util import Util, ResultCode

webui = Blueprint('webui', __name__)

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

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/login?next=" + request.path)


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

    if request.method == "GET":
        return render_template('webui/login.html', form=form)

    if request.method == "POST":
        if not form.validate():
            return render_template('webui/login.html',
            login_description="フォームを正しく入力してください。",
            form=form)
        
        user, code = model.user_login(form.username.data, form.password.data)

        if code == ResultCode.Success and user:
            login_user(user)
            return redirect(request.args.get('next') or url_for("webui.device_list"))
        else:
            return render_template('webui/login.html',
            login_description="ユーザIDまたはパスワードが違います。",
            form=form)
            

    return render_template('webui/login.html', form=form)


@webui.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))


@webui.route('/register', methods=("GET", "POST"))
def user_register():
    form = forms.UserRegisterForm(request.form)

    if request.method == "GET":
        return render_template('webui/user_register.html', form=form)

    if request.method == "POST":
        if not form.validate():
            return render_template('webui/user_register.html',
                register_description="フォームを正しく入力してください。",
                form=form)

        
        username = form.username.data
        password = form.password.data

        model = UserModel()
        if model.user_isExist(username)[0]:
            return render_template('webui/user_register.html',
                    register_description="既に同じ名前のユーザが存在します。",
                    form=form)

        msg, code = model.user_register(username, password)

        if code == ResultCode.Success :
            return render_template('webui/success_user_register.html')
        else:
            return render_template('webui/user_register.html',
                register_description="ユーザ登録に失敗しました: %s" % msg,
                form=form)
            


@webui.route('/devices')
@login_required
def device_list():
    deviceModel = DeviceModel()
    sensorModel = SensorModel()

    sensorTypes, code = sensorModel.getSensorType()
    if code != ResultCode.Success:
        return render_template('webui/device_register.html',
            description="センサータイプの取得に失敗しました: %s" % sensorTypes,
            form=form)

    devices, code = deviceModel.device_list(current_user.user_hash)

    if code != ResultCode.Success:
        return render_template('webui/device_list.html', description="デバイスの取得に失敗しました")

    if len(devices) == 0:
        return render_template('webui/device_list.html', description="デバイスが登録されていません")
    
    # sensor_typeに対応する名前を取得
    for device in devices:
        for type_data in sensorTypes:
            if device["sensor_type"] == type_data["id"]:
                device["sensor_type_name"] = type_data["name"]

    return render_template('webui/device_list.html', devices=devices)


@webui.route('/register-device', methods=("GET", "POST"))
@login_required
def device_register():
    sensorModel = SensorModel()
    form = forms.DeviceRegisterForm(request.form)

    sensorTypes, code = sensorModel.getSensorType()
    if code != ResultCode.Success:
        return render_template('webui/device_register.html',
            description="センサータイプの取得に失敗しました: %s" % sensorTypes,
            form=form)

    sensorType = [(i["id"], i["name"]) for i in sensorTypes]
    form.sensor_type.choices = sensorType

    if request.method == 'GET':
        return render_template('webui/device_register.html', form=form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('webui/device_register.html',
                description="フォームがあかん",
                form=form)


        device_name = form.device_name.data
        sensor_type = form.sensor_type.data

        model = DeviceModel()

        msg, code = model.device_register(current_user.user_hash, device_name, sensor_type)

        if code == ResultCode.Success:
            return redirect(url_for("webui.device_list"))
        else:
            return render_template('webui/device_register.html',
                description="デバイス登録に失敗しました: %s" % msg,
                form=form)            
        

@webui.route('/device/<device_id>')
@login_required
def device_view(device_id):
    deviceModel = DeviceModel()

    deviceData, code = deviceModel.device_get(current_user.user_hash, device_id)

    if code != ResultCode.Success:
        return redirect(url_for("webui.device_list"))
    
    endpoint = None

    if deviceData["sensor_type"] == Util.SensorType.Temperature:
        endpoint = 'webui/device_temperature_view.html'
        deviceData["sensor_type_name"] = "Temperature"

        sensorTemperatureModel = SensorTemperatureModel()
        sensorData, code = sensorTemperatureModel.getDataOfLastTenMinutes(current_user.user_hash, device_id)  

    
    if endpoint:
        return render_template(endpoint, sensorData=sensorData, device=deviceData) 
    else:
        return redirect(url_for("webui.device_list"))

