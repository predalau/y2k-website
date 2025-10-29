# Y2K Shopping - Frontend

Vue.js 3 frontend with Y2K aesthetic and pure CSS animations.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm (or yarn)

### Installation

1. **Install Node.js** (if not already installed):
   - Download from https://nodejs.org/
   - Or use Homebrew: `brew install node`

2. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (default points to local backend)
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

5. **Open in browser**:
   - Frontend: http://localhost:5173
   - Vite will automatically reload on file changes

## 📁 Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── api/             # API client and service functions
│   │   └── client.js    # Axios instance with interceptors
│   ├── assets/          # Images, fonts, etc.
│   ├── components/      # Reusable Vue components
│   ├── router/          # Vue Router configuration
│   │   └── index.js     # Routes definition
│   ├── styles/          # Global CSS styles
│   │   ├── reset.css        # CSS reset
│   │   ├── variables.css    # Y2K color variables
│   │   ├── animations.css   # Pure CSS animations
│   │   └── global.css       # Global utility classes
│   ├── views/           # Page components
│   │   ├── Home.vue     # Homepage
│   │   ├── Products.vue # Products page
│   │   ├── Cart.vue     # Shopping cart
│   │   └── Login.vue    # Login page
│   ├── App.vue          # Root component
│   └── main.js          # Application entry point
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies and scripts
├── .env.example         # Example environment variables
└── README.md            # This file
```

## 🎨 Y2K Design System

### Color Palette
- **Cyber Pink**: `#ff00ff`
- **Cyber Blue**: `#00ffff`
- **Neon Green**: `#39ff14`
- **Electric Yellow**: `#ffff00`
- **Cyber Purple**: `#9945ff`

### Typography
- **Display Font**: Orbitron (headings, bold statements)
- **Body Font**: Space Grotesk (paragraphs, UI text)

### Animations (Pure CSS)
All animations are custom-built with pure CSS:
- `gradient-shift` - Animated gradient backgrounds
- `glitch` - Glitch effects for text/elements
- `neon-pulse` - Pulsing neon glow
- `float` - Floating animation
- `holographic` - Holographic text shine
- And many more! (see `animations.css`)

### Component Classes
- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary buttons
- `.card` - Card containers with glass effect
- `.neon-text` - Neon glowing text
- `.holographic` - Holographic gradient text
- `.glass` - Glassmorphism effect

## 🛠️ Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔌 API Integration

The frontend communicates with the FastAPI backend through Axios:

```javascript
// Example API call
import apiClient from '@/api/client'

const getProducts = async () => {
  const response = await apiClient.get('/products')
  return response.data
}
```

The API base URL is configured via environment variables.

## 🎯 Features Implemented

- ✅ Project structure and configuration
- ✅ Vue Router setup with pages
- ✅ Y2K design system (colors, fonts, variables)
- ✅ Pure CSS animations library
- ✅ Responsive glassmorphism UI components
- ✅ API client with interceptors
- ✅ Beautiful home page with animations
- ⏳ Product catalog (coming soon)
- ⏳ Shopping cart functionality (coming soon)
- ⏳ User authentication (coming soon)

## 📝 Development Tips

### Adding New Components
```bash
# Create a new component in src/components/
# Import and use in views or other components
```

### Using CSS Animations
```vue
<template>
  <div class="fade-in-up neon-pulse">
    Animated Element
  </div>
</template>
```

### Creating New Pages
1. Create Vue file in `src/views/`
2. Add route in `src/router/index.js`
3. Use `<router-link>` to navigate

## 🌈 Y2K Animation Examples

```vue
<!-- Holographic text -->
<h1 class="holographic">Y2K Shop</h1>

<!-- Neon glow text -->
<p class="neon-text">Cyber Style</p>

<!-- Glitch effect -->
<div class="text-glitch">Error 404</div>

<!-- Floating element -->
<div class="float">⚡</div>

<!-- Hover glow button -->
<button class="btn btn-primary hover-glow">Click Me</button>
```

## 🔧 Customization

### Adding New Colors
Edit `src/styles/variables.css`:
```css
:root {
  --color-custom: #your-color;
}
```

### Creating New Animations
Add to `src/styles/animations.css`:
```css
@keyframes your-animation {
  /* animation keyframes */
}

.your-class {
  animation: your-animation 2s ease infinite;
}
```

## 📱 Responsive Design

All components are responsive by default using:
- CSS Grid with `auto-fit`
- Flexbox layouts
- Media queries for mobile/tablet
- Clamp() for fluid typography

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change port in vite.config.js or use:
npm run dev -- --port 3000
```

**API connection issues?**
- Check backend is running on port 8000
- Verify VITE_API_URL in .env
- Check CORS settings in backend

**Styles not updating?**
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Clear Vite cache: `rm -rf node_modules/.vite`

## 📚 Learn More

- [Vue.js Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Vue Router](https://router.vuejs.org/)
- [CSS Tricks](https://css-tricks.com/) - For animation ideas

## 🎨 Design Inspiration

- Y2K aesthetic references
- Cyberpunk UI elements
- Retro-futuristic themes
- Neon and holographic effects
