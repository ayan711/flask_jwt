Implemented jwt wit flask framework.

    1. Needs user creds for login
    2. Generates jwt
    3. Protected APIs required the jwt as Bearer token

For sending response , we are using serializer module marshmallow. We are also doing custom validation via this module.

We have added migration feature which has following commands :
    a. python3 manage.py db init   
	b. python3 manage.py db migrate
    c. python3 manage.py db upgrade
    d. python3 manage.py db downgrade