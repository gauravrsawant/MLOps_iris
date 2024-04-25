import joblib
from flask import Flask, request, jsonify, render_template
import logging
import os

# Create a Flask app
app = Flask(__name__)

# Load the model
model = joblib.load('iris_model.joblib')

# Set up logging to record predictions
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/flask_app.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s'
)

# Route for the home page that displays the form
@app.route('/')
def index():
    return render_template('index.html')

# Route for form submission
@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])
    
    # Make a prediction
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

    # Log the prediction
    logging.info(f"Input: [{sepal_length}, {sepal_width}, {petal_length}, {petal_width}], Prediction: {prediction.tolist()}")

    # Return the result to the user
    return render_template('result.html', prediction=prediction[0])

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
