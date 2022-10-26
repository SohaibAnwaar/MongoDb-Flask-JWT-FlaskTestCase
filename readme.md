# Flask with MongoDB and JWT Authentication.
In this tasks, I tried to make a software which use Flask and mongo db with JWT Token authentication. Idea is to Register a user, A user can manage their templates (Select, Update, Delete, Insert).

### EndPoints
1. Register User
2. Login User (With JWT)
3. Insert Templates
4. Select All Templates
5. Update Template
6. Delete Template


## Code Part:
Import all of the necessary Modules

```python
from flask import Flask
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime
import hashlib
import urllib
```

Setup JWT Authentication

```python
app = Flask(__name__)
jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = '38dd56f56d405e02ec0ba4be4607eaab'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token
```
The JWT secret can be get through the secret library. 
1. Go to the terminal
2. Type these lines of code
```python
>>> import secrets
>>> secrets.token_hex(16)
'38dd56f56d405e02ec0ba4be4607eaab'
```

Setup Mongo Database, I created this database online on mongodb. 
follow this link to create online mongo db database
https://www.mongodb.com/docs/atlas/online-archive/connect-to-online-archive/

```python
client = MongoClient("mongodb+srv://Sohaib:sohaib@cluster0.ljdhvgj.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]
users_collection = db["users"]
templates_collection = db["templates"]
```

Simple Hello world route to check if everything is working fine.
```python
@app.route('/')
def hello_world():
	return 'Hello, World!'
```

After completing this go to the terminal and start the application. I am writing this code in main.py file.
Please do install the requirements before starting the application. 
```pip install -r requirements.txt```

```
python main.py
```

### **Registration API**
Now Lets make an endpoint to register user. 

```python
@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request
    # Creating Hash of password to store in the database
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    # Checking if user already exists
    doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
    # If not exists than create one
    if not doc:
        # Creating user
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409
```
To Check this endpoint, go to the terminal start the application. After that open your postman hit the URL like this.

```curl
http://localhost:5000/api/v1/users

```
Body of the Endpoint
```json
{
  "username":"sohaib123", 
  "password":"sohaib123"
}
```
Response of Endpoint
```json
{
  "msg": "User created successfully"
}
```
![Registration Screenshot](attachments/Register.png)

### **Login User**
This endpoint is used for the user login

```python
@app.route("/api/v1/login", methods=["post"])
def login():
    # Getting the login Details from payload
    login_details = request.get_json() # store the json body request
    # Checking if user exists in database or not
    user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database
    # If user exists
    if user_from_db:
        # Check if password is correct
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Create JWT Access Token
            access_token = create_access_token(identity=user_from_db['username']) # create jwt token
            # Return Token
            return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'The username or password is incorrect'}), 401
```
```curl
http://localhost:5000/api/v1/login

```
Body of the Endpoint
```json
{
  "username":"sohaib123", 
  "password":"sohaib123"
}
```
Response of Endpoint
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njc4MDg2MywianRpIjoiNTM2Zjg2MTQtODllZi00YWI1LWIxNDgtNmYxOTAxYTYyMDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvaGFpYjEyMyIsIm5iZiI6MTY2Njc4MDg2MywiZXhwIjoxNjY2ODY3MjYzfQ.IRsLXY2hugjJkmtpHi79X8JgueXUmDIzYC7DlYIQD_A"
}
```
![Registration Screenshot](attachments/login.png)

### **Create Template**
Creating templatet, template here is only a demo object, You can create book, car, bike etc
```@jwt_required()``` this line help us to validate if the access token is valid or not
```python
@app.route("/create", methods=["POST"])
@jwt_required()
def create_template():
    """Creating the template with respect to the user

    Returns:
        dict: Return the profile and template created
    """
    # Getting the user from access token
    current_user = get_jwt_identity() # Get the identity of the current user
    user_from_db = users_collection.find_one({'username' : current_user})
    
    # Checking if user exists
    if user_from_db:
        # Getting the template details from json
        template_details = request.get_json() # store the json body request
        # Viewing if templated already present in collection
        user_template = {'profile' : user_from_db["username"],  "template": template_details["template"]}
        doc = templates_collection.find_one(user_template) # check if user exist
        # Creating collection if not exists
        
        if not doc:
            templates_collection.insert_one(user_template)
            print("user_template ", user_template)
            return jsonify({'msg': 'Template created successfully'}), 200
        # Returning message if template exists
        else: return jsonify({'msg': 'Template already exists on your profile'}), 404
    else:
        return jsonify({'msg': 'Access Token Expired'}), 404
