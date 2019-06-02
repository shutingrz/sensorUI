import hmac, hashlib, string, secrets

class Util():

	MaxUserIdLength = 64
	MaxUserPassLength = 64
	DefaultStockValue = 100
	InfiniteMode = True
	DebugMode = True
	
	@classmethod
	def generateRandomBytes(self, length, seq=string.digits + string.ascii_lowercase):
		rand_str = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
		rand_bytes = rand_str.encode('ascii')
		return rand_bytes

	@classmethod
	def getEncryptedPassword(self, key, password):
		password_bytes = password.encode('utf-8')
		return hmac.new(key, password_bytes, hashlib.sha256).hexdigest()	

	@classmethod
	def generateUserHash(self, user_id):
		key = self.generateRandomBytes(32)
		user_id_bytes = user_id.encode('utf-8')
		userHash = hmac.new(key, user_id_bytes, hashlib.md5).hexdigest()
		return userHash
