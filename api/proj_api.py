from flask import jsonify, Flask, make_response, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask("__name__")

app.config['SECRET_KEY'] = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
# creates SQLALCHEMY object
db = SQLAlchemy(app)

jwt = JWTManager(app)

#user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    groceries = db.Column(db.Integer, default = 0)
    leisure = db.Column(db.Integer, default = 0)
    electronics = db.Column(db.Integer,default = 0)
    utilities = db.Column(db.Integer,default = 0)
    clothing = db.Column(db.Integer,default = 0)
    health = db.Column(db.Integer,default = 0)
    others = db.Column(db.Integer,default = 0)
    total = db.Column(db.Integer,default = 0)

@app.route("/sign-in", methods = ["POST"])
def login():
    data = request.get_json()
    user_name = data['Username']
    passwrd = data["Password"]

    user = User.query.filter_by(username = user_name).first()
    if user:
        pass
    else:
        return make_response("The account with this username dosen't exist or the password is wrong", 201)

    


@app.route("/sign-up", methods = ["POST"])
def signup():
    data = request.get_json()
    user_name = data['Username']
    passwrd = data["Password"]

    users = User.query.filter_by(username = user_name).first()

    if not users:
        users = User(
            id = str(uuid.uuid4()),
            username = user_name,
            password = passwrd )
        db.session.add(users)
        db.session.commit()
    else:
        return make_response("user already exists", 202)



@app.route("/expenses", methods = ["GET"])
@jwt_required()
def show_expeses():
    pass
    #return data from db

@app.route("/add", methods = ["POST"])
@jwt_required()
def add_exp():
    pass


@app.route("/delete", methods = ["POST"])
@jwt_required()
def del_exp():
    pass


@app.route("/update/<expense>", methods = ["POST"])
@jwt_required()
def upt_exp(expense):
    pass


if __name__ == "__main__":
    app.run(debug=True)