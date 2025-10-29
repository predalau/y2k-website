# Y2K Shopping Website 🌈✨

A visually stunning e-commerce website with Y2K aesthetic and smooth CSS animations.

## 🎨 Project Vision

This project aims to create a full-featured shopping website with:
- **Y2K Theme**: Nostalgic late 90s/early 2000s design aesthetic
- **Pure CSS Animations**: Smooth, eye-catching animations without external libraries
- **Full E-commerce Features**: Complete shopping experience from browse to checkout

## 📋 Features (Planned)

- 🛍️ Product catalog with categories
- 🛒 Interactive shopping cart
- 👤 User authentication and profiles
- 💳 Secure payment processing (Stripe)
- 📦 Order management and tracking
- ⚡ Smooth animations and transitions
- 📱 Responsive design

## 🔧 Tech Stack

✅ **Stack Selected and Configured!**

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: Pure CSS with custom Y2K animations
- **HTTP Client**: Axios
- **Routing**: Vue Router

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **API Docs**: Auto-generated with Swagger UI

### Development Tools
- **Version Control**: Git + GitHub
- **Package Managers**: npm (frontend), pip (backend)

See [TECH_STACK_GUIDE.md](./TECH_STACK_GUIDE.md) for detailed rationale and learning resources.

## 📁 Project Structure

```
y2k-website/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── core/              # Configuration
│   │   ├── models/            # Database models
│   │   ├── routes/            # API endpoints
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── database.py        # DB connection
│   │   └── main.py            # App entry point
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── README.md             # Backend docs
│
├── frontend/                  # Vue.js application
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── assets/           # Images, fonts
│   │   ├── components/       # Reusable components
│   │   ├── router/           # Vue Router setup
│   │   ├── styles/           # CSS (Y2K theme!)
│   │   │   ├── reset.css
│   │   │   ├── variables.css
│   │   │   ├── animations.css
│   │   │   └── global.css
│   │   ├── views/            # Page components
│   │   ├── App.vue           # Root component
│   │   └── main.js           # Entry point
│   ├── package.json          # npm dependencies
│   ├── vite.config.js        # Vite config
│   └── README.md             # Frontend docs
│
├── docs/                     # Additional documentation
├── TECH_STACK_GUIDE.md      # Tech stack decisions
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### ✅ Ready to Run!

Everything is set up and ready to go. Just start the servers:

**Terminal 1 - Start Backend:**
```bash
cd /Users/preda/Documents/Projects/y2k-website
./start-backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /Users/preda/Documents/Projects/y2k-website
./start-frontend.sh
```

Then open your browser:
- **Website**: http://localhost:5173 🌈
- **API Docs**: http://localhost:8000/api/v1/docs 📚

### 📖 Detailed Guides

- **[QUICKSTART.md](./QUICKSTART.md)** - Fast start guide with examples
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Complete setup from scratch
- **[TECH_STACK_GUIDE.md](./TECH_STACK_GUIDE.md)** - Technology decisions

### First Time Setup (Already Done! ✓)

If you need to set up on a different machine:

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
```

## 🎨 Y2K Design Features

### Color Palette
- 💗 Cyber Pink (`#ff00ff`)
- 💙 Cyber Blue (`#00ffff`)
- 💚 Neon Green (`#39ff14`)
- 💛 Electric Yellow (`#ffff00`)
- 💜 Cyber Purple (`#9945ff`)

### Pure CSS Animations
All animations built from scratch:
- `gradient-shift` - Animated gradients
- `glitch` - Glitch text effects
- `neon-pulse` - Pulsing neon glow
- `holographic` - Holographic text
- `float` - Floating elements
- `fade-in-up` - Smooth fade entrances
- And 15+ more custom animations!

### Typography
- **Display**: Orbitron (retro-futuristic)
- **Body**: Space Grotesk (modern readability)

## 📚 Documentation

- [Tech Stack Selection Guide](./TECH_STACK_GUIDE.md) - Why we chose this stack
- [Backend README](./backend/README.md) - FastAPI setup and API docs
- [Frontend README](./frontend/README.md) - Vue.js setup and component guide

## 🛠️ Development Status

### ✅ Completed - Phase 1: Foundation
- [x] Git repository initialized and connected to GitHub
- [x] Tech stack selected (Vue.js + FastAPI + Pure CSS)
- [x] Backend structure created with FastAPI
- [x] Frontend structure created with Vue.js 3 + Vite
- [x] Y2K CSS design system with 20+ animations
- [x] Pure CSS animation library (no external dependencies)
- [x] API client configuration with Axios
- [x] Vue Router setup with page transitions
- [x] Beautiful Y2K home page with animations
- [x] Development environment fully configured
- [x] **Backend server running** ✅
- [x] **Frontend server running** ✅
- [x] Both servers communicating via proxy

### 🔨 Phase 2: Core Features (Next)
- [ ] Database models (User, Product, Order, Cart)
- [ ] Product catalog API endpoints
- [ ] Product display page with Y2K styling
- [ ] Shopping cart functionality
- [ ] User authentication system (JWT)
- [ ] Checkout flow

### 📋 Phase 3: Advanced Features
- [ ] Payment integration (Stripe)
- [ ] Order management and tracking
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Product search and filters
- [ ] User reviews and ratings
- [ ] Wishlist feature
- [ ] Deployment configuration

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm run test
```

## 🚢 Deployment

(Deployment instructions will be added)

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

## 📝 License

(To be determined)

## 🙏 Acknowledgments

- Vue.js team for excellent documentation
- FastAPI for modern Python web framework
- Y2K aesthetic community for inspiration

---

**Last Updated**: October 29, 2025  
**Status**: Development Phase - Structure Complete ✓
