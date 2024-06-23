from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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
@app.route('/')
def index():
    # Fetch all users from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    # Insert new user into database
    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
    db.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        # Update user in the database
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (new_username, new_email, id))
        db.commit()
        return redirect(url_for('index'))
    else:
        # Fetch user details from the database
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        return render_template('update.html', user=user)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    # Delete user from database based on ID
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
