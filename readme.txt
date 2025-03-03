# Health & Nutrition Analyzer API

A REST API that analyzes food images and medical reports using Google's Gemini AI.

## Features

- Analyze food images to get nutritional information
- Extract structured data from medical reports
- Consistent JSON response format
- Built with FastAPI for high performance

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
4. Add your Google Gemini API key to the `.env` file
5. Run the application:
```bash
python app.py
```

## Project Structure

```
health_nutrition_api/
├── app.py                 # Main application entry point
├── api/                   # API-related code
│   ├── __init__.py
│   ├── endpoints.py       # API route definitions
│   ├── models.py          # Pydantic models
│   └── config.py          # API configuration
├── services/              # Business logic
│   ├── __init__.py
│   ├── gemini_service.py  # Gemini AI integration
│   └── image_service.py   # Image processing
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── json_utils.py      # JSON handling
│   └── constants.py       # Prompts and constants
└── .env                   # Environment variables
```

## API Endpoints

### `GET /`
Returns basic API information.

### `POST /api/analyze`
Analyzes an image for food or medical information.

**Request Parameters:**
- `file`: Image file (JPEG or PNG)
- `category`: Analysis type (`food` or `medical`)

**Response Format:**
```json
{
  "status": true,
  "message": "Successfully analyzed data",
  "data": [...]
}
```

## Debugging

Set `DEBUG_MODE=true` in your `.env` file to get additional debugging information in error responses.

## License

MIT
