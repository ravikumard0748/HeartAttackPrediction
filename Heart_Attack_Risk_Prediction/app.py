from flask import Flask, render_template, request, session, jsonify
import joblib
import numpy as np
import pandas as pd
from twilio.rest import Client
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio API credentials from environment variables
SID = os.getenv('TWILIO_SID', '')
token = os.getenv('TWILIO_TOKEN', '')
twilio_from = os.getenv('TWILIO_FROM_NUMBER', '+19898122470')
twilio_to = os.getenv('TWILIO_TO_NUMBER', '+918668129523')

# Initialize Twilio client only if credentials are provided
ct = None
if SID and token:
    ct = Client(SID, token)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configure for production
if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

# Load ML Model
model = joblib.load("finalfinalmodel.joblib")

# Initialize records storage
RECORDS_FILE = 'heart_risk_records.json'

def load_records():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_record(record):
    records = load_records()
    records.append(record)
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("predict.html")

@app.route("/dashboard")
def dashboard():
    records = load_records()
    if not records:
        return render_template("dashboard.html", 
                             recent_records=[],
                             highest_risk=0,
                             lowest_risk=0,
                             average_risk=0,
                             highest_risk_date="N/A",
                             lowest_risk_date="N/A",
                             dates=[],
                             risk_values=[])
    
    # Sort records by date
    records.sort(key=lambda x: x['date'])
    
    # Calculate statistics
    risk_values = [r['risk_percentage'] for r in records]
    highest_risk = max(risk_values)
    lowest_risk = min(risk_values)
    average_risk = round(sum(risk_values) / len(risk_values), 1)
    
    # Get dates for highest and lowest risk
    highest_risk_record = max(records, key=lambda x: x['risk_percentage'])
    lowest_risk_record = min(records, key=lambda x: x['risk_percentage'])
    
    # Prepare data for the chart
    dates = [r['date'] for r in records]
    
    # Get recent records (last 5)
    recent_records = records[-5:][::-1]  # Reverse to show newest first
    
    return render_template("dashboard.html",
                         recent_records=recent_records,
                         highest_risk=highest_risk,
                         lowest_risk=lowest_risk,
                         average_risk=average_risk,
                         highest_risk_date=highest_risk_record['date'],
                         lowest_risk_date=lowest_risk_record['date'],
                         dates=dates,
                         risk_values=risk_values)

@app.route("/sub", methods=["POST"])
def result():
    if request.method == "POST":
        cols = ['Age', 'Gender', 'Heart rate', 'Systolic blood pressure',
                'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin']
        
        try:
            # Extract form values
            age = request.form['Age']
            gender = request.form['Gender']
            heart_rate = float(request.form['Heart_Rate'])
            systolic = float(request.form['Systolic_blood_pressure'])
            diastolic = float(request.form['Diastolic_blood_pressure'])
            blood_sugar = float(request.form['Blood_sugar'])
            ckmb = float(request.form['CK-MB'])
            troponin = float(request.form['Troponin'])
            
            # Convert gender to numerical value
            gender_num = 1 if gender == 'Male' else 0

            # Prepare input data
            input_data = np.array([age, gender_num, heart_rate, systolic, diastolic, blood_sugar, ckmb, troponin]).reshape(1, -1)
            final_input = pd.DataFrame(input_data, columns=cols)

            # Make prediction
            result = model.predict(final_input)
            prob = model.predict_proba(final_input)
            risk_percentage = round(prob[0][1] * 100, 1)

            # Determine risk class and key factors
            risk_class = 'high' if risk_percentage > 70 else 'medium' if risk_percentage > 30 else 'low'
            key_factors = []
            
            if systolic > 140 or diastolic > 90:
                key_factors.append("High blood pressure")
            if blood_sugar > 140:
                key_factors.append("Elevated blood sugar")
            if heart_rate > 100:
                key_factors.append("High heart rate")
            if ckmb > 25:
                key_factors.append("Elevated CK-MB")
            if troponin > 0.4:
                key_factors.append("High Troponin")
                
            key_factors = ", ".join(key_factors) if key_factors else "No significant risk factors"

            # Generate recommendations
            recommendations = []
            if "High blood pressure" in key_factors:
                recommendations.append("Monitor blood pressure regularly")
            if "Elevated blood sugar" in key_factors:
                recommendations.append("Control blood sugar levels")
            if "High heart rate" in key_factors:
                recommendations.append("Regular cardiovascular check-ups")
            if any(factor in key_factors for factor in ["Elevated CK-MB", "High Troponin"]):
                recommendations.append("Immediate medical attention recommended")
                
            recommendations = "; ".join(recommendations) if recommendations else "Maintain healthy lifestyle"

            # Save the record
            record = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'risk_percentage': risk_percentage,
                'risk_class': risk_class,
                'key_factors': key_factors,
                'recommendations': recommendations,
                'age': age,
                'gender': gender,
                'heart_rate': heart_rate,
                'systolic': systolic,
                'diastolic': diastolic,
                'blood_sugar': blood_sugar,
                'ckmb': ckmb,
                'troponin': troponin
            }
            save_record(record)

            # Check if high risk for SMS alert
            if result[0] == 1 and ct:
                try:
                    ct.messages.create(
                        body="Your friend / Relative have High risk of being Attack by the Heart Attack Please contact Him",
                        from_=twilio_from,
                        to=twilio_to
                    )
                except Exception as e:
                    print(f"Failed to send SMS: {str(e)}")

        except Exception as e:
            return render_template("result.html", res=f"Error: {str(e)}")

        return render_template("result.html", 
                           ress=risk_percentage,
                           age=age, 
                           gender=gender, 
                           heart_rate=heart_rate, 
                           systolic_bp=systolic, 
                           diastolic_bp=diastolic, 
                           blood_sugar=blood_sugar, 
                           ck_mb=ckmb, 
                           troponin=troponin)

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check if model can be loaded
        model_path = "finalfinalmodel.joblib"
        if os.path.exists(model_path):
            return {"status": "healthy", "model": "loaded"}, 200
        else:
            return {"status": "unhealthy", "error": "model not found"}, 500
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
