# Persona AI - Memory Extraction & Personality Engine

A full-stack application that extracts user memory (preferences, emotional patterns, facts) from chat messages and transforms AI responses using different personality styles.

## Features

- **Memory Extraction Module**: Identifies user preferences, emotional patterns, and facts worth remembering from chat conversations
- **Personality Engine**: Transforms AI responses with different personalities:
  - Calm Mentor: Patient, wise, and supportive
  - Witty Friend: Fun, humorous, and engaging
  - Therapist: Professional, empathetic listener
- **Before/After Comparison**: Shows default vs. personality-transformed responses side-by-side
- **Structured Output Parsing**: Extracts structured JSON data from LLM responses
- **Modular Architecture**: Separate frontend and backend with clean separation of concerns

## Tech Stack

- **Frontend**: React.js
- **Backend**: Python FastAPI
- **LLM**: Mistral AI Devstral 2 123B (via NVIDIA API)

## Project Structure

```
Persona AI/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── memory_extraction.py    # Memory extraction module
│   ├── personality_engine.py   # Personality transformation engine
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── components/
│   │   │   ├── ChatInterface.js
│   │   │   ├── MemoryDisplay.js
│   │   │   └── PersonalitySelector.js
│   │   └── index.js
│   ├── public/
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Add your NVIDIA API key to `.env`:
```
NVIDIA_API_KEY=your_api_key_here
```

6. Run the FastAPI server:
```bash
python main.py
# Or using uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional, defaults to localhost:8000):
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### `POST /api/extract-memory`
Extract memory from chat messages.

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "I love coffee in the morning"},
    {"role": "assistant", "content": "That's great!"}
  ],
  "user_id": "default_user"
}
```

**Response:**
```json
{
  "extracted_memory": {
    "preferences": [...],
    "emotional_patterns": [...],
    "facts": [...]
  },
  "total_memory": {...}
}
```

### `POST /api/transform-personality`
Transform response with personality engine.

**Request:**
```json
{
  "messages": [...],
  "personality": "calm_mentor",
  "user_id": "default_user"
}
```

**Response:**
```json
{
  "personality": "calm_mentor",
  "response": "...",
  "before_response": "...",
  "after_response": "..."
}
```

### `POST /api/chat`
Complete chat endpoint (extract memory + generate personality response).

### `GET /api/memory/{user_id}`
Get stored memory for a user.

## Usage

1. **Start both servers** (backend and frontend)

2. **Add chat messages**: Type messages in the chat interface (up to 30 messages)

3. **Select personality**: Choose from Calm Mentor, Witty Friend, or Therapist

4. **Send messages**: Each message will automatically:
   - Extract memory from the conversation
   - Generate a response with the selected personality
   - Show before/after comparison

5. **View extracted memory**: The right panel displays all extracted preferences, emotional patterns, and facts

## Deployment

### Backend Deployment (Example: Heroku/Railway/Render)

1. Add a `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables:
- `NVIDIA_API_KEY`

3. Deploy using your preferred platform

### Frontend Deployment (Example: Vercel/Netlify)

1. Build the React app:
```bash
npm run build
```

2. Set environment variable:
- `REACT_APP_API_URL` (your backend URL)

3. Deploy the `build` folder

## Key Design Decisions

1. **Structured Output Parsing**: Uses JSON extraction with fallback regex parsing to handle LLM response variations
2. **Memory Storage**: In-memory dictionary (can be easily replaced with a database)
3. **Modular Architecture**: Separate modules for memory extraction and personality transformation
4. **User Context Integration**: Personality engine incorporates user memory for personalized responses
5. **Before/After Comparison**: Shows the transformation effect of personality engine

## Future Enhancements

- Database integration for persistent memory storage
- Multiple user support with authentication
- Memory deduplication and merging
- More personality options
- Memory importance scoring and pruning
- Export/import memory functionality

## License

This project is for assignment purposes.

## Notes

- The NVIDIA API key in the example is a placeholder. Replace it with your own key.
- Memory extraction works best with 10+ messages for better context.
- The personality transformation is more noticeable with longer conversations.


