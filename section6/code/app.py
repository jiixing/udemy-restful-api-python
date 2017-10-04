from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList


# setup
app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)


jwt = JWT(app, authenticate, identity)
# creates a new endpoint: /auth
# send a username and password
# then it sends info to authenticate function
# find the correct user object using username
# compare pwd
# if match, return the user, and /auth end point returns a JW token
# wich can then be used to identify authenticated user


# add resources
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

# run
app.run(port=5000, debug=True)