```

```curl
http://localhost:5000/create
```
Body of Endpoint
```json
{
  "template":"My First Template"
}
```
Response of Endpoint 
```json
{
  "msg": "Template created successfully"
}
```
Giving the access token in auth option of postman
```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njc4MDg2MywianRpIjoiNTM2Zjg2MTQtODllZi00YWI1LWIxNDgtNmYxOTAxYTYyMDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvaGFpYjEyMyIsIm5iZiI6MTY2Njc4MDg2MywiZXhwIjoxNjY2ODY3MjYzfQ.IRsLXY2hugjJkmtpHi79X8JgueXUmDIzYC7DlYIQD_A
```
Access Token
![Registration Screenshot](attachments/access_token.png)

Creation endpoint
![Registration Screenshot](attachments/create_template.png)


### **Get All Templates**
Getting all templates of a specefic User
```@jwt_required()``` this line help us to validate if the access token is valid or not
```python
@app.route("/get", methods=["GET"])
@jwt_required()
def get_template():
    """Get the templates of specefic user

    Returns:
        dict: Return the profile and template 
    """
    # Getting the user from access token
    current_user = get_jwt_identity() # Get the identity of the current user
    user_from_db = users_collection.find_one({'username' : current_user})
    # Checking if user exists
    if user_from_db:
        # Viewing if templated already present in collection
        user_template = {'profile' : user_from_db["username"]}
        return jsonify({"docs":list(db.templates.find(user_template, {"_id":0}))}), 200
    else:
        return jsonify({'msg': 'Access Token Expired'}), 404
```

```curl
http://localhost:5000/get
```

Response of Endpoint 
```json
{
  "docs": [
    {
      "profile": "sohaib123",
      "template": "My First Template"
    }
  ]
}
```
Giving the access token in auth option of postman
```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njc4MDg2MywianRpIjoiNTM2Zjg2MTQtODllZi00YWI1LWIxNDgtNmYxOTAxYTYyMDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvaGFpYjEyMyIsIm5iZiI6MTY2Njc4MDg2MywiZXhwIjoxNjY2ODY3MjYzfQ.IRsLXY2hugjJkmtpHi79X8JgueXUmDIzYC7DlYIQD_A
```
Access Token
![Access Screenshot](attachments/access_token.png)

Creation endpoint
![Get Screenshot](attachments/get.png)



### **Update Templates**
Update template
```@jwt_required()``` this line help us to validate if the access token is valid or not
```python
@app.route("/update", methods=["POST"])
@jwt_required()
def update_template():
    """Updating the template with respect to the user

    Returns:
        dict: Return the profile and template created
    """
    # Getting the user from access token
    current_user = get_jwt_identity() # Get the identity of the current user
    user_from_db = users_collection.find_one({'username' : current_user})
    
    # Checking if user exists
    if user_from_db:
        # Getting the template details from json
        template_details = request.get_json() # store the json body request
        # Viewing if templated already present in collection
        user_template = {'profile' : user_from_db["username"],  "template": template_details["old_template"]}
        doc = templates_collection.find_one(user_template) # check if user exist
        # Updating collection if not exists
        
        if doc:
            doc["template"] = template_details["new_template"]
            templates_collection.update_one(user_template, {"$set": {"template":doc["template"]}}, upsert=False)
            return jsonify({'msg': 'Template Updated successfully'}), 200
        # Returning message if template exists
        else: return jsonify({'msg': 'Template not exists on your profile'}), 404
    else:
        return jsonify({'msg': 'Access Token Expired'}), 404
