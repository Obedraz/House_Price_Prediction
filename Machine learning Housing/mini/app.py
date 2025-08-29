from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import sqlite3
from sklearn.preprocessing import LabelEncoder
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "2802190e7e2c0c69d4efa1fb013c4e7488b50888c7fb1efed666cf5308e31224"  # Replace with a secure key

# Database file
DB_FILE = "users.db"

# Initialize the database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()

# Initialize the database
init_db()

# Load the trained model
model_file_path = 'updated_house_price_model.pkl'  # Path to your trained model
try:
    with open(model_file_path, 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")
    model = None

# Load the LabelEncoder used for encoding locations
le_location = LabelEncoder()

# List of locations used during training
trained_locations = [
    'Electronic City Phase II',
    'Chikka Tirupathi',
    'Uttarahalli',
    'Sadahalli',
    'Sathya Layout',
    '5 Bedroom Farm House in Lakshmipura',
    'Shanti Nagar',
    '2nd Stage Arekere Mico Layout',
    'Jayamahal',
    'Veer Sandra',
    'Chennappa Layout',
    'RMV Extension Stage 2',
]  # Example

# Fit the LabelEncoder with the trained locations
le_location.fit(trained_locations)

# Function to handle unseen locations
def handle_unseen_location(location):
    try:
        return le_location.transform([location])[0]
    except ValueError:
        # Default to the first known location if an unseen one is encountered
        print(f"Warning: '{location}' is unseen. Defaulting to '{trained_locations[0]}'.")
        return le_location.transform([trained_locations[0]])[0]

# Routes for login/signup functionality
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username or email already exists
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username or email already exists.", "error")
            else:
                hashed_password = generate_password_hash(password)
                try:
                    cursor.execute(''' 
                        INSERT INTO users (username, email, password) 
                        VALUES (?, ?, ?)
                    ''', (username, email, hashed_password))
                    conn.commit()
                    flash("Signup successful! Please log in.", "success")
                    return redirect(url_for('login'))
                except sqlite3.IntegrityError:
                    flash("Error occurred while signing up. Please try again.", "error")

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash("Login successful!", "success")
                return redirect(url_for('home'))  # Redirect to home after successful login
            else:
                flash("Invalid username or password.", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'user_id' not in session:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('home.html', username=session.get('username'))

@app.route('/getstarted')
def getstarted():
    if 'user_id' not in session:  # Ensure the user is logged in before accessing the prediction page
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('predict.html')  # Redirect to the prediction page

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        flash(f"Thank you for your enquiry, {name}! We'll get back to you soon.", "success")
    return render_template('enquiry.html', username=session.get('username'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        # Get form data
        location = request.form['location']
        total_sqft = float(request.form['total_sqft'])
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Handle unseen locations gracefully
        encoded_location = handle_unseen_location(location)
        input_data = np.array([[encoded_location, total_sqft, bhk, bath]])

        # Debug: Log input data
        print(f"Input Data: {input_data}")

        # Make prediction
        if model:
            prediction = model.predict(input_data)
            print(f"Prediction: {prediction}")
            return render_template('predict.html', prediction_text=f'Predicted House Price: ₹{prediction[0]:,.2f}')
        else:
            flash("Error: Model not loaded correctly.", "error")
            return render_template('predict.html', prediction_text="Error: Model not loaded correctly.")
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        flash(f"Error occurred during prediction: {e}", "error")
        return render_template('predict.html', prediction_text=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
