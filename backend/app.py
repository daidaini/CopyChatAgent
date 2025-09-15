import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ai_service import AIService
from logger import api_logger
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

api_logger.info("Starting Flask application")
ai_service = AIService()

@app.route('/api/generate', methods=['POST'])
def generate_content():
    start_time = time.time()
    client_ip = request.remote_addr
    api_logger.info(f"Received POST /api/generate request from {client_ip}")

    try:
        data = request.get_json()

        if not data or 'input' not in data:
            api_logger.warning(f"Missing required field 'input' in request from {client_ip}")
            return jsonify({
                'error': 'Missing required field: input'
            }), 400

        user_input = data['input'].strip()
        prompt_type = data.get('prompt_type', None)

        api_logger.info(f"Processing request - prompt_type: {prompt_type}, input_length: {len(user_input)}")

        if not user_input:
            api_logger.warning(f"Empty input received from {client_ip}")
            return jsonify({
                'error': 'Input cannot be empty'
            }), 400

        result = ai_service.generate_content(user_input, prompt_type)

        processing_time = time.time() - start_time
        api_logger.info(f"Request completed successfully - processing_time: {processing_time:.2f}s, format: {result.get('format', 'unknown')}")

        return jsonify(result)

    except Exception as e:
        processing_time = time.time() - start_time
        api_logger.error(f"Error processing request from {client_ip}: {e} - processing_time: {processing_time:.2f}s")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """Get available prompt types"""
    client_ip = request.remote_addr
    api_logger.info(f"Received GET /api/prompts request from {client_ip}")

    try:
        prompts = ai_service.get_available_prompts()
        api_logger.info(f"Returning {len(prompts)} available prompts to {client_ip}")
        return jsonify({
            'prompts': prompts,
            'default': None
        })
    except Exception as e:
        api_logger.error(f"Error getting prompts for {client_ip}: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    client_ip = request.remote_addr
    api_logger.debug(f"Health check requested from {client_ip}")
    return jsonify({'status': 'healthy'})

@app.route('/api/log', methods=['POST'])
def log_frontend_event():
    """Receive logging events from frontend"""
    try:
        data = request.get_json()
        if data:
            api_logger.info(f"Frontend log: {data.get('action', 'unknown')} - {data.get('details', {})}")
        return jsonify({'status': 'logged'})
    except Exception as e:
        api_logger.error(f"Error receiving frontend log: {e}")
        return jsonify({'status': 'error'}), 500

@app.before_request
def log_request_info():
    """Log request information"""
    api_logger.debug(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response_info(response):
    """Log response information"""
    api_logger.debug(f"Response {response.status_code} for {request.path}")
    return response

if __name__ == '__main__':
    api_logger.info("Flask application starting on port 5000")
    api_logger.info(f"Available endpoints: /api/generate, /api/prompts, /health")
    app.run(debug=False, host='0.0.0.0', port=5000)
