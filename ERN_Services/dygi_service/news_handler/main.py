import json
import requests
from time import sleep
from preprocess import SpacyTokenizer
from mongo_utils.query_utils import QueryUtils
from mongo_utils.mongo_builder import MongoBuilder

url = "http://url"
valid_class=['class', 'class1']

def getNewDocs(ERN_DB):

	new_docs = firstRequest(ERN_DB)

	if (len(new_docs)<1):
		new_docs=nextReuest(ERN_DB)

	if (len(new_docs)<1):
		while(len(new_docs)<1):
			sleep(300)
			new_docs = firstRequest(ERN_DB)

	return new_docs

def firstRequest(ERN_DB):
	parameters = {"news_count": 20, "offset": 0, "keyset": ["id", "text", "class"]}

	data = requests.post(url=url, json=parameters)
	print("status_code_first_request: ",data.status_code)

	new_docs= data.json()
	# new_docs=[doc for doc in new_docs if doc['class'] in valid_class]
	# new_docs=[doc for doc in new_docs if doc['id'] not in exist_doc_ids]
	new_docs=[doc for doc in new_docs if not ERN_DB.checkDocExiste(['id'])]


	print("return in first:",len(new_docs))
	return new_docs

def nextReuest(ERN_DB):
	parameters = {"news_count": 500, "offset": 20, "keyset": ["id", "text", "class"]}

	data = requests.post(url=url, json=parameters)
	print("status_code_next_request: ",data.status_code)

	new_docs= data.json()
	# new_docs=[doc for doc in new_docs if doc['class'] in valid_class and doc['id'] not in exist_doc_ids]
	# new_docs=[doc for doc in new_docs if doc['class'] in valid_class and not ERN_DB.checkDocExiste(doc['id'])]
	new_docs=[doc for doc in new_docs if not ERN_DB.checkDocExiste(doc['id'])]



	new_docs_count=len(new_docs)

	if new_docs_count >= 10:
		new_docs=new_docs[-10:]

	print("return in next:",len(new_docs))
	return new_docs

def tokenCount(doc):
	count=0
	for sent in doc:
		count=count+len(sent)

	return count


if __name__ == '__main__':

	#--------------------------- get tagged doc(s) from database ----------------------------
	mongo_builder = MongoBuilder()

	ern_collection = \
		mongo_builder.get_mongodb_collection(collection_name="ERN")

	ERN_DB = QueryUtils(ern_collection)

	# exist_doc_ids= ERN_DB.getDocIds('id')

	#--------------------------- get new doc from ner service ------------------------------
	new_docs=[]
	try:
		new_docs = getNewDocs(ERN_DB)
	except:
		print("request error")

	#------------------------- preprocess doc to jsonall -------------------------------
	tokeizer= SpacyTokenizer()

	sum_tokns=0
	docs_jsoned=''
	for doc in new_docs:
		doc_sents= tokeizer.docTokenizer(doc['text'])
		# print(len(doc_tokenized))

		doc_tokens=tokenCount(doc)

		sum_tokns = sum_tokns + doc_tokens
		if sum_tokns > 4000:
			break

		if doc_tokens > 2000:
			doc_jsoned={"doc_key": doc['id'], "dataset": "ace-event", "sentences":doc_sents}
			docs_jsoned= json.dumps(doc_jsoned)
			break

		doc_jsoned={"doc_key": doc['id'], "dataset": "ace-event", "sentences":doc_sents}
		docs_jsoned= json.dumps(doc_jsoned)+ '\n' + docs_jsoned
		# ERN_DB.insert(doc_jsoned)

	with open('news_handler/docs.jsonl', 'w') as f:
		f.write(docs_jsoned)

