#!/bin/bash
# start.sh — Start the Product Learning Studio application
set -e
trap 'echo "Shutting down..."; [ -f .pids ] && while IFS= read -r pid; do kill "$pid" 2>/dev/null || true; done < .pids; rm -f .pids; exit 0' SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Portable sed (macOS + Linux)
portable_sed() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Port detection
find_available_port() {
    local port=$1
    if command -v lsof &>/dev/null; then
        while lsof -iTCP:$port -sTCP:LISTEN -t >/dev/null 2>&1; do
            echo "Port $port in use, trying $((port+1))..." >&2
            port=$((port+1))
        done
    fi
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Detect Python executable
    PYTHON=""
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    done

    if [ -n "$PYTHON" ]; then
        PYTHON_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
            echo "❌ Python 3.11+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    # Node.js 18+
    if command -v node &>/dev/null; then
        NODE_VERSION=$(node --version | sed 's/v//')
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
        if [ "$NODE_MAJOR" -lt 18 ]; then
            echo "❌ Node.js 18+ required (found $NODE_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Node.js $NODE_VERSION"
        fi
    else
        echo "❌ Node.js not found. Install from https://nodejs.org"
        errors=$((errors+1))
    fi

    # npm
    if ! command -v npm &>/dev/null; then
        echo "❌ npm not found"
        errors=$((errors+1))
    else
        echo "✓ npm $(npm --version)"
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# Backend setup
BACKEND_DIR="$SCRIPT_DIR/backend"
echo "=== Setting up backend ==="
cd "$BACKEND_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON -m venv .venv
fi

# Activate virtual environment (cross-platform)
if [ -f ".venv/Scripts/activate" ]; then
    # Windows Git Bash
    source .venv/Scripts/activate
else
    # macOS/Linux
    source .venv/bin/activate
fi

# Install dependencies
echo "Installing backend dependencies..."
pip install . -q

# Materialize dev.env if .env doesn't exist
if [ ! -f ".env" ] && [ -f "dev.env" ]; then
    echo "Creating .env from dev.env..."
    cp dev.env .env
fi

# Helper to convert path for native Windows programs
native_path() {
    if command -v cygpath >/dev/null 2>&1; then
        cygpath -m "$1"
    else
        printf '%s' "$1"
    fi
}

# Resolve database path
DB_PATH="$SCRIPT_DIR/app.db"

# Database — default to SQLite
export DATABASE_URL="${DATABASE_URL:-sqlite:///$(native_path "$DB_PATH")}"
echo "  Database: $DATABASE_URL"

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Find available backend port
BACKEND_PORT=$(find_available_port 9000)

# Frontend setup
FRONTEND_DIR="$SCRIPT_DIR/frontend"
echo ""
echo "=== Setting up frontend ==="
cd "$FRONTEND_DIR"

echo "Installing frontend dependencies..."
npm install --silent

# Find available frontend port
FRONTEND_PORT=$(find_available_port 5173)

# Update frontend Vite proxy to point to actual backend port
export BACKEND_PORT

# Start backend
cd "$BACKEND_DIR"
echo ""
echo "Starting backend on http://localhost:$BACKEND_PORT"
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$SCRIPT_DIR/.pids"

# Start frontend
cd "$FRONTEND_DIR"
echo "Starting frontend on http://localhost:$FRONTEND_PORT"
npm run dev -- --port $FRONTEND_PORT &
FRONTEND_PID=$!
echo "$FRONTEND_PID" >> "$SCRIPT_DIR/.pids"

cd "$SCRIPT_DIR"

echo ""
echo "=== Services running ==="
echo "  Backend:  http://localhost:$BACKEND_PORT"
echo "  Frontend: http://localhost:$FRONTEND_PORT"
echo "  API Docs: http://localhost:$BACKEND_PORT/api/docs"
echo ""
echo "=== Default Credentials ==="
echo "  Email:    demo@example.com"
echo "  Password: demo1234"
echo ""
echo "Press Ctrl+C to stop all services"
wait
