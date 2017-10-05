from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# setup
app = Flask(__name__)

# tell sqlalchemy the location of the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" 

# this turns off the flask sqlalchemy track not the real sqlalchemy one
app.config['SQLIALCHEMY_TRACK_MODIFICATIONS'] = False 

app.secret_key = "jose"
api = Api(app)


# create db before all request is run
@app.before_first_request
def create_tables():
	db.create_all()


jwt = JWT(app, authenticate, identity)
# creates a new endpoint: /auth
# send a username and password
# then it sends info to authenticate function
# find the correct user object using username
# compare pwd
# if match, return the user, and /auth end point returns a JW token
# wich can then be used to identify authenticated user


# add resources
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")


# run
if __name__ == "__main__":
	# avoid circular import
	from db import db
	db.init_app(app)

	app.run(port=5000, debug=True)

