# Complete Setup Guide - Y2K Shopping Website

This guide will walk you through setting up the complete development environment for the Y2K Shopping Website.

## 📋 Table of Contents

1. [Prerequisites Installation](#prerequisites-installation)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Verification](#verification)
5. [Common Issues](#common-issues)
6. [Next Steps](#next-steps)

---

## Prerequisites Installation

### 1. Install Python 3.9+

**Check if already installed:**
```bash
python3 --version
```

**Install on macOS:**
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from: https://www.python.org/downloads/
```

**Install on Windows:**
- Download from: https://www.python.org/downloads/
- ⚠️ Check "Add Python to PATH" during installation

**Install on Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Install Node.js 16+ and npm

**Check if already installed:**
```bash
node --version
npm --version
```

**Install on macOS:**
```bash
# Using Homebrew (recommended)
brew install node

# Or download from: https://nodejs.org/
```

**Install on Windows/Linux:**
- Download LTS version from: https://nodejs.org/

### 3. Install Git (Already Done ✓)

You've already initialized git! To verify:
```bash
git --version
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd /Users/preda/Documents/Projects/y2k-website/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# This creates a 'venv' folder in your backend directory
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**You'll see `(venv)` in your terminal prompt when activated**

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- And other dependencies

**Expected time:** 2-3 minutes

### Step 5: Set Up Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your preferred editor
# nano .env
# or
# code .env  (if using VS Code)
```

**For now, the defaults are fine! The database will use SQLite.**

### Step 6: Run the Backend Server

```bash
# Make sure virtual environment is activated (you should see (venv))
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/Users/preda/Documents/Projects/y2k-website/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 7: Verify Backend is Running

Open your browser and visit:
- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/api/v1/docs
- **Alternative Docs**: http://localhost:8000/api/v1/redoc

You should see the FastAPI welcome message!

**Keep this terminal window open** (backend server running)

---

## Frontend Setup

### Step 1: Open New Terminal Window

Keep the backend running in the previous terminal.

### Step 2: Navigate to Frontend Directory

```bash
cd /Users/preda/Documents/Projects/y2k-website/frontend
```

### Step 3: Install Node Dependencies

```bash
npm install
```

This installs:
- Vue.js 3
- Vite (build tool)
- Vue Router
- Axios (HTTP client)
- And other dependencies

**Expected time:** 1-2 minutes  
**You may see some warnings - this is normal**

### Step 4: Set Up Environment Variables

```bash
# Copy example env file
cp .env.example .env

# The default settings point to http://localhost:8000
# No need to edit unless you changed backend port
```

### Step 5: Run the Frontend Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.2  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Step 6: Open Frontend in Browser

Visit: http://localhost:5173

You should see:
- Beautiful Y2K-themed homepage
- Holographic title: "Welcome to Y2K Shop"
- Animated background elements
- Gradient buttons with hover effects
- Smooth animations and transitions

**Try these interactions:**
- Hover over buttons (they glow!)
- Watch the floating shapes
- See the gradient animations

---

## Verification Checklist

### Backend ✓
- [ ] Virtual environment created and activated
- [ ] Dependencies installed without errors
- [ ] Server running on http://localhost:8000
- [ ] Can access API docs at http://localhost:8000/api/v1/docs
- [ ] API returns JSON response

### Frontend ✓
- [ ] Node modules installed
- [ ] Development server running on http://localhost:5173
- [ ] Homepage loads with Y2K styling
- [ ] Animations are working
- [ ] No console errors in browser (press F12 to check)

### Both Running Simultaneously
- [ ] Backend terminal shows: `INFO: Uvicorn running...`
- [ ] Frontend terminal shows: `VITE v5.0.2 ready...`
- [ ] Can access both URLs without conflict

---

## Common Issues

### Issue: `python3: command not found`

**Solution:**
- Install Python from https://www.python.org/downloads/
- Or try `python` instead of `python3`

### Issue: `npm: command not found`

**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

### Issue: `pip install` fails

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then try installing again
pip install -r requirements.txt
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Update frontend .env:
VITE_API_URL=http://localhost:8001/api/v1
```

### Issue: Port 5173 already in use

**Solution:**
```bash
# Use a different port
npm run dev -- --port 3000
```

### Issue: `ModuleNotFoundError` in Python

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Frontend shows blank page

**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Verify backend is running
4. Check `.env` has correct API URL

### Issue: Import errors in VS Code

**Solution:**
This is normal! The packages aren't installed globally, only in your virtual environment. The code will still run.

To fix in VS Code:
1. Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose the venv interpreter (`./venv/bin/python`)

---

## Development Workflow

### Starting Both Servers

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # On macOS/Linux
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Stopping Servers

Press `Ctrl+C` in each terminal window

### Making Changes

**Backend:**
- Edit files in `backend/app/`
- Server auto-reloads on save (--reload flag)
- Check http://localhost:8000/api/v1/docs for API changes

**Frontend:**
- Edit files in `frontend/src/`
- Vite auto-reloads on save
- Browser updates automatically

---

## Next Steps

Now that everything is set up, here's what to do next:

### 1. Explore the Frontend
- Open `frontend/src/views/Home.vue` to see the homepage code
- Check `frontend/src/styles/` to see the Y2K CSS
- Try modifying colors in `variables.css`
- Add new animations in `animations.css`

### 2. Test the Backend API
- Visit http://localhost:8000/api/v1/docs
- Try the `/health` endpoint
- Read through `backend/app/main.py`

### 3. Start Building Features

**Recommended first feature:** Product Model
1. Create `backend/app/models/product.py`
2. Create `backend/app/schemas/product.py`
3. Create `backend/app/routes/products.py`
4. Add products endpoint to main.py

### 4. Learning Resources

**Vue.js:**
- Official Tutorial: https://vuejs.org/tutorial/
- Work through the interactive guide (2-3 hours)

**FastAPI:**
- Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- Build a simple API (2-3 hours)

**CSS Animations:**
- Experiment with `frontend/src/styles/animations.css`
- Try combining different animation classes

### 5. Version Control

Don't forget to commit your changes:

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Set up project structure and Y2K styling"

# Push to GitHub (after creating remote repo)
git push origin main
```

---

## Project Structure Reminder

```
y2k-website/
├── backend/           ← Python FastAPI
│   ├── venv/         ← Virtual environment (don't commit)
│   └── app/          ← Your backend code
└── frontend/         ← Vue.js app
    ├── node_modules/ ← Dependencies (don't commit)
    └── src/          ← Your frontend code
```

---

## Need Help?

### Documentation
- [Main README](./README.md)
- [Tech Stack Guide](./TECH_STACK_GUIDE.md)
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

### Resources
- FastAPI Docs: https://fastapi.tiangolo.com/
- Vue.js Docs: https://vuejs.org/
- Vite Docs: https://vitejs.dev/

---

## 🎉 Congratulations!

You now have a fully functional development environment with:
- ✅ FastAPI backend running with hot reload
- ✅ Vue.js frontend with Y2K styling
- ✅ Pure CSS animations working
- ✅ API documentation auto-generated
- ✅ Development workflow established

**Happy coding! 🚀**
