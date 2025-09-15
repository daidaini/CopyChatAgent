import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ai_service import AIService

load_dotenv()

app = Flask(__name__)
CORS(app)

ai_service = AIService()

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()

        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input'
            }), 400

        user_input = data['input'].strip()
        prompt_type = data.get('prompt_type', None)

        if not user_input:
            return jsonify({
                'error': 'Input cannot be empty'
            }), 400

        result = ai_service.generate_content(user_input, prompt_type)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """Get available prompt types"""
    try:
        prompts = ai_service.get_available_prompts()
        return jsonify({
            'prompts': prompts,
            'default': None
        })
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
