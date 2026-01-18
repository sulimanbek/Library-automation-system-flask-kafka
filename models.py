# app/models.py
from app import mongo
from bson import ObjectId  # Import ObjectId for handling _id
from pymongo import MongoClient

# Establish a connection to the MongoDB server
client = MongoClient('localhost', 5001)
db = client.library

class Book:
    def __init__(self, title, author, isbn):
        self._id = ObjectId()  # Generate a new ObjectId for each book
        self.title = title
        self.author = author
        self.isbn = isbn

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['isbn'])

    def save(self):
        try:
            result = mongo.db.books.insert_one(self.__dict__)
            return str(result.inserted_id)  # Return the ID of the newly inserted document
        except Exception as e:
            return str(e)  # Handle the exception as needed

    @staticmethod
    def get_all():
        try:
            books = list(mongo.db.books.find())
            return books
        except Exception as e:
            return str(e)

    @staticmethod
    def get_by_id(book_id):
        try:
            book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
            return book
        except Exception as e:
            return str(e)

    def update(self):
        try:
            result = mongo.db.books.update_one({"_id": self._id}, {"$set": self.__dict__})
            return result.modified_count > 0  # Check if any document was modified
        except Exception as e:
            return str(e)

    @staticmethod
    def delete(book_id):
        try:
            result = mongo.db.books.delete_one({"_id": ObjectId(book_id)})
            return result.deleted_count > 0  # Check if any document was deleted
        except Exception as e:
            return str(e)
