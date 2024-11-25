from flask import jsonify, Flask, make_response, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
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
    category = db.Column(db.String(50))
    amount = db.Column(db.Integer, default = 0)

@app.route("/sign-in", methods = ["POST"])
def login():
    data = request.get_json()
    user_name = data['Username']
    passwrd = data["Password"]

    user = User.query.filter_by(username = user_name).first()
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
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
    current_user = get_jwt_identity()
    expenses = Expenses.query.filter_by(user_id=current_user).all()

    # Serialize expenses into JSON format
    expenses_list = [{"category": exp.category, "amount": exp.amount} for exp in expenses]
    return jsonify({"expenses": expenses_list}), 200


@app.route("/add/<cat>/<total>", methods = ["POST"])
@jwt_required()
def add_exp(cat, total):
    current_user = get_jwt_identity()
    expense = Expenses(
        id = str(uuid.uuid4()),
        user_id = current_user,
        category = cat,
        amount = total
    )
    db.session.add(expense)
    db.session.commit()


@app.route("/delete/<cat>/<total>", methods = ["POST"])
@jwt_required()
def del_exp(cat,total):
    current_user = get_jwt_identity()
    exp = Expenses.query.filter_by(user_id = current_user, category = cat, amount = total)
    if exp:
        db.session.remove(exp)
        db.session.commit()
    else:
        return make_response("This expense dosen't exist", 201)


@app.route("/update/<cat>/<total>/<new>", methods = ["POST"])
@jwt_required()
def upt_exp(cat,total,new):
    current_user = get_jwt_identity()
    exp = Expenses.query.filter_by(user_id = current_user, category = cat, amount = total)
    if exp:
        exp.amount = new
        db.session.commit()
    else:
        return make_response("This expense dosen't exist", 201)


if __name__ == "__main__":
    app.run(debug=True)