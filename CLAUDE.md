# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CopyChatAgent is a full-stack AI chat application that provides a web interface for interacting with BigModel's GLM-4.5 API (智谱清言GLM-4.5). The application features intelligent content formatting detection, supports multiple output formats (Markdown, HTML, plain text), and includes file-based content management capabilities. Built with Vue.js frontend and Flask backend, it demonstrates a modern AI-powered chat application with comprehensive logging and modular architecture.

## Architecture

### Frontend (Vue.js)
- **Framework**: Vue 3 with Options API
- **Build Tool**: Vite 4.4.5 with hot reload
- **Key Dependencies**:
  - `marked` 5.1.0 for Markdown rendering
  - `axios` 1.4.0 for API calls
  - `highlight.js` 11.8.0 for code syntax highlighting
  - `vue-router` 4 for client-side routing
- **Development Server**: Runs on port 3000 with API proxy to backend
- **Package Manager**: Yarn (using yarn.lock for dependency pinning)

### Backend (Flask)
- **Framework**: Flask 2.3.3 with CORS support
- **AI Integration**: BigModel GLM-4.5 API with ZhipuAI SDK (`zai-sdk`)
- **Key Components**:
  - `app.py` - Main Flask application with `/api/generate` endpoint
  - `ai_service.py` - GLM-4.5 API integration with intelligent format detection
  - `file_based_markdown_converter.py` - File-based content conversion system
  - `html_manager.py` - HTML content management utilities
  - `markdown_converter.py` - Markdown processing utilities
  - `logger.py` - Comprehensive logging system
- **Development Server**: Runs on port 5000
- **Environment**: Configured via `python-dotenv`

### Data Flow
1. User input in Vue.js frontend → POST to `/api/generate`
2. Flask routes request to `AIService.generate_content()` with optional prompt type
3. BigModel API call with system prompt + user input (using configurable base URL)
4. Response format detection (Markdown/HTML/text)
5. Content cleaning and formatting
6. JSON response with `format` and `content` fields
7. Frontend dynamically renders based on format type

## Development Commands

### Frontend Development
```bash
cd frontend
yarn install          # Install dependencies (uses yarn.lock)
yarn dev              # Start development server (port 3000)
yarn build            # Build for production
yarn preview          # Preview production build
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt  # Install Python dependencies
cp .env.example .env              # Create environment file
# Edit .env to add GLM_API_KEY
python app.py                     # Start Flask server (port 5000)
```

### Testing and Utilities
```bash
# Run various test scripts
python test_markdown_conversion.py      # Test markdown conversion
python test_file_based_conversion.py     # Test file-based conversion
python test_fixed_markdown_saving.py     # Test markdown saving
python test_logging.py                   # Test logging functionality

# Translate markdown files using AI service
python translate_markdown.py <input.md> <output.md>
```

## Configuration

### Required Environment Variables (Backend)
- `GLM_API_KEY`: Your BigModel GLM API key (required)
- `AI_BASE_URL`: GLM API base URL (default: `https://open.bigmodel.cn/api/paas/v4`)
- `FLASK_ENV`: Set to 'development' for debug mode
- `FLASK_DEBUG`: Enable/disable Flask debug mode

### API Configuration
- Frontend Vite server proxies `/api` requests to `http://localhost:5000`
- Backend CORS configured for cross-origin requests
- Health check endpoint available at `/health`
- Model used: `glm-4-0520` (GLM-4.5 variant)

## Key Implementation Details

### Prompt System
- **Dynamic Prompt Loading**: `ai_service.py` loads prompts from `prompts/` directory
- **Prompt Types**: Supports different prompt templates for various use cases
- **Default System Prompt**: Comprehensive Chinese-language prompt for content generation

