from flask import jsonify, Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask("__name__")
jwt = JWTManager(app)

@app.route("/sign-in", methods = ["POST"])
def login():
    data = request.get_json()
    


@app.route("/sign-up", methods = ["POST"])
def signup():
    data = request.get_json()



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