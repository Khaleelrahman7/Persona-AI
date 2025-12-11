# Quick Start Guide

Get Persona AI up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- NVIDIA API key (get one at https://build.nvidia.com)

## Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo NVIDIA_API_KEY=your_api_key_here > .env

# Run the server
python main.py
# Or: python run.py
```

Backend will run at `http://localhost:8000`

## Step 2: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run at `http://localhost:3000`

## Step 3: Test the Application

1. Open `http://localhost:3000` in your browser
2. Select a personality (Calm Mentor, Witty Friend, or Therapist)
3. Type a message like: "I'm feeling stressed about my upcoming exam"
4. Click Send
5. View the extracted memory in the right panel
6. See the before/after personality comparison

## Example Messages to Try

Try these to see memory extraction in action:

1. "I love coffee in the morning, it helps me focus"
2. "I get anxious when I have too many deadlines"
3. "My birthday is on March 15th"
4. "I prefer working late at night"
5. "I'm a software engineer at a startup"

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Verify dependencies: `pip list`
- Check API key in `.env` file

### Frontend won't start
- Check Node version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### API connection errors
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify `REACT_APP_API_URL` in frontend `.env` (optional, defaults to localhost:8000)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- Experiment with different personalities and messages!


