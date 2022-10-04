from flask import Flask, request, jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(100))
    desc_book = db.Column(db.String(1000))
    price = db.Column(db.String(100))

    def __init__(self, book_name, desc_book, price):
        self.book_name = book_name
        self.desc_book = desc_book
        self.price = price

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book', 'desc_book', 'price')
        
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reader_name = db.Column(db.String(100))
    reader_type = db.Column(db.String(100))
    
    def __init__(self, reader_name, reader_type):
        self.reader_name = reader_name
        self.reader_type = reader_type
        
class ReaderSchema(ma.Schema):
    class Meta:
        fields = (íd','reader_name','reader_type')
        
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/')
def home():
    return "<h6>welcome to bookstore api</h6>"

@app.route('/books/add', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    desc_book = request.json['desc_book']
    price = request.json['price']
    new_book = Book(book_name, desc_book, price)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

@app.route('/books/all', methods=['GET'])
def get_book():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)


@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    book_name = request.json['book_name']
    desc_book = request.json['desc_book']
    price = request.json['price']

    book.book_name = book_name
    book.desc_book = desc_book
    book.price = price

    db.session.commit()
    return book_schema.jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)
