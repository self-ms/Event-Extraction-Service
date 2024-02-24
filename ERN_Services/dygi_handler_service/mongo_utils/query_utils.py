from pymongo import DESCENDING


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

	def fetch_docs(self, skip: int, limit: int):
		"""
		Fetch some documents from Mongo DB using
		provided count and offset.

		Args:
			skip: Number of document to skip from fetched result.
			limit: Document count to fetch from Mongo database.

		Returns:
			A document containing id, text,
			sentences, and etc. fields.
		"""

		response = list(
			self.collection.find().skip(skip).limit(limit).sort("date", DESCENDING))

		return response

	def fetch_doc(self, doc_id: str):
		"""
		Fetch a document from Mongo DB using
		document id.

		Args:
			doc_id: Document id

		Returns:
			A document containing id, text,
			sentences, and etc. fields.
		"""

		result = list(
			self.collection.find({"id": doc_id}))

		response = result[0] if result else None

		return response
