from werkzeug.security import safe_str_cmp # for string compare (safer)
from user import User


# function to authenticate user
def authenticate(username, password):
	user = User.find_by_username(username)
	if user and safe_str_cmp(user.password, password):
		return user


# identity function
def identity(payload): # payload from the request
	user_id = payload["identity"]
	return User.find_by_id(user_id)

