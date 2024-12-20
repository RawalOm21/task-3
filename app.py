from flask import Flask, request, jsonify, send_from_directory, make_response
import json
import sqlite3
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, get_jwt
from app_config import Config
from user import add_user, get_all_users
from datetime import timedelta, datetime

app = Flask(__name__)
app.config.from_object(Config)


jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route("/")
def index():
    return "Welcome to the Book API!"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    audience = request.json.get('audience', None)
    users = get_all_users()
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user is None:
        return make_response(jsonify({"msg": "Bad username or password"}), 401)
    if audience =="super-admin":
        nbf = datetime.utcnow() + timedelta(minutes=10)
        exp = datetime.utcnow() + timedelta(minutes=15)
    elif audience =="admin":
        nbf = datetime.utcnow() + timedelta(minutes=5)
        exp = datetime.utcnow() + timedelta(minutes=10)
    elif audience =="user":
        nbf = datetime.utcnow()
        exp = datetime.utcnow() + timedelta(minutes=5)
    else:
        return make_response(jsonify({"msg": "Invalid audience"}), 400)
    
    additional_claims = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": exp,
        "nbf": nbf,
        "iss": "your-issuer",
        "aud": audience
    }
    access_token = create_access_token(identity=username , additional_claims=additional_claims)
    return jsonify(access_token=access_token)

@app.route("/users", methods=["GET", "POST"])
@jwt_required()
def users():
    if request.method == "GET":
        users = get_all_users()
        return jsonify(users), 200

    if request.method == "POST":
        new_username = request.form["username"]
        new_email = request.form["email"]
        new_password = request.form["password"]
        add_user(new_username, new_email, new_password)
        return f"User {new_username} created successfully", 201

# Add a user (run this once to add a user)
from user import add_user
add_user("Alice", "alice@example.com", "password123")

#register a user
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    add_user(username, email, password)
    return jsonify({"msg": "User created successfully"}), 201

@app.route("/books", methods=["GET", "POST"])
@jwt_required()
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == "POST":
        new_author = request.form["author"]
        new_lang = request.form["language"]
        new_title = request.form["title"]
        sql = """INSERT INTO book (author, language, title)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201

@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE book
                SET title=?,
                    author=?,
                    language=?
                WHERE id=? """
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]
        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title,
        }
        conn.execute(sql, (title, author, language, id))
        conn.commit()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return f"Book with the id: {id} deleted successfully", 200
"""
@app.route('/check_token', methods=['GET'])
@jwt_required()
def check_token():
    current_user = get_jwt_identity()
    jwt_data = get_jwt()
    iat= datetime.fromtimestamp(jwt_data['iat'])
    if datetime.utcnow() < iat + timedelta(minutes=1):
        return jsonify({"msg":"Token not valid yet"}), 401
    return jsonify(logged_in_as=current_user), 200

"""
@app.route('/check_token', methods=['GET'])
@jwt_required()
def check_token():
    current_user = get_jwt_identity()
    jwt_data = get_jwt()
    iat = datetime.fromtimestamp(jwt_data['iat'])
    exp = datetime.fromtimestamp(jwt_data['exp'])
    nbf = datetime.fromtimestamp(jwt_data['nbf'])
    iss = jwt_data['iss']
    aud = jwt_data['aud']
    now = datetime.utcnow()
    """if now < iat + timedelta(minutes=1):
        return jsonify({"msg": "Token not valid yet"}), 401
    elif now < iat + timedelta(minutes=2):
        return jsonify({"msg": "Token is valid but will expire soon"}), 200
    elif now > exp:
        return jsonify({"msg": "Token has expired"}), 401
    else:
        return jsonify(logged_in_as=current_user), 200

    if now < nbf:
        return jsonify({"msg": "Token not valid yet"}), 401
    if now > exp:
        return jsonify({"msg": "Token has expired"}), 401
    return jsonify(logged_in_as=current_user, iat=iat, exp=exp, nbf=nbf, iss=iss, aud=aud), 200
"""
    if now > exp:
        return jsonify({"msg": exp}), 401
    return jsonify(logged_in_as=current_user, iat=iat, exp=exp, nbf=nbf, iss=iss, aud=aud), 200
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200
    
if __name__ == '__main__':
    app.run(debug=True)