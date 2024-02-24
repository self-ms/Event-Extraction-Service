import os
from pymongo import MongoClient, DESCENDING


class MongoBuilder:

	"""
	A class to build mongo instance.

	...

	Attributes
	----------
	None
	"""

	def __init__(self):
		
		pass

	@staticmethod
	def get_mongodb_config():
		"""
		Get Mongodb connection configuration to work 
		with data base.

		Args:
			None

		Returns:
			A Mongodb connection dict.
		"""

		mongodb_config = {

			"host": os.environ.get("MONGO_HOST"),
			"port": os.environ.get("MONGO_PORT"),
			"user": os.environ.get("MONGO_USERNAME"),
			"pass": os.environ.get("MONGO_PASSWORD"),
			"name": os.environ.get("MONGO_NAME")
		}

		return mongodb_config

	def select_collection(self, connection, db_name: str, db_collection: str):
		"""
		Select and initiate a Mongo collection object to work with.

		Args:
			connection: A MongoClient connection object 
			db_name: Name of the Mongo database to select or create in case of absence
			db_collection: Name of the Mongo collection to select or create in case of absence

		Returns:
			MongoClient collection object
		"""

		if db_name not in connection.list_database_names():

			print("selected database does not exist! creating now ...")

		db = connection[db_name]

		if db_collection not in db.list_collection_names():

			print("selected collection does not exist! creating now ...")

			collection = db[db_collection]

			collection.create_index([("id", DESCENDING)], unique=True)

		else:

			collection = db[db_collection]

		return collection

	def connect(self, db_user: str, db_pass: str, db_host: str, db_port: str, db_name: str):
		"""
		Initiate a connection to Mongo database.

		Args:
			db_user: Mongo database username
			db_pass: Mongo database password
			db_host: Mongo database host
			db_port: Mongo database port
			db_name: Mongo database name

		Returns:
			MongoClient connection object	
		"""

		uri = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

		connection = MongoClient(uri)

		return connection

	def get_mongodb_collection(self, collection_name):
		"""
		Connect to Mongo database and select collection with
		predefined config variables and provided name.

		Args:
			collection_name: name of the desired collection

		Returns:
			A MongoClient collection object.
		"""

		config = self.get_mongodb_config()

		connection = self.connect(
			db_user=config["user"],
			db_pass=config["pass"],
			db_host=config["host"],
			db_port=config["port"],
			db_name=config["name"])

		collection = self.select_collection(
			connection=connection,
			db_name=config["name"],
			db_collection=collection_name)

		return collection
