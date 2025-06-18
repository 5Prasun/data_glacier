# Iris Species Prediction Web App

This is a Flask-based web application that predicts the species of an Iris flower based on user input features. The app uses a pre-trained Random Forest machine learning model saved as `iris_model.pkl`. It provides both a web interface and a REST API endpoint.

---

## Features

- Predict Iris species via a web form.
- REST API for programmatic predictions.
- Deployable on Heroku or other cloud platforms.
- Simple and user-friendly interface.

---

## Project Structure

iris-flask-ml-app/
│
├── app.py # Flask application code
├── iris_model.pkl # Pre-trained ML model
├── requirements.txt # Python dependencies
├── Procfile # For Heroku deployment
└── templates/
└── index.html # HTML template for web form