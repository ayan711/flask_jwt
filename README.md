Implemented jwt with flask framework.

    1. Needs user creds for login
    2. Generates jwt
    3. Protected APIs required the jwt as Bearer token

For sending response , we are using serializer module marshmallow. 
We are also doing custom validation via this module.

We have added migration feature which has following commands.

    1. python3 manage.py db init   
    2. python3 manage.py db migrate
    3. python3 manage.py db upgrade
    4. python3 manage.py db downgrade

--> Refering to project - https://github.com/CryceTruly/bookmarker-api/tree/main/src
