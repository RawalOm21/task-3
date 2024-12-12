from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

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
        new_id = user_list[-1]['id'] + 1
        
        new_obj = {
            "id": new_id,
            "username": new_user,
            "email": new_email,
            "password": new_password
        }
        user_list.append(new_obj)
        return make_response(jsonify(new_obj), 201)

@app.route('/<name>')
def print_name(name):
    return 'Hello, {}'.format(name)  

if __name__ == '__main__':
    app.run()
