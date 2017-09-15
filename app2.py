from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# stores
stores = [
	{
		"name": "My Wonderful Store",
		"items": [
			{
				"name": "My Item",
				"price": 15.99 
			}
		]
	}
]

# POST - used to receive data
# GET - used to send data back only

# a render function
@app.route("/")
def home():
	return render_template("index.html")

# by default, @app.route is a GET request

# what we can create:

# POST /store data: {name:}
@app.route("/store", methods=["POST"]) # make is a post request
def create_store():
	request_data = request.get_json() # get data from browser
	new_store = {
		"name": request_data["name"],
		"items": []
	}
	stores.append(new_store)
	return jsonify(new_store)

# GET /store/<string:name>
@app.route("/store/<string:name>") # http://127.0.0.1:5000/store/some_name
def get_store(name):
	# iterate over stores, if name matches, return that one
	# if none match, return an error message (jsonified)
	for store in stores:
		if store["name"] == name:
			return jsonify(store)
	return jsonify({"message": "store not found."})

# GET /store
@app.route("/store")
def get_stores():
	return jsonify({"stores": stores})

# POST /store/<string:name>/item data: {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"]) # make is a post request
def create_item_in_store(name):
	request_data = request.get_json() # get data from browser
	for store in stores:
		if store["name"] == name:
			new_item = {
				"name": request_data["name"],
				"price": request_data["price"]
			}
			store["items"].append(new_item)
			return jsonify(store)
	return jsonify({"message": "store not found."})

# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
	for store in stores:
		if store["name"] == name:
			return jsonify({"items": store["items"]})
	return jsonify({"message": "store not found."})



app.run(port=5000)





