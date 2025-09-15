# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CopyChatAgent is a full-stack AI chat application that provides a web interface for interacting with BigModel's GLM-4.5 API (智谱清言GLM-4.5). The application features intelligent content formatting detection and supports Markdown, HTML, and plain text rendering. Built with Vue.js frontend and Flask backend, it demonstrates a modern AI-powered chat application with clean architecture.

## Architecture

### Frontend (Vue.js)
- **Framework**: Vue 3 with Options API
- **Build Tool**: Vite 4.4.5 with hot reload
- **Key Dependencies**: 
  - `marked` 5.1.0 for Markdown rendering
  - `axios` 1.4.0 for API calls
  - `highlight.js` 11.8.0 for code syntax highlighting
  - Built-in CSS for styling
- **Development Server**: Runs on port 3000 with API proxy to backend
- **Package Manager**: Yarn

### Backend (Flask)
- **Framework**: Flask 2.3.3 with CORS support
- **AI Integration**: BigModel GLM-4.5 API with ZhipuAI SDK 2.0.1
- **Key Components**:
  - `app.py` - Main Flask application with `/api/generate` endpoint
  - `ai_service.py` - GLM-4.5 API integration with intelligent format detection
- **Development Server**: Runs on port 5000
- **Environment**: Configured via `python-dotenv`

### Data Flow
1. User input in Vue.js frontend → POST to `/api/generate`
2. Flask routes request to `AIService.generate_content()`
3. BigModel API call with system prompt + user input (using `glm-4-0520` model)
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

### Utilities
```bash
python translate_markdown.py <input.md> <output.md>  # Translate markdown files
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

### Format Detection Algorithm
The AI service intelligently detects response format:
- **Markdown**: Contains headers (`#`), code blocks (```), or explicit "format: markdown"
- **HTML**: Contains HTML tags and explicit "format: html" 
- **Text**: Default fallback for plain text responses

### Content Cleaning
- Removes format declarations and metadata
- Preserves code blocks and structured content
- Handles mixed format responses gracefully

### Error Handling
- Frontend: Displays user-friendly error messages with loading states
- Backend: Comprehensive exception handling with proper HTTP status codes
- API: Structured error responses in JSON format

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
│   └── node_modules/        # Node.js dependencies
├── backend/
│   ├── app.py               # Flask main application
│   ├── ai_service.py        # GLM-4.5 API integration with configurable base URL
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (actual)
│   ├── .env.example         # Environment configuration template
│   ├── translate_markdown.py # Utility for translating markdown files
│   └── __pycache__/         # Python bytecode cache
├── prompts/
│   ├── init_prj_prompt.md   # Initial project specification prompt
│   └── learn_word.md        # Word learning template
├── .claude/
│   ├── commands.json        # Claude command configuration
│   ├── settings.local.json  # Local settings
│   └── prompts/             # Claude prompt templates
├── README.md                # Basic project documentation (Chinese)
├── API_FORMATS.md           # Detailed API format examples
├── image_links.txt          # External image references
├── CLAUDE.md                # This file
└── translate_markdown.py    # Root-level translation utility
```

## API Reference

### POST /api/generate
**Request**: `{ "input": "user text" }`
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
- Project includes prompt templates for project initialization and word learning

## Troubleshooting

### Common Issues
1. **API Key**: Ensure `GLM_API_KEY` is properly set in `backend/.env`
2. **Port Conflicts**: Frontend uses port 3000, backend uses port 5000
3. **CORS**: Already configured via Flask-CORS and Vite proxy
4. **Dependencies**: Use `yarn install` for frontend, `pip install -r requirements.txt` for backend
5. **Chinese Content**: The system and UI are designed for Chinese language content

### Model Configuration
- Default model: `glm-4-0520`
- Temperature: 0.7 (balanced creativity/accuracy)
- Max tokens: 1000 (sufficient for most responses)
- Base URL: Configurable via `AI_BASE_URL` environment variable