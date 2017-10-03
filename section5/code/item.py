import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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


	# get the item by unique name from db
	@jwt_required() # need authentication for this action
	def get(self, name):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		
		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {"item": {"name": row[0], "price": row[1]}}
		return {"message": "Item not found"}, 404


	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		
		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {"item": {"name": row[0], "price": row[1]}}


	# create a new item if not exist
	def post(self, name):

		if self.find_by_name(name):
			return {"message": "An item with name '{}' already exists.".format(name)}, 400
		
		data = Item.parser.parse_args()
		item = {
			"name": name,
			"price": data["price"]
		}

		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?,?)"
		cursor.execute(query, (name, data["price"]))
		
		connection.commit()
		connection.close()

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
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "select * FROM items"
		result = cursor.execute(query)
		rows = result.fetchall()


		return jsonify({"items": items})






