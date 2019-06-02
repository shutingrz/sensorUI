from flask import Blueprint, jsonify, url_for, request, redirect
from flask_login import LoginManager, login_user, login_required, current_user
from cheers.model.cheers import CheersModel
from cheers.model.user import UserModel
from cheers.model.account import AccountModel
from cheers.model.flask_user import User as FlaskUser
from cheers.util import Util

api = Blueprint('cheers_api', __name__, url_prefix='/api/')

login_manager = LoginManager()

#@api.record_once
#def on_load(state):
#	login_manager.init_app(state.app)

@api.route('/')
def api_index():
	return jsonify(list = url_for('.api_user_list'))

@api.route('/list')
def api_user_list():
	model = UserModel()

	page = request.args.get('page', None)

	msg, code = model.user_list(page)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

@api.route('/user/detail/<id>')
def api_user_detail():
	pass

@api.route('/login')
def api_login():
	user_id = request.args.get('user_id', None)
	password = request.args.get('password', None)

	if user_id is None or password is None:
		return jsonify(_makeErrorMessage(11))

	if len(user_id) > Util.MaxUserIdLength or len(password) > Util.MaxUserPassLength:
		return jsonify(_makeErrorMessage(12))

	model = UserModel()
	user, code = model.user_login(user_id, password)

	if user is None:
		return jsonify(_makeErrorMessage(code))
	else:
		if user:
			login_user(user)
			return redirect(request.args.get("next") or url_for(".api_index"))
		else:
			return jsonify(_makeErrorMessage(21))

#todo. デザインとかできたらPOSTのフォームを受け付けるようにする
#todo. デザインとかできたらAPIから通常画面にする？
@api.route('/register')
def api_user_register():
	user_id = request.args.get('user_id', None)
	password = request.args.get('password', None)

	if user_id is None or password is None:
		return jsonify(_makeErrorMessage(11))

	if len(user_id) > Util.MaxUserIdLength or len(password) > Util.MaxUserPassLength:
		return jsonify(_makeErrorMessage(12))


	model = UserModel()

	if model.user_isExist(user_id)[0]: # get first element, because user_isExist returns "True/False, code".
		return jsonify(_makeErrorMessage(13))

	msg, code = model.user_register(user_id, password)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	

	return jsonify(_makeResponseMessage(msg))


#ユーザ削除, デバッグ用のためユーザ認証は不要.
#todo. 本番運用時は削除!!
@api.route('/admin/user/delete/<user_id>')
def api_admin_user_delete(user_id):
	if Util.DebugMode is False:
		return jsonify(_makeErrorMessage(0))

	model = UserModel()

	if model.user_isExist(user_id)[0]:
		msg, code = model.user_delete(user_id)

		if msg is None:
			return jsonify(_makeErrorMessage(code))
		else:
			return jsonify(_makeResponseMessage(msg))
	else:
		return jsonify(_makeErrorMessage(13))
	

'''
api_userid_isExist
ユーザの存在確認(重複登録防止)

todo: ブルートフォース攻撃対策
'''
@api.route('/user/<user_id>/isexist')
def api_userid_isExist(user_id):
	model = UserModel()
	msg, code = model.user_isExist(user_id)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

@api.route('/account/status')
@login_required
def api_account_status():
	model = AccountModel()
	msg, code = model.account_status(current_user.user_id)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

'''
本人からみたプロフィール
'''
@api.route('/account/profile')
@login_required
def api_account_profile():
	model = UserModel()
	msg, code = model.user_profile(current_user.user_id)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

'''
プロフィール保存
todo. POSTで送信
'''
@api.route('/account/profile/save')
@login_required
def api_account_save_profile():
	model = AccountModel()
	nickname = request.args.get('nickname', None)
	email = request.args.get('email', None)
	department = request.args.get('department', None)
	introduction = request.args.get('introduction', None)

	msg, code = model.account_save_profile(current_user.user_id, nickname=nickname, email=email, department=department, introduction=introduction)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

'''
みんなからみたプロフィール
'''
@api.route('/user/<user_id>')
def api_user_profile(user_id):
	model = UserModel()
	msg, code = model.user_profile(user_id)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

#todo. POSTで送るようにする
@api.route('/gift')
@login_required
def api_gift():
	model = CheersModel()
	sender =  current_user.user_id
	receiver = request.args.get('destination', None)
	value = 1
	message = request.args.get('message', None)
	is_anonymous = request.args.get('is_anonymous', False)

	if receiver is None:
		return jsonify(_makeErrorMessage(0))
	elif sender == receiver:
		return jsonify(_makeErrorMEssage(1))

	if is_anonymous is not True:
		is_anonymous = False

	msg, code = model.gift(sender, receiver, value, message, is_anonymous)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

@api.route('/gifts')
@login_required
def api_gifts():
	model = CheersModel()
	user_id = current_user.user_id

	msg, code = model.gifts(user_id)

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

@api.route('/gifts/send')
@login_required
def api_gifts_send():
	model = CheersModel()
	user_id = current_user.user_id

	msg, code = model.gifts(user_id, "send")

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

@api.route('/gifts/receive')
@login_required
def api_gifts_receive():
	model = CheersModel()
	user_id = current_user.user_id

	msg, code = model.gifts(user_id, "receive")

	if msg is None:
		return jsonify(_makeErrorMessage(code))
	else:
		return jsonify(_makeResponseMessage(msg))

def _makeErrorMessage(code):
	data = {'header': {'status': 'error', 'errorCode': code}, 'response': {}}
	return data

def _makeResponseMessage(response):
	data = {'header': {'status': 'success', 'errorCode': 0}, 'response': response}
	return data
