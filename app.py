import json
from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
from config import Config
from flask_swagger import swagger


app = Flask(__name__)
 
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

 
db = SQLAlchemy(app)

from models import *
from serializers import book_schema,books_schema
from marshmallow import Schema, fields, ValidationError

@app.route('/')
def hello():
    return jsonify({"message":"Hello World!"}),200

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Bookstore API"
    return jsonify(swag)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None

        #    print(vars(request))
       
       if request.headers['Authorization']:

            token = (request.headers['Authorization']).split(' ')[1]
           
        #    if 'x-access-tokens' in request.headers:
        #        token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           
           data = jwt.decode(token,Config.SECRET_KEY, algorithms=["HS256"])
           current_user = Users.query.filter_by(public_id=data['public_id']).first()
           
       except:
           
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator


@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json()
   print(data) 
   hashed_password = generate_password_hash(data['password'], method='sha256')

   new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'}),201


@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   user = Users.query.filter_by(name=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
   return make_response({'messgae':'could not verify'},  401, {'Authentication': '"login required"'})

@app.route('/delete_user/<user_id>',methods=['POST'])
@token_required
def delete_user(current_user,user_id):
    
    admin = (Users.query.filter_by(id=current_user.id).first()).admin
    
    
    if  not admin :
        
        return jsonify({"message":"Admin access required"}),401
    
    user = Users.query.filter_by(id=user_id).first()
    
    if not user:
        
        return jsonify({"message":"User not found"},404)
    
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message":"User deleted"}),204


@app.route('/users', methods=['GET'])
def get_all_users(): 
 
   users = Users.query.all()
   result = []  
   for user in users:  
       user_data = {}  
       user_data['public_id'] = user.public_id 
       user_data['name'] = user.name
       user_data['password'] = user.password
       user_data['admin'] = user.admin
     
       result.append(user_data)  
   return jsonify({'users': result})

@app.route('/book', methods=['POST'])
@token_required
def create_book(current_user):
 
    data = request.get_json()

    try:
        data = book_schema.load(data)
    except ValidationError as err:
        return err.messages, 422

    if 'book_prize' not in data:
        data['book_prize'] = None
        
    try :
        
        new_books = Books(name=data['name'], Author=data['Author'], Publisher=data['Publisher'], book_prize=data['book_prize'], user_id=current_user.id) 
        db.session.add(new_books)  
        db.session.commit() 
        
    except Exception as err:
        
        db.session.rollback()
        print("Rollbacked ---------------------------")
        
        return jsonify({'message' : str(err)}),400

    return jsonify({'message' : 'new books created','data':book_schema.dump(data)})

@app.route('/books', methods=['GET'])
@token_required
def get_books(current_user):
 
   books = Books.query.filter_by(user_id=current_user.id).all()

 
   return jsonify({'list_of_books' : books_schema.dump(books)})

if __name__ == '__main__':
    app.run(debug=True)