

class QueryUtils:

	"""
	A class contating a set of functionalities to 
	interact with Mongo database

	...

	Attributes:
		None
	"""

	def __init__(self, collection):

		self.collection = collection	

	def insert(self, doc):
		
		try:

			response = self.collection.insert_one(doc)

		except: pass

	def checkDocExiste(self, docId):

		result = list(
			self.collection.find({"id": docId}))

		response = True if result else False

		return response
