# House_Price_Prediction
This project is a Machine Learning web application that predicts house prices based on user inputs such as location, square footage, number of bedrooms (BHK), anIt combines a trained ML regression model with a Flask web application that includes user authentication, enquiry form, and prediction interface.

🔹 Features

User Authentication: Signup, login, and logout functionality with hashed passwords (SQLite database).

House Price Prediction: Predicts prices using a pre-trained ML model (updated_house_price_model.pkl).

Location Handling: Encodes categorical location values, gracefully managing unseen locations.

Flask Web App: Clean UI with routes for home, prediction, and enquiries.

Database Integration: SQLite database (users.db) for storing user accounts securely.

🔹 Tech Stack

Frontend: HTML (Flask templates: home.html, login.html, signup.html, predict.html)

Backend: Flask (Python)

Database: SQLite (users.db)

Machine Learning:

Trained model stored in updated_house_price_model.pkl

Location encoding using LabelEncoder (scikit-learn)

Security: Password hashing via werkzeug.security

🔹 File Overview

app.py → Main Flask application (auth, prediction, routes, model loading)

datbase.py → Initializes the SQLite users table

query.py → Helper script to query user details from DB

updated_house_price_model.pkl → Pre-trained ML model for prediction

users.db → SQLite database storing registered users

omer.py → Additional ML experimentation (drug discovery, not directly tied to house price app)d bathrooms.
