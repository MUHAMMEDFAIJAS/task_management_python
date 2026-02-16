import bcrypt
from flask import Flask, jsonify, request
from models import create_tables, create_user, get_user_by_username
from auth import generate_token, verify_token
from models import create_task, get_tasks_by_user,update_task,delete_task
app = Flask(__name__)

create_tables()

@app.route("/")
def home():
    return jsonify({"message": "Task Manager API Running"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return {"error": "Username and password required"}, 400

    success = create_user(data["username"], data["password"])

    if not success:
        return {"error": "Username already exists"}, 400

    return {"message": "User registered successfully"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return {"error": "Username and password required"}, 400

    user = get_user_by_username(data["username"])

    if not user:
        return {"error": "Invalid credentials"}, 401

    stored_password = user[2]

    if not bcrypt.checkpw(data["password"].encode("utf-8"), stored_password):
        return {"error": "Invalid credentials"}, 401

    token = generate_token(user[0])

    return {
        "message": "Login successful",
        "token": token
    }


@app.route("/profile", methods=["GET"])
def profile():
    user_id = verify_token()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    return {"message": f"Welcome user {user_id}"}

  


@app.route("/tasks", methods=["POST"])
def add_task():
    user_id = verify_token()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    if not data or "title" not in data:
        return {"error": "Title is required"}, 400

    create_task(data["title"], user_id)

    return {"message": "Task created successfully"}, 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = verify_token()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    tasks = get_tasks_by_user(user_id)

    return {"tasks": [{"id": t[0], "title": t[1], "completed": bool(t[3])} for t in tasks]}


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    user_id = verify_token()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    if not data or "title" not in data:
        return {"error": "Title required"}, 400

    affected = update_task(task_id, data["title"], user_id)

    if affected == 0:
        return {"error": "Task not found or not yours"}, 404

    return {"message": "Task updated"}



@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    user_id = verify_token()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    affected = delete_task(task_id, user_id)

    if affected == 0:
        return {"error": "Task not found or not yours"}, 404

    return {"message": "Task deleted"}

# if __name__ == "__main__":
#     app.run(debug=True)


if __name__ == "__main__":
    app.run()
