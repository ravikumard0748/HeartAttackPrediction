import json
import os
import sys
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def handler(event, context):
    try:
        # Handle CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        }
        
        # Handle preflight requests
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Parse request body
        body = json.loads(event['body'])
        
        # Load the model
        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'finalfinalmodel.joblib')
        model = joblib.load(model_path)
        
        # Extract form values
        age = body.get('Age')
        gender = body.get('Gender')
        heart_rate = float(body.get('Heart_Rate'))
        systolic = float(body.get('Systolic_blood_pressure'))
        diastolic = float(body.get('Diastolic_blood_pressure'))
        blood_sugar = float(body.get('Blood_sugar'))
        ckmb = float(body.get('CK-MB'))
        troponin = float(body.get('Troponin'))
        
        # Convert gender to numerical value
        gender_num = 1 if gender == 'Male' else 0
        
        # Prepare input data
        cols = ['Age', 'Gender', 'Heart rate', 'Systolic blood pressure',
                'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin']
        
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
        
        # Prepare response
        response_data = {
            'risk_percentage': risk_percentage,
            'risk_class': risk_class,
            'key_factors': key_factors,
            'recommendations': recommendations,
            'prediction': int(result[0]),
            'input_data': {
                'age': age,
                'gender': gender,
                'heart_rate': heart_rate,
                'systolic': systolic,
                'diastolic': diastolic,
                'blood_sugar': blood_sugar,
                'ckmb': ckmb,
                'troponin': troponin
            }
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
