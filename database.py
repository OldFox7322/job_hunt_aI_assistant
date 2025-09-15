import pymongo
import logging
from pymongo.mongo_client import MongoClient 
from pymongo.server_api import ServerApi 
from pymongo.errors import DuplicateKeyError, OperationFailure, ConnectionFailure, BulkWriteError
from pydantic import BaseModel
from typing import Optional, Dict, List



logger = logging.getLogger(__name__)


class VacancyData(BaseModel):
	url: str
	text_content: str



class BaseDBManager:
	def __init__(self, db_name: str, collection_name: str):
		self.uri = "mongodb://localhost:27017/"
		self.client: Optional[MongoClient] = None
		self.db: Optional[pymongo.database.Database] = None
		self.collection: Optional[pymongo.collection.Collection] = None

		try:
			self.client = MongoClient(self.uri)
			self.db = self.client.get_database(db_name)
			self.collection = self.db.get_collection(collection_name)
			try:
				self.collection.create_index('url', unique=True)
			except OperationFailure as e:
				logging.warning(f'The index at ‘url’ already exists. Error: {e}')
		except ConnectionFailure as e:
			logging.error(f'Error connecting to MongoDB: {e}')


			

	def get_data(self, query: Dict[str, str]={}) -> List[Dict[str, str]]:
		if self.collection is None:
			logging.error("Unable to retrieve data: no connection to MongoDB.")
			return []
		try:
			documents = list(self.collection.find(query))
			return documents
		except Exception as e:
			logging.error(f'Error when receiving data from MongoDB: {e}')
			return []

	def save_data(self, data_dict: Dict[str, str]) -> None:
		if self.collection is None:
			return
		validated_documents = []
		try:
			for url, text_content in data_dict.items():
				validated_item = VacancyData(url=url, text_content=text_content)
				doc = validated_item.model_dump()
				doc['_id'] = doc['url']
				validated_documents.append(doc)
		except ValidationError as e:
			logging.error(f'Data validation error: {e}')
			return

		try:
			if validated_documents:
				self.collection.insert_many(validated_documents, ordered=False)
		except BulkWriteError as e:
			logging.error(f'Bulk write operation failed: {e}')
		except DuplicateKeyError as e:
			logging.warning(f'Some data already exists. Error: {e}')
		except Exception as e:
			logging.error(f'Error saving to MongoDB: {e}')







class DescriptionVacancies(BaseDBManager):
	def __init__(self, db_name="djinni_scraper_db"):
		super().__init__(db_name, 'description_vacancies')





class CoverLetterVacancies(BaseDBManager):
	def __init__(self, db_name="djinni_scraper_db"):
		super().__init__(db_name, 'cover_letter_vacancies')





























