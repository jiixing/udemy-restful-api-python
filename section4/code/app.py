from flask import Flask, jsonify, request # to get data
from flask_restful import Resource, Api, reqparse # for get_data() argument parsing
from flask_jwt import JWT, jwt_required # this is a decorator

from security import authenticate, identity


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


# initialize data
items = []


# class for item
class Item(Resource):

	# define parser here so that we only need to do it once
	# for each call, need to do Item.parser.parse_args()

	# define a parser and add "price"
	# this is to make sure that when we are updating the dictionary,
	# we do not overwrite fields other than "price"
	parser = reqparse.RequestParser()
	parser.add_argument("price",
		type=float,
		required=True,
		help="This field cannot be left blank."
	)

	# get the item by unique name
	@jwt_required() # need authentication for this action
	def get(self, name):
		# next function will return the next item in the list
		# if noting in there, will return None (default value)

		item = next(filter(lambda x: x["name"] == name, items), None) 
		return {"item": item}, 200 if item else 404

	# create a new item
	def post(self, name):
		# if there is a match, return a message

		if next(filter(lambda x: x["name"] == name, items), None):
			return {"message": "An item with name '{0}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		item = {
			"name": name,
			"price": data["price"]
		}
		items.append(item)
		return item, 201 # code for creating

	# delete the item by unique name
	def delete(self, name):
		global items # this items created is the global variable we created before
		items = list(filter(lambda x: x["name"] != name, items))
		return {"message": "Item '{0}' deleted.".format(name)}

	# create or update item
	def put(self, name):

		data = Item.parser.parse_args()

		item = next(filter(lambda x: x["name"] == name, items), None)
		if item is None:
			item = {
				"name": name,
				"price": data["price"]
			}
			items.append(item)
		else:
			item.update(data) # update the dictionary
		return item 


# class for items
class Items(Resource):

	# get all items
	def get(self):
		return jsonify({"items": items})


# add resources
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")

# run
app.run(port=5000, debug=True)





