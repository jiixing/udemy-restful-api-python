from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

	# define a parser and add "price"
	# this is to make sure that when we are updating the dictionary,
	# we do not overwrite fields other than "price"
	parser = reqparse.RequestParser()
	parser.add_argument("price",
		type=float,
		required=True,
		help="This field cannot be left blank."
	)
	parser.add_argument("store_id",
		type=float,
		required=True,
		help="Every item needs a store id."
	)


	# get the item by unique name from db
	@jwt_required() # need authentication for this action
	def get(self, name):
		item = ItemModel.find_by_name(name) # ItemModel object

		if item:
			return item.json()
			
		return {"message": "Item not found."}, 404


	# create a new item if not exist
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {"message": "An item with name '{}' already exists.".format(name)}, 400 # wrong with request
		
		data = Item.parser.parse_args()
		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500 # internal server error

		return item.json(), 201 # code for creating


	# delete the item by unique name
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {"message": "Item deleted."}


	# create or update item
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data["price"]
			item.store_id = data["store_id"]

		item.save_to_db()

		return item.json()


class ItemList(Resource):

	# will return all items
	def get(self):
		return {"items": [item.json() for item in ItemModel.query.all()]}


