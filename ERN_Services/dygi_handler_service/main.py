import json
from nameko.rpc import rpc
from mongo_utils.query_utils import QueryUtils
from mongo_utils.mongo_builder import MongoBuilder


class DygiHandlerService:

	"""
	Dygi handler service main class with one rpc entrypoint,
	fetch_news which returns ERN labeled document if exists.

    ...

    Attributes
    ----------
	None
	"""

	name = 'dygi_handler_service'

	mongo_builder = MongoBuilder()

	ern_collection = \
		mongo_builder.get_mongodb_collection(collection_name="collection_name")

	def __init__(self):

		self.query_utils = QueryUtils(self.ern_collection)

	@rpc
	def fetch_news(self, data):

		response_content = []

		docs = self.query_utils.fetch_docs(
				skip=data["offset"],
				limit=data["news_count"])

		if docs:

			for doc in docs:

				response_content.append(
					{"id": doc["id"],
					"doc_tokens": doc["doc_tokens"],
					"ner": doc["ner"],
					"events": doc["events"],
					"relations": doc["relations"],
					"sentences": doc["sentences"]})

			response_status = 200

		else:
			
			response_content = []

			response_status = 400

		return {"content": json.dumps(response_content), "status": response_status}

	@rpc
	def read_news(self, data):

		doc = self.query_utils.fetch_doc(
			doc_id=data["id"])

		if doc:

			response_content = {
					"id": doc["id"],
					"doc_tokens": doc["doc_tokens"],
					"ner": doc["ner"],
					"events": doc["events"],
					"relations": doc["relations"],
					"sentences": doc["sentences"]}

			response_status = 200

		else:

			response_content = {}

			response_status = 400

		return {"content": json.dumps(response_content), "status": response_status}
