from flask import jsonify, Flask, request

app = Flask("__name__")

@app.route("/get-user/<user_id>")
def user(user_id):
    data = {
        'user-id': user_id,
        'name': 'john',
        'mail':"john.doe@gmail.com"
    }
    return jsonify(data), 200

    
@app.route("/create", methods = ["POST"])
def create():
    data = request.get_json()
    return jsonify(data), 201




if __name__ == "__main__":
    app.run(debug=True)