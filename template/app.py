from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('iris_model.pkl')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the form
    features = [float(x) for x in request.form.values()]
    prediction = model.predict([np.array(features)])

    return render_template('index.html', prediction_text=f'Predicted Iris class: {prediction[0]}')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
