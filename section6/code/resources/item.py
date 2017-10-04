import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


# class for item
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
		item = ItemModel(name, data["price"])

		try:
			item.insert()
		except:
			return {"message": "An error occurred inserting the item."}, 500 # internal server error

		return item.json(), 201 # code for creating


	# delete the item by unique name
	def delete(self, name):

		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()

		return {"message": "Item '{0}' deleted.".format(name)}


	# create or update item
	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		updated_item = ItemModel(name, data["price"])

		if item is None:
			try:
				updated_item.insert()
			except:
				return {"message": "An error occurred inserting the item."}, 500
		else:
			try:
				updated_item.update()
			except:
				return {"message": "An error occurred updating the item."}, 500
		return updated_item.json()


# class for items
class ItemList(Resource):

	# get all items
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "select * FROM items"
		result = cursor.execute(query)

		items = []
		for row in result:
			items.append({"name": row[0], "price": row[1]})
		
		connection.close()

		return jsonify({"items": items})