```

```curl
http://localhost:5000/update
```
Body of Endpoint
```json
{
  "old_template":"My First Template",
  "new_template":"My First Updated Template"
}
```
Response of Endpoint 
```json
{
  "msg": "Template Updated successfully"
}
```
Giving the access token in auth option of postman
```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njc4MDg2MywianRpIjoiNTM2Zjg2MTQtODllZi00YWI1LWIxNDgtNmYxOTAxYTYyMDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvaGFpYjEyMyIsIm5iZiI6MTY2Njc4MDg2MywiZXhwIjoxNjY2ODY3MjYzfQ.IRsLXY2hugjJkmtpHi79X8JgueXUmDIzYC7DlYIQD_A
```
Access Token
![Access Screenshot](attachments/access_token.png)

Updation endpoint
![Get Screenshot](attachments/update.png)

Checking if updated in db or not
![Get Screenshot](attachments/db_update.png)



### **Delete Templates**
Update template
```@jwt_required()``` this line help us to validate if the access token is valid or not
```python
@app.route("/delete", methods=["POST"])
@jwt_required()
def delete_template():
    """Creating the template with respect to the user

    Returns:
        dict: Return the profile and template created
    """
    # Getting the user from access token
    current_user = get_jwt_identity() # Get the identity of the current user
    user_from_db = users_collection.find_one({'username' : current_user})
    
    # Checking if user exists
    if user_from_db:
        # Getting the template details from json
        template_details = request.get_json() # store the json body request
        # Viewing if templated already present in collection
        user_template = {'profile' : user_from_db["username"],  "template": template_details["template"]}
        doc = templates_collection.find_one(user_template) # check if user exist
        # Creating collection if not exists
        
        if doc:
            templates_collection.delete_one(user_template)
            print("user_template ", user_template)
            return jsonify({'msg': 'Template Deleted Sucessfully'}), 404
        # Returning message if template exists
        else: return jsonify({'msg': 'Template not exists on your profile'}), 404
    else:
        return jsonify({'msg': 'Access Token Expired'}), 404
```

```curl
http://localhost:5000/delete
```
Body of Endpoint
```json
{
  "template":"My First Updated Template"
}
```
Response of Endpoint 
```json
{
  "msg": "Template Deleted Sucessfully"
}
```
Giving the access token in auth option of postman
```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njc4MDg2MywianRpIjoiNTM2Zjg2MTQtODllZi00YWI1LWIxNDgtNmYxOTAxYTYyMDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvaGFpYjEyMyIsIm5iZiI6MTY2Njc4MDg2MywiZXhwIjoxNjY2ODY3MjYzfQ.IRsLXY2hugjJkmtpHi79X8JgueXUmDIzYC7DlYIQD_A
```
Access Token
![Access Screenshot](attachments/access_token.png)

Updation endpoint
![Get Screenshot](attachments/delete.png)

Checking if deleted from db or not
![Get Screenshot](attachments/db_delete.png)

So this is how we can make a JWT authenticatioin software with the help of flask, MongoDB. Hope you liked In Blog.

## TestCases

Now Lets write the testcases for the endpoints. I wrote 3 testcases, 
1. Main endpoint
2. Registration
3. Login

```python



import json
from flask import Flask
from main import app


def test_flask():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
       
def test_registration():
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        data = {
            "username":"test1",
            "password":"1234"
        }
        response = test_client.post('/api/v1/users', data=json.dumps(data), headers={"Content-Type": "application/json"})
        assert response.status_code == 201 or response.status_code == 409

def test_login():
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        data = {
            "username":"test1",
            "password":"1234"
        }
        response = test_client.post('/api/v1/login', data=json.dumps(data), headers={"Content-Type": "application/json"})
        assert response.status_code == 200
```

Now go to the terminal and write, ```pytest```

![Get Screenshot](attachments/testcase.png)



# Author 

* Sohaib Anwaar
* gmail          : sohaibanwaar36@gmail.com
* linkedin       : [Have Some Professional Talk here](https://www.linkedin.com/in/sohaib-anwaar-4b7ba1187/)
* Stack Overflow : [Get my help Here](https://stackoverflow.com/users/7959545/sohaib-anwaar)
* Kaggle         : [View my master-pieces here](https://www.kaggle.com/sohaibanwaar1203)