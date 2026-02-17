# RVCE OMR - Windows Installation Guide

## Prerequisites

Install the following software on your Windows machine:

### 1. Python 3.10+
Download from: https://www.python.org/downloads/

During installation, **check "Add Python to PATH"**.

Verify installation:
```cmd
python --version
```

### 2. Node.js 18+
Download from: https://nodejs.org/

Verify installation:
```cmd
node --version
npm --version
```

### 3. uv (Python package manager)
Install via PowerShell (run as Administrator):
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Or via pip:
```cmd
pip install uv
```

Verify installation:
```cmd
uv --version
```

---

## Installation Steps

### 1. Create Virtual Environment

Open Command Prompt in the project root and run:

```cmd
uv venv
```

This creates a `.venv` folder with the virtual environment.

### 2. Install Python Dependencies

```cmd
uv sync
```

### 3. Install Frontend Dependencies

```cmd
cd frontend
npm install
cd ..
```

---

## Running the Application

### Option 1: Using run.bat

Simply double-click `run.bat` in the project root.

This opens two new command windows:
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000

### Option 2: Manual

Open two separate Command Prompt windows:

**Window 1 - Backend:**
```cmd
cd backend
python main.py
```

**Window 2 - Frontend:**
```cmd
cd frontend
npm run dev
```

---

## Access the Application

Open your browser and go to: **http://localhost:3000**

---

## Troubleshooting

### Backend fails to start with "Module not found" error
Run `uv sync` again to ensure all dependencies are installed.

### Frontend fails with "npm is not recognized"
Ensure Node.js is installed and added to PATH. Restart Command Prompt after installation.

### Port 8000 or 3000 already in use
Stop any other application using those ports, or modify the port in:
- Backend: `backend/main.py`
- Frontend: `frontend/package.json`

---

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
