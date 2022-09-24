import imp
from flask import Blueprint,jsonify,request,make_response
from functools import wraps

from werkzeug.security import generate_password_hash,check_password_hash
import uuid , datetime , jwt ,os

from src.models import Users,db
from src.serializers import book_schema,books_schema
from marshmallow import Schema, fields, ValidationError
from src.utils.http_status_code import *
from src.config.config import Config

from dotenv import load_dotenv
load_dotenv()

auth = Blueprint("auth",__name__,url_prefix='/auth')

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None

        print(vars(request))
        
        try:
       
            if request.headers['Authorization']:

                token = (request.headers['Authorization']).split(' ')[1]
                
        except Exception as e :
            
            return jsonify({'message': 'Auth token required'}),401
            
        #    if 'x-access-tokens' in request.headers:
        #        token = request.headers['x-access-tokens']
 
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            
            data = jwt.decode(token,Config.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            
        except:
            
            return jsonify({'message': 'token is invalid'}),HTTP_401_UNAUTHORIZED
    
        return f(current_user, *args, **kwargs)
   return decorator



@auth.post('/register')
def signup_user(): 
   data = request.get_json()
   print(data) 
   hashed_password = generate_password_hash(data['password'], method='sha256')

   new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'}),HTTP_201_CREATED


@auth.post('/login')
def login_user():
    
   auth = request.authorization  
   
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', HTTP_401_UNAUTHORIZED, {'Authentication': 'login required"'})   
 
   user = Users.query.filter_by(name=auth.username).first()
       
   
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, os.environ.get('SECRET_KEY'), "HS256")
    #    token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, '004f2af45d3a4e161a7dd2d17fdae47f', "HS256")
  
       return jsonify({'token' : token})
 
   return make_response({'messgae':'could not verify'},  HTTP_401_UNAUTHORIZED, {'Authentication': '"login required"'})

@auth.get('/test')
def test():
 
   return make_response({'messgae':'Auth blueprint working'},  HTTP_200_OK)

