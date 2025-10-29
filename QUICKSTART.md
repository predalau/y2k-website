# Quick Start Guide - Y2K Shopping Website

Your Y2K Shopping Website is now ready to run! 🎉

## ✅ What's Already Set Up

- ✅ Backend (FastAPI) - Configured and ready
- ✅ Frontend (Vue.js 3) - Installed and ready  
- ✅ Y2K CSS Styling - Beautiful animations included
- ✅ Development environment - All dependencies installed

## 🚀 Running the Website

### Option 1: Using the Startup Scripts (Easiest)

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

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd /Users/preda/Documents/Projects/y2k-website/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd /Users/preda/Documents/Projects/y2k-website/frontend
npm run dev
```

## 🌐 Access Your Website

Once both servers are running:

- **Frontend (Your Website)**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs

## 🎨 What You'll See

When you visit http://localhost:5173, you'll see:

- 🌈 **Holographic "Welcome to Y2K Shop" title** - With gradient animation
- ✨ **Floating animated shapes** - In the background
- 💫 **Neon glowing buttons** - With hover effects
- 🎭 **Feature cards** - With glassmorphism effect
- 🔮 **Smooth page transitions** - Pure CSS animations

## 🛠️ Making Changes

### Frontend Changes
- Edit files in `frontend/src/`
- Changes auto-reload in browser
- CSS styles are in `frontend/src/styles/`

### Backend Changes  
- Edit files in `backend/app/`
- Server auto-reloads on save
- API docs update automatically

## 📝 Next Development Steps

### 1. Create Product Model
```python
# backend/app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
```

### 2. Create Product Schema
```python
# backend/app/schemas/product.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True
```

### 3. Create Product Routes
```python
# backend/app/routes/products.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import product as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    # Your logic here
    return []
```

### 4. Add Products Component in Frontend
```vue
<!-- frontend/src/components/ProductCard.vue -->
<template>
  <div class="card card-glow hover-scale">
    <img :src="product.image_url" :alt="product.name">
    <h3>{{ product.name }}</h3>
    <p>{{ product.description }}</p>
    <p class="price neon-text-blue">${{ product.price }}</p>
    <button class="btn btn-primary">Add to Cart</button>
  </div>
</template>

<script>
export default {
  props: ['product']
}
</script>
```

## 🎨 Using Y2K Animations

The website comes with tons of pre-built CSS animations:

```html
<!-- Holographic text -->
<h1 class="holographic">Text</h1>

<!-- Neon glow -->
<p class="neon-text">Glowing</p>
<p class="neon-text-blue">Blue Glow</p>
<p class="neon-text-green">Green Glow</p>

<!-- Animations -->
<div class="float">Floating</div>
<div class="pulse-scale">Pulsing</div>
<div class="fade-in-up">Fade In</div>
<div class="glitch">Glitch</div>

<!-- Hover effects -->
<button class="hover-glow">Button</button>
<div class="hover-scale">Scale on hover</div>

<!-- Glassmorphism -->
<div class="glass">Glass effect</div>
<div class="card">Card with glass</div>
```

All animation classes are in `frontend/src/styles/animations.css`

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Check if uvicorn is installed
which uvicorn

# Try running directly
python -m uvicorn app.main:app --reload
```

### Frontend won't start
```bash
# Make sure dependencies are installed
cd frontend
npm install

# Clear cache and restart
rm -rf node_modules/.vite
npm run dev
```

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)  
lsof -ti:5173 | xargs kill -9
```

### Can't see changes
- Hard refresh browser: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- Check both terminals for errors
- Make sure both servers are running

## 📚 Learn More

- **Vue.js Tutorial**: https://vuejs.org/tutorial/
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **CSS Animations**: Check `frontend/src/styles/animations.css`

## 🎯 Current Features

✅ Project structure complete  
✅ Backend API running  
✅ Frontend UI running  
✅ Y2K design system  
✅ Pure CSS animations  
✅ Responsive layout  
✅ API documentation  
✅ Hot reload for development  

## 🔮 Coming Soon

⏳ Product catalog  
⏳ Shopping cart  
⏳ User authentication  
⏳ Checkout process  
⏳ Payment integration  
⏳ Order management  

---

**Need help?** Check the detailed guides:
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed setup instructions
- [TECH_STACK_GUIDE.md](./TECH_STACK_GUIDE.md) - Technology choices explained

**Happy coding! 🚀✨**
