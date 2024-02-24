from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from services_manager.rpc_manager import RpcManager


# Initiate a fast API instance and adding CORS policy settings
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.post('/fetch_news')
def fetch_news(news_count: int = Form(...), offset: int = Form(...)):
	"""
	A fastAPI endpoint to fetch news from
	data base with provided count and offset.

	Args:
		news_count: Document count to fetch from Arango database.
		offset: Number of document to skip from fetched result.

	Returns:
		Response from fetch_news rpc.
	"""

	data = {"news_count": news_count, "offset": offset}

	response = RpcManager.handler_service_fetch_news(data)

	return Response(content=response["content"], status_code=response["status"], media_type="application/json")

@app.post('/read_news')
def read_news(id: str = Form(...)):
	"""
	A fastAPI endpoint to read a news from 
	data base and return tags if exist.

	Args:
		id: Document id to save or modify inside Arango database.

	Returns:
		Response from read_news rpc.
	"""

	data = {"id": id}

	response = RpcManager.handler_service_read_news(data)

	return Response(content=response["content"], status_code=response["status"], media_type="application/json")