### Format Detection Algorithm
The AI service intelligently detects response format:
- **Markdown**: Contains headers (`#`), code blocks (```), or explicit "format: markdown"
- **HTML**: Contains HTML tags and explicit "format: html"
- **Text**: Default fallback for plain text responses

### Content Management
- **File-based Conversion**: `FileBasedMarkdownConverter` handles file operations
- **HTML Management**: `HTMLManager` provides HTML content utilities
- **Logging**: Comprehensive logging system with separate loggers for API and AI service

### Error Handling
- Frontend: Displays user-friendly error messages with loading states
- Backend: Comprehensive exception handling with proper HTTP status codes
- API: Structured error responses in JSON format
- Logging: Detailed request/response logging with timing information

## File Structure

```
/
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Main Vue component with dynamic rendering
│   │   └── main.js          # Vue app entry point
│   ├── index.html           # HTML template with embedded CSS
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration with API proxy
│   ├── yarn.lock            # Dependency lock file
│   ├── node_modules/        # Node.js dependencies
│   └── dist/                # Production build output
├── backend/
│   ├── app.py               # Flask main application
│   ├── ai_service.py        # GLM-4.5 API integration with configurable base URL
│   ├── file_based_markdown_converter.py  # File-based content conversion
│   ├── html_manager.py      # HTML content management
│   ├── markdown_converter.py # Markdown processing utilities
│   ├── logger.py           # Comprehensive logging system
│   ├── translate_markdown.py # Utility for translating markdown files
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (actual)
│   ├── .env.example         # Environment configuration template
│   ├── logs/                # Application logs directory
│   └── __pycache__/         # Python bytecode cache
├── prompts/
│   ├── init_prj_prompt.md   # Initial project specification prompt
│   ├── learn_word.md        # Word learning template
│   └── concept_svg.md       # SVG concept generation template
├── Data/                   # Data storage directory
├── .claude/
│   ├── commands.json        # Claude command configuration
│   ├── settings.local.json  # Local settings
│   └── prompts/             # Claude prompt templates
├── README.md                # Basic project documentation (Chinese)
├── API_FORMATS.md           # Detailed API format examples
├── CLAUDE.md                # This file
└── Various test files        # Python test scripts
```

## API Reference

### POST /api/generate
**Request**: `{ "input": "user text", "prompt_type": "optional_prompt_type" }`
**Response**: `{ "format": "markdown|html|text", "content": "generated content" }`
**Error**: `{ "error": "error message" }`

### GET /health
**Response**: `{ "status": "healthy" }`

## Development Notes

- The application uses Chinese language in the UI and system prompts
- Vite development server automatically proxies API requests to avoid CORS issues
- The AI service includes a comprehensive system prompt for content generation
- Frontend handles loading states and error conditions gracefully
- Both frontend and backend can be run independently for development
- AI base URL is configurable via `AI_BASE_URL` environment variable (defaults to BigModel's GLM API)
- Uses `glm-4-0520` model variant with temperature 0.7 and max_tokens 1000
- The `translate_markdown.py` utility can translate markdown files using the AI service
- Project includes prompt templates for project initialization, word learning, and SVG concept generation
- Comprehensive logging system tracks all API requests and AI service interactions

## Troubleshooting

### Common Issues
1. **API Key**: Ensure `GLM_API_KEY` is properly set in `backend/.env`
2. **Port Conflicts**: Frontend uses port 3000, backend uses port 5000
3. **CORS**: Already configured via Flask-CORS and Vite proxy
4. **Dependencies**: Use `yarn install` for frontend, `pip install -r requirements.txt` for backend
5. **Chinese Content**: The system and UI are designed for Chinese language content
6. **Logging**: Check `backend/logs/` directory for detailed logs

### Model Configuration
- Default model: `glm-4-0520`
- Temperature: 0.7 (balanced creativity/accuracy)
- Max tokens: 1000 (sufficient for most responses)
- Base URL: Configurable via `AI_BASE_URL` environment variable

### File Management
- The `FileBasedMarkdownConverter` handles file operations for markdown conversion
- HTML content is managed through the `HTMLManager` class
- All logging is centralized through the `logger.py` module