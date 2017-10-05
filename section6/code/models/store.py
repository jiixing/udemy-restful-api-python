from db import db


class StoreModel(db.Model):

	# tell sqlalchemy db and column information
	__tablename__ = "stores"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	items = db.relationship("ItemModel", lazy="dynamic")
	# lazy: this will be loaded only when requested
	# will need to change self.items -> self.items.all()

	# trade off:
	# - dynamic: will take time each time when requested
	# - otherwise: takes time when creating the store object for the first time

	def __init__(self, name):
		self.name = name


	# return store name and all items within the store
	def json(self):
		return {"name": self.name, "items": [item.json() for item in self.items.all()]}


	@classmethod
	def find_by_name(cls, name):
		# .query is from the db.Model class
		# the same as "SELECT * FROM items WHERE name=name LIMIT 1"
		return cls.query.filter_by(name=name).first()


	# this will do both insert and update
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

