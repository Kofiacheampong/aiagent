
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from utils import load_nutrition_data, process_user_input

app = Flask(__name__)

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/track-meal', methods=['POST'])
def track_meal():
    data = request.json
    if not data or 'food' not in data:
        return jsonify({"error": "Food data is required"}), 400
    
    nutrition_data = load_nutrition_data(data['food'])
    if not nutrition_data:
        return jsonify({"error": "Could not fetch nutrition data"}), 400
        
    # Extract basic nutrition info
    if 'hints' in nutrition_data and nutrition_data['hints']:
        food_data = nutrition_data['hints'][0]['food']
        return jsonify({
            "message": "Meal tracked successfully",
            "nutrients": {
                "calories": food_data.get('nutrients', {}).get('ENERC_KCAL', 0),
                "protein": food_data.get('nutrients', {}).get('PROCNT', 0),
                "fat": food_data.get('nutrients', {}).get('FAT', 0),
                "carbs": food_data.get('nutrients', {}).get('CHOCDF', 0)
            }
        })
    return jsonify({"error": "No nutrition data found"}), 404

@app.route('/create-workout', methods=['POST'])
def create_workout():
    data = request.json
    # TODO: Implement workout creation logic
    return jsonify({"message": "Workout created successfully"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    result = process_user_input(data['message'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
