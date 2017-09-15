from werkzeug.security import safe_str_cmp # for string compare (safer)
from user import User

# a table of users
users = [
	User(1, "bob", "asdf")
]


# index by username
username_mapping = {u.username: u for u in users}

# index by userid
userid_mapping = {u.id: u for u in users}


# function to authenticate user
def authenticate(username, password):
	user = username_mapping.get(username, None) # we can set a default value with get()
	if user and safe_str_cmp(user.password, password):
		return user


# identity function
def identity(payload):
	user_id = payload["identity"]
	return userid_mapping.get(user_id, None)

