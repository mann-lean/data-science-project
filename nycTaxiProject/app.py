import logging
import os
from flask import Flask, request, render_template
from flask_cors import CORS
from nycTaxiProject.pipeline.stage_06_prediction import PredictionPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def parse_input(form):
    return {
        'vendorid': [int(form.get('vendorid'))],
        'ratecodeid': [float(form.get('ratecodeid'))],
        'pulocationid': [int(form.get('pulocationid'))],
        'dolocationid': [int(form.get('dolocationid'))],
        'passenger_count': [int(form.get('passenger_count'))],
        'extra': [float(form.get('extra'))],
        'tolls_amount': [float(form.get('tolls_amount'))],
        'congestion_surcharge': [float(form.get('congestion_surcharge'))],
        'improvement_surcharge': [float(form.get('improvement_surcharge'))],
        'mta_tax': [float(form.get('mta_tax'))],
        'airport_fee': [float(form.get('airport_fee'))],
        'trip_distance': [float(form.get('trip_distance'))],
        'fare_amount': [float(form.get('fare_amount'))],
        'pickupDateTime': [form.get('pickupDateTime')],
        'dropoffDateTime': [form.get('dropoffDateTime')]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    try:
        input_dict = parse_input(request.form)
        pipeline = PredictionPipeline()
        prediction = pipeline.predict(input_dict)
        final_result = round(float(prediction[0]), 2)
        return render_template('index.html', results=f"Predicted Tip Amount: ${final_result}")
    
    except Exception as e:
        logger.exception(f"Prediction error: {e}")
        return render_template('index.html', results="Error occurred. Please check your input!")

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)