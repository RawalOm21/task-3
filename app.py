
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import random
from datetime import timedelta
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = random._urandom(32)
#token creation and expiration time  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=20)
jwt = JWTManager(app)

@app.route('/')
def index():
    return 'Hello World'

user_list = [
    {
        "id": 0,
        "username": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    },
    {
        "id": 1,
        "username": "Bob",
        "email": "bob@example.com",
        "password": "password456"
    },
    {
        "id": 2,
        "username": "Charlie",
        "email": "charlie@example.com",
        "password": "password789"
    }
]

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = next((user for user in user_list if user['username'] == username and user['password'] == password), None)
    if user is None:
        return make_response(jsonify({"msg": "Bad username or password"}), 401)
    #delay simulation 
    delay_time = 5
    access_token = create_access_token(identity=username)
    return jsonify({"msg":f"Token created in {delay_time} minutes", "access_token": access_token}), 200

@app.route('/users', methods=['GET', 'POST'])
@jwt_required()# automatic authentication occurs here 
def users():
    if request.method == 'GET':
        if len(user_list) > 0:
            return make_response(jsonify(user_list), 200)
        else:
            return make_response('Nothing found', 404)
    if request.method == 'POST':
        new_user = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']
        new_id = user_list[-1]['id'] + 1
        
        new_obj = {
            "id": new_id,
            "username": new_user,
            "email": new_email,
            "password": new_password
        }
        user_list.append(new_obj)
        return make_response(jsonify(new_obj), 201)

@app.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    identity = get_jwt_identity()  # Retrieve the identity of the current token
    return jsonify({"msg": "Token is valid", "identity": identity}), 200


if __name__ == '__main__':
    app.run(debug=True)

"""

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

user_list = [
    {

        "username": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    },
    {

        "username": "Bob",
        "email": "bob@example.com",
        "password": "password456"
    },
    {
        "username": "Charlie",
        "email": "charlie@example.com",
        "password": "password789"
    }
]

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        if len(user_list) > 0:
            return make_response(jsonify(user_list), 200)
        else:
            return make_response('Nothing found', 404)
        
    if request.method == 'POST':
        new_user = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']

        
        new_obj = {

            "username": new_user,
            "email": new_email,
            "password": new_password
        }
        user_list.append(new_obj)
        return make_response(jsonify(new_obj), 201)
    
@app.route('/deluser', methods=['POST'])
def deluser():
    print("Received a POST request to /deluser")  
    global user_list
    user_list = []
    return make_response('User list cleared', 200)


if __name__ == '__main__':
    app.run(debug=True)
"""