import sqlalchemy
from sqlalchemy import or_
from flask import current_app
from cheers.util import Util
from cheers.model.ormutil import ORMUtil

class CheersModel(object):
	
	def __init__(self):
		pass

	'''
	いいね送信
	'''
	def gift(self, sender, receiver, value, message, is_anonymous):
		db = ORMUtil.initDB()
		User = ORMUtil.getUserORM()
		UserHash = ORMUtil.getUserHashORM()
		GiftTransaction = ORMUtil.getGiftTransactionORM()

		if (db and User and GiftTransaction) is None:
			return None, 100

		#ユーザ存在確認
		try:
			hasSender = db.session.query(User.user_id).filter(User.user_id == sender).first()
			hasReceiver = db.session.query(User.user_id).filter(User.user_id == receiver).first()
		except Exception as exc:
			current_app.logger.critical("gift: hasSender/hasReceiver Unknown error: %s" % exc)
			return None, 199
			
		if (hasSender and hasReceiver) is None:
			return None, 131

		#like残数確認
		if Util.InfiniteMode:
			pass
		else:
			try:
				sender_stock = db.session.query(User.stock).filter(User.user_id == sender).first()
			except Exception as exc:
				current_app.logger.critical("gift: sender_stock Unknown error: %s" % exc)
				return None, 199

			if sender_stock.stock < value:
				return None, 132

		#hash取得
		try:
			result_sender_hash = db.session.query(UserHash.user_hash).filter(UserHash.user_id == sender).first()
			result_receiver_hash = db.session.query(UserHash.user_hash).filter(UserHash.user_id == receiver).first()
		except Exception as exc:
			current_app.logger.critical("gift: get hash Unknown error: %s" % exc)
			return None, 199

		sender_hash = result_sender_hash.user_hash
		receiver_hash = result_receiver_hash.user_hash
		
		if sender_hash is None or receiver_hash is None:
			return None, 133
			
		
		#コミット
		try:
			db.session.add(GiftTransaction(sender_hash, receiver_hash, value, message, is_anonymous, None))
			db.session.query(User).filter(User.user_id == receiver).update({'gift': User.gift + value})
			if Util.InfiniteMode:
				pass
			else:
				db.session.query(User).filter(User.user_id == sender).update({'stock': User.stock - value})
			db.session.commit()
			
		except Exception as exc:
			current_app.logger.critical("gift: commit transaction Unknown error: %s" % exc)
			return None, 199

		return "ok", 0


	'''
	いいね履歴の取得
	'''
	def gifts(self, user_id, mode=None):
		db = ORMUtil.initDB()
		GiftTransaction = ORMUtil.getGiftTransactionORM()
		User = ORMUtil.getUserORM()
		UserHash = ORMUtil.getUserHashORM()
		Profile = ORMUtil.getProfileORM()

		if (db and GiftTransaction and User and UserHash) is None:
			return None, 100

		try:
			result = db.session.query(UserHash.user_hash).filter(UserHash.user_id == user_id).first()
		except Exception as exc:
			return None, 123

		if result is None:
			return None, 124

		user_hash = result.user_hash
		try:
			if mode == "send":
				result = db.session.query(GiftTransaction).filter(GiftTransaction.sender == user_hash).all()
			elif mode == "receive":
				result = db.session.query(GiftTransaction).filter(GiftTransaction.receiver == user_hash).all()
			else:
				result = db.session.query(GiftTransaction).filter(or_(GiftTransaction.sender == user_hash, GiftTransaction.receiver == user_hash)).all()
		except Exception as exc:
			return None, 122

		if result is None:
			return None, 121
		
		events = []

		#ニックネーム取得
		nicknames = {}
		user_ids = {}
		user_ids[user_hash] = user_id
		nicknames[user_hash] = "あなた"
		for event in result:
			for target_hash in [event.sender, event.receiver]:
				if target_hash in nicknames:
					continue
				else:
					try:
						tmp_result = db.session.query(UserHash.user_id).filter(UserHash.user_hash == target_hash).first()
						if tmp_result is None:
							user_ids[target_hash] = ""
							nicknames[target_hash] = "(退会したユーザ)"
						else:
							peer_user_id = tmp_result.user_id
							user_ids[target_hash] = peer_user_id

							tmp_result = db.session.query(Profile.nickname).filter(Profile.user_id == peer_user_id).first()
							peer_nickname = tmp_result.nickname
							#ニックネームが設定されていない場合はuser_idを用いる
							if peer_nickname is None:
								nicknames[target_hash] = peer_user_id
							else:
								nicknames[target_hash] = peer_nickname
					except Exception as exc:
						current_app.logger.critical("gifts getNickname error: %s" % exc)	
						return None, 125
			else:
				continue

		for event in result:
			json = {"date": event.created_at, "sender": user_ids[event.sender], "sender_nickname": nicknames[event.sender], "receiver":user_ids[event.receiver], "receiver_nickname": nicknames[event.receiver], "value": event.value, "message": event.message}
			events.append(json)
		
		if events is not None:
			return events, 0
		else:
			return None, 0

