from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("iris_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=["POST"])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        prediction = model.predict([features])[0]
        species = ['Setosa', 'Versicolor', 'Virginica'][prediction]
        return render_template('index.html', prediction_text=f'Predicted Iris Species: {species}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {e}')

@app.route('/api', methods=["POST"])
def api():
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)[0]
    species = ['Setosa', 'Versicolor', 'Virginica'][prediction]
    return jsonify({'species': species})

if __name__ == '__main__':
    app.run(debug=True)
