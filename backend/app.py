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
        model_type = data.get('model_type', 'standard')  # 新增模型类型参数

        api_logger.info(f"Processing request - prompt_type: {prompt_type}, use_test_file: {use_test_file}, model_type: {model_type}, input_length: {len(user_input)}")

        result = ai_service.generate_content(user_input, prompt_type, use_test_file, model_type)

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

@app.route('/api/generate_quant_trade_strategy', methods=['POST'])
def generate_quant_trade_strategy():
    """Generate quantitative trading strategy using knowledge base"""
    start_time = time.time()
    client_ip = request.remote_addr
    api_logger.info(f"Received POST /api/generate_quant_trade_strategy request from {client_ip}")

    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            api_logger.warning(f"Missing required field 'prompt' in request from {client_ip}")
            return jsonify({
                'error': 'Missing required field: prompt'
            }), 400

        user_prompt = data['prompt'].strip()
        knowledge_base_name = data.get('knowledge_base_name', 'quant_trade_api_doc')
        model_type = data.get('model_type', 'standard')  # 新增模型类型参数

        if not user_prompt:
            api_logger.warning(f"Empty prompt in request from {client_ip}")
            return jsonify({
                'error': 'Prompt cannot be empty'
            }), 400

        api_logger.info(f"Processing quant trade strategy request - knowledge_base: {knowledge_base_name}, model_type: {model_type}, prompt_length: {len(user_prompt)}")

        result = ai_service.generate_quant_trade_strategy(user_prompt, knowledge_base_name, model_type)

        processing_time = time.time() - start_time
        api_logger.info(f"Quant trade strategy request completed successfully - processing_time: {processing_time:.2f}s, format: {result.get('format', 'unknown')}")

        return jsonify(result)

    except Exception as e:
        processing_time = time.time() - start_time
        api_logger.error(f"Error processing quant trade strategy request from {client_ip}: {e} - processing_time: {processing_time:.2f}s")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/generate_quant_trade_strategy/knowledge_bases', methods=['GET'])
def get_knowledge_bases():
    """Get available knowledge bases for quantitative trading"""
    client_ip = request.remote_addr
    api_logger.info(f"Received GET /api/generate_quant_trade_strategy/knowledge_bases request from {client_ip}")

    try:
        knowledge_bases = ai_service.knowledge_base_service.get_knowledge_base_list()
        api_logger.info(f"Returning {len(knowledge_bases)} knowledge bases to {client_ip}")
        return jsonify({
            'knowledge_bases': knowledge_bases
        })
    except Exception as e:
        api_logger.error(f"Error getting knowledge bases for {client_ip}: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get available model configurations"""
    client_ip = request.remote_addr
    api_logger.info(f"Received GET /api/models request from {client_ip}")

    try:
        models = ai_service.get_available_models()
        api_logger.info(f"Returning available models to {client_ip}: {models}")
        return jsonify({
            'models': models,
            'current_config': {
                'standard_model': models['standard'],
                'lightweight_model': models['lightweight']
            }
        })
    except Exception as e:
        api_logger.error(f"Error getting available models for {client_ip}: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/models/select', methods=['POST'])
def select_model():
    """Select model for a specific input"""
    start_time = time.time()
    client_ip = request.remote_addr
    api_logger.info(f"Received POST /api/models/select request from {client_ip}")

    try:
        data = request.get_json()

        if not data or 'input' not in data:
            api_logger.warning(f"Missing required field 'input' in model selection request from {client_ip}")
            return jsonify({
                'error': 'Missing required field: input'
            }), 400

        user_input = data['input'].strip()
        model_type = data.get('model_type', 'auto')
        prompt_type = data.get('prompt_type', None)

        if not user_input:
            api_logger.warning(f"Empty input in model selection request from {client_ip}")
            return jsonify({
                'error': 'Input cannot be empty'
            }), 400

        # 获取系统提示词
        if prompt_type and prompt_type in ai_service.get_available_prompts():
            system_prompt = ai_service.prompt_service.get_prompt_content(prompt_type)
        else:
            system_prompt = ai_service.prompt_service.get_default_prompt()

        # 选择模型
        selected_model = ai_service.model_service.select_model(user_input, system_prompt, model_type)

        processing_time = time.time() - start_time
        api_logger.info(f"Model selection completed successfully - selected_model: {selected_model}, processing_time: {processing_time:.2f}s")

        return jsonify({
            'selected_model': selected_model,
            'model_type': model_type,
            'input_length': len(user_input),
            'reasoning': f"Model selected based on input analysis and model_type: {model_type}"
        })

    except Exception as e:
        processing_time = time.time() - start_time
        api_logger.error(f"Error in model selection request from {client_ip}: {e} - processing_time: {processing_time:.2f}s")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

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
    api_logger.info(f"Available endpoints: /api/generate, /api/prompts, /health, /api/html/files/*, /api/generate_quant_trade_strategy, /api/models, /api/models/select")
    app.run(debug=False, host='0.0.0.0', port=5000)
