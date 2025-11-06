<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero section-scroll">
      <div class="container">
        <h1 class="hero-title neon-text-silver neon-pulse">
          Welcome to Y2K Shop
        </h1>
        <p class="hero-subtitle neon-text-blue" style="animation-delay: 0.2s">
          Experience the Future of Retro Shopping
        </p>
        <div class="hero-buttons fade-in-up" style="animation-delay: 0.4s">
          <button class="btn btn-secondary hover-glow">
            Shop Now
          </button>
          <button class="btn btn-secondary hover-glow">
            View Collection
          </button>
        </div>
      </div>
    </section>

    <!-- Gallery Highlights Section -->
    <section class="gallery-highlights section-scroll">
      <div class="container">
        <h2 class="section-title neon-text-silver text-center mb-5">Featured Artists & Art</h2>
        <div class="gallery-grid">
          <!-- Placeholder for featured artists and art -->
          <div class="gallery-card card-glow scale-in" v-for="n in 3" :key="n" :style="`animation-delay: ${n * 0.2}s`">
            <div class="gallery-image silver-bg"></div>
            <h3 class="gallery-artist">Artist Name {{ n }}</h3>
            <p class="gallery-art-title">Artwork Title {{ n }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Artist/Product Sections -->
    <section class="artist-products section-scroll">
      <div class="container">
        <h2 class="section-title neon-text-blue text-center mb-5">Shop Artist Collections</h2>
        <div class="artist-grid">
          <!-- Placeholder for artist and product cards -->
          <div class="artist-card card-glow scale-in" v-for="n in 3" :key="`artist-${n}`" :style="`animation-delay: ${n * 0.2}s`">
            <div class="artist-image blue-bg"></div>
            <h3 class="artist-name">Artist {{ n }}</h3>
            <p class="product-title">T-Shirt Design {{ n }}</p>
            <button class="btn btn-primary hover-glow">Buy Now</button>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta section-scroll">
      <div class="container">
        <div class="cta-content glass p-5">
          <h2 class="cta-title mb-3">
            Join the Y2K Revolution
          </h2>
          <p class="cta-text mb-4">
            Sign up now and get exclusive access to our retro-futuristic collection
          </p>
          <button class="btn btn-primary hover-glow pulse-scale">
            Get Started
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      features: [
        {
          icon: '⚡',
          title: 'Lightning Fast',
          description: 'Experience blazing fast checkout and delivery',
          color: 'green'
        },
        {
          icon: '🎨',
          title: 'Unique Style',
          description: 'Curated Y2K aesthetic products you won\'t find elsewhere',
          color: 'pink'
        },
        {
          icon: '🔒',
          title: 'Secure Payment',
          description: 'Shop with confidence using our encrypted payment system',
          color: 'blue'
        }
      ]
    }
  }
}
</script>

<style scoped>
/* Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  padding: var(--space-2xl) 0;
}

.home {
  background: var(--bg-gradient);
  color: var(--color-silver);
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

.section-scroll {
  scroll-snap-align: start;
  min-height: 100vh;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}


.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  margin-bottom: var(--space-lg);
  font-weight: 900;
  text-shadow: #ffcc00 1px 0 10px;
}

.holographic {
  background: var(--gradient-holographic);
  background-clip: text;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  margin-bottom: var(--space-2xl);
  font-weight: 300;
  text-shadow: rgba(16, 37, 53, 0.267) 1px 0 10px;
}

.hero-buttons {
  display: flex;
  gap: var(--space-lg);
  justify-content: center;
  flex-wrap: wrap;
}
 .shape-1 {
  width: 400px;
  height: 400px;
  background: var(--color-silver);
  top: 10%;
  left: 10%;
 }
 .shape-2 {
  width: 300px;
  height: 300px;
  background: var(--color-cyber-blue);
  top: 60%;
  right: 10%;
 }
 .shape-3 {
  width: 350px;
  height: 350px;
  background: var(--color-black);
  bottom: 10%;
  left: 50%;
 }

 .gallery-highlights {
  
 }
 .gallery-grid {
  display: flex;
  gap: var(--space-xl);
  justify-content: center;
  flex-wrap: wrap;
 }
 .gallery-card {
  background: var(--color-black);
  border: 2px solid var(--color-silver);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  min-width: 220px;
  max-width: 260px;
  color: var(--color-silver);
  box-shadow: 0 0 24px var(--color-cyber-blue);
}
.gallery-image {
  width: 100%;
  height: 120px;
  background: var(--color-silver);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
}
.neon-text-silver {
  color: var(--color-silver);
  text-shadow: 0 0 8px var(--color-cyber-blue), 0 0 16px var(--color-silver);
}
.artist-products {

}
.artist-grid {
  display: flex;
  gap: var(--space-xl);
  justify-content: center;
  flex-wrap: wrap;
}
.artist-card {
  background: var(--color-black);
  border: 2px solid var(--color-cyber-blue);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  min-width: 220px;
  max-width: 260px;
  color: var(--color-cyber-blue);
  box-shadow: 0 0 24px var(--color-silver);
}
.artist-image {
  width: 100%;
  height: 120px;
  background: var(--color-cyber-blue);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
}
.blue-bg {
  background: var(--color-cyber-blue) !important;
}
.silver-bg {
  background: var(--color-silver) !important;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: var(--color-cyber-blue);
  top: 60%;
  right: 10%;
}

.shape-3 {
  width: 350px;
  height: 350px;
  background: var(--color-neon-green);
  bottom: 10%;
  left: 50%;
}

/* Features Section */
.features {
  padding: var(--space-3xl) 0;
  position: relative;
}

.section-title {
  font-size: var(--font-4xl);
  margin-bottom: var(--space-2xl);
}

.feature-icon {
  font-size: 4rem;
  margin-bottom: var(--space-md);
  display: block;
}

.feature-title {
  font-size: var(--font-2xl);
  margin-bottom: var(--space-md);
  background: var(--gradient-cyber);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

/* CTA Section */
.cta {
  padding: var(--space-3xl) 0;
  margin: var(--space-3xl) 0;
}

.cta-content {
  text-align: center;
  border-radius: var(--radius-xl);
  max-width: 800px;
  margin: 0 auto;
}

.cta-title {
  font-size: var(--font-4xl);
}

.cta-text {
  font-size: var(--font-lg);
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .shape {
    filter: blur(40px);
  }
}
</style>
