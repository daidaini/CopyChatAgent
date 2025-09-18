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
        use_test_file = data.get('use_test_file', False)

        api_logger.info(f"Processing request - prompt_type: {prompt_type}, use_test_file: {use_test_file}, input_length: {len(user_input)}")

        result = ai_service.generate_content(user_input, prompt_type, use_test_file)

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

@app.route('/api/html/files', methods=['GET'])
def get_html_files():
    """Get list of all HTML files"""
    try:
        files = ai_service.get_all_html_files()
        api_logger.info(f"Returning {len(files)} HTML files")
        return jsonify({
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        api_logger.error(f"Error getting HTML files: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/html/files/<file_id>', methods=['GET'])
def get_html_file(file_id):
    """Get specific HTML file content"""
    try:
        result = ai_service.get_html_file(file_id)
        if result:
            api_logger.info(f"Serving HTML file: {file_id}")
            return jsonify(result)
        else:
            api_logger.warning(f"HTML file not found: {file_id}")
            return jsonify({
                'error': 'HTML file not found'
            }), 404
    except Exception as e:
        api_logger.error(f"Error getting HTML file {file_id}: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/html/files/<file_id>', methods=['DELETE'])
def delete_html_file(file_id):
    """Delete HTML file"""
    try:
        success = ai_service.delete_html_file(file_id)
        if success:
            api_logger.info(f"HTML file deleted: {file_id}")
            return jsonify({
                'status': 'deleted'
            })
        else:
            api_logger.warning(f"HTML file not found for deletion: {file_id}")
            return jsonify({
                'error': 'HTML file not found'
            }), 404
    except Exception as e:
        api_logger.error(f"Error deleting HTML file {file_id}: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/html/files/<file_id>/view', methods=['GET'])
def view_html_file(file_id):
    """View HTML file directly in browser"""
    try:
        result = ai_service.get_html_file(file_id)
        if result:
            api_logger.info(f"Direct view of HTML file: {file_id}")
            return result['content'], 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            api_logger.warning(f"HTML file not found for view: {file_id}")
            return "HTML file not found", 404
    except Exception as e:
        api_logger.error(f"Error viewing HTML file {file_id}: {e}")
        return f"Error loading HTML file: {str(e)}", 500

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
    api_logger.info(f"Available endpoints: /api/generate, /api/prompts, /health, /api/html/files/*")
    app.run(debug=False, host='0.0.0.0', port=5000)
