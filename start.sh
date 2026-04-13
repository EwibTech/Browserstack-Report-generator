#!/bin/bash

echo "🚀 Starting BrowserStack Report Generator..."

echo ""
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Starting Flask server on port 5000..."
python app.py &
BACKEND_PID=$!

cd ..

echo ""
echo "📦 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Starting React development server on port 3000..."
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting..."
echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
