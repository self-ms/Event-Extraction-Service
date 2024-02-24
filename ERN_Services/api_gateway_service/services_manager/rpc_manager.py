import os
from nameko.standalone.rpc import ClusterRpcProxy


class RpcManager:

	"""
	A RPC manager class to interact with dygi handler
	rpc entrypoints and handle fast API requests

	...

	Attributes
	----------
	None
	"""

	def __init__(self):

		pass

	@staticmethod
	def get_rabbit_connection():
		"""
		Get RabbitMQ connection configuration to work 
		with rpc entrypoints.

		Args:
			None

		Returns:
			A RabbitMQ connection string.
		"""

		RABBIT_USER = os.environ.get("RABBIT_USER")

		RABBIT_PASSWORD = os.environ.get("RABBIT_PASSWORD")

		RABBIT_HOST = os.environ.get("RABBIT_HOST")

		RABBIT_PORT = os.environ.get("RABBIT_PORT")

		RABBIT_CONFIG = {
			"AMQP_URI": f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/"}

		return RABBIT_CONFIG

	@classmethod
	def handler_service_fetch_news(cls, data):
		"""
		A class method to call dygi handler service fetch_news 
		entrypoint, pass parameters and get responses.

		Args:
			data: Dict of required data.

		Returns:
			Response from fetch_news rpc.
		"""

		with ClusterRpcProxy(cls.get_rabbit_connection()) as rpc:

			response = rpc.dygi_handler_service.fetch_news(data)

		return response

	@classmethod
	def handler_service_read_news(cls, data):
		"""
		A class method to call ner handler service read_news 
		entrypoint, pass parameters and get responses.

		Args:
			data: Dict of required data.

		Returns:
			Response from read_news rpc.
		"""

		with ClusterRpcProxy(cls.get_rabbit_connection()) as rpc:

			response = rpc.dygi_handler_service.read_news(data)

		return response
