from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flaskapp"
    )
cursor = db.cursor()

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    try:
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Error as e:
        print("Error fetching users:", e)
        return jsonify({"error": "Failed to fetch users"}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Error as e:
        print("Error fetching user:", e)
        return jsonify({"error": "Failed to fetch user"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        db.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Error as e:
        print("Error creating user:", e)
        return jsonify({"error": "Failed to create user"}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    new_username = data.get('username')
    new_email = data.get('email')
    try:
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (new_username, new_email, id))
        db.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Error as e:
        print("Error updating user:", e)
        return jsonify({"error": "Failed to update user"}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        db.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        print("Error deleting user:", e)
        return jsonify({"error": "Failed to delete user"}), 500

if __name__ == '__main__':
    app.run(debug=True)
