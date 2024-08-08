

from flask import Flask, request, url_for, redirect, render_template, jsonify
import pickle
import requests
import numpy as np
import pandas as pd
import openpyxl
app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def hello_world():
    return render_template("forest.html")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    

    float_features = [float(x) for x in request.form.values()]
    final = [np.array(float_features)]
    print(float_features)
    print(final)

    # Make a prediction using your machine learning model
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)

    if output > str(0.5):
        result = 'Your Forest is in Danger.\nProbability of fire occurring is {}'.format(output)
    else:
        result = 'Your Forest is safe.\n Probability of fire occurring is {}'.format(output)

    # Create or open an Excel file and add the prediction result
    excel_file = 'forest_predictions.xlsx'
    try:
        workbook = openpyxl.load_workbook(excel_file)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
    sheet = workbook.active



    sheet['A1'] = 'Temperature'
    sheet['B1'] = 'Oxygen'
    sheet['C1'] = 'Humidity'
    sheet['D1'] = 'Result'



    # Add a new row with the prediction result
    new_row = [str(x) for x in float_features] + [result]
    sheet.append(new_row)

    # Save the Excel file
    workbook.save(excel_file)

    return render_template('forest.html', pred=result, bhai="Result saved to Excel file")


@app.route('/update_location', methods=['POST'])
def update_location():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    api_key = '4da3ac8d9ecb02439ffb21a99def8f77'

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        temp = weather_data['main']['temp']
        oxygen = 21.0
        humidity = weather_data['main']['humidity']

        return jsonify({'message': 'Location updated successfully', 'longitude': longitude, 'latitude': latitude,
                        'temp': temp, 'oxygen': oxygen, 'humidity': humidity})

if __name__ == '__main__':
    app.run(debug=True)