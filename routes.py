from flask import Flask, Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask import Blueprint


# Initialize Flask and Blueprint
app = Flask(__name__)
library_api = Blueprint('library_api', __name__)

# MongoDB setup (adjust the connection string and database name as needed)
client = MongoClient('mongodb://localhost:5001/')
db = client['library_db']
books_collection = db['books']
users_collection = db['users']
borrowing_collection = db['borrowing_records']
module1 = Blueprint('module1', __name__)

@module1.route('/route1')
def route1():
    return "Welcome to the Library Automation System"

@app.route('/books', methods=['GET'])
def search_books():
    query = request.args.get('query')
    if query:
        search_results = books_collection.find({"$or": [{"title": {"$regex": query, "$options": "i"}}, {"description": {"$regex": query, "$options": "i"}}]})
    else:
        search_results = books_collection.find()

    books = [{"title": book["title"], "author": book["author"], "description": book["description"]} for book in search_results]
    return jsonify({'books': books})

@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    # Add validation logic for user_data if necessary
    users_collection.insert_one(user_data)
    return jsonify({'message': 'User registered successfully'})

@app.route('/borrow', methods=['POST'])
def borrow_book():
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')
    # Implement borrowing logic, like checking if the book is available, etc.
    borrowing_collection.insert_one({"user_id": user_id, "book_id": book_id, "borrow_date": datetime.now()})
    return jsonify({'message': 'Book borrowed successfully'})

@app.route('/return', methods=['POST'])
def return_book():
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')
    # Implement return logic, such as updating the borrowing record
    borrowing_collection.update_one({"user_id": user_id, "book_id": book_id}, {"$set": {"return_date": datetime.now()}})
    return jsonify({'message': 'Book returned successfully'})

# Register the blueprint
app.register_blueprint(library_api)

if __name__ == '__main__':
    app.run(debug=True)
