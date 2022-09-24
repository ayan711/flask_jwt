from flask import Blueprint,jsonify,request,make_response


from werkzeug.security import generate_password_hash,check_password_hash
import uuid , datetime , jwt ,os

from src.models import Users,db,Books
from src.serializers import book_schema,books_schema
from marshmallow import Schema, fields, ValidationError
from src.utils.http_status_code import *

from src.auth import token_required


books = Blueprint("books",__name__,url_prefix='')

@books.post('/book')
@token_required
def create_book(current_user):
 
    data = request.get_json()
    print(data)

    try:
        data = book_schema.load(data)
        
    except ValidationError as err:
        return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

    if 'book_prize' not in data:
        data['book_prize'] = None
        
    try :
        
        new_books = Books(name=data['name'], Author=data['Author'], Publisher=data['Publisher'], book_prize=data['book_prize'], user_id=current_user.id) 
        db.session.add(new_books)  
        db.session.commit() 
        
    except Exception as err:
        
        db.session.rollback()
        print("Rollbacked ---------------------------")
        
        return jsonify({'message' : str(err)}),HTTP_400_BAD_REQUEST

    return jsonify({'message' : 'new books created','data':book_schema.dump(data)})

@books.get('/books')
@token_required
def get_books(current_user):
 
   books = Books.query.filter_by(user_id=current_user.id).all()

 
   return jsonify({'list_of_books' : books_schema.dump(books)}),HTTP_200_OK
