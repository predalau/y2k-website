import poli_img from '../assets/poli.jpg';
import poli_art from '../assets/poli_art.jpg';
<template>
  <div class="home">
      <div class="hero-background-logo">
        <img src="@/assets/leather-bg2.jpg" alt="Leather Background" class="leather-bg" />
        <img src="@/assets/logo2.png" alt="Logo Background" class="logo-bg pulse-scale"/>
      </div>
    <!-- Hero Section -->
    <section class="hero section-scroll">
      <div class="container scroll-indicator-container scroll-indicator">
        <img src="@/assets/scroll_arrow.png" alt="Scroll Arrow" class="scroll-arrow" @click="scrollToNextSection"/>
      </div>
    </section>

    <!-- Gallery Highlights Section -->
    <section class="gallery-highlights section-scroll">
      <h2 class="section-title neon-text-silver text-center mb-5">Featured Artists & Art</h2>
      <div class="carousel-container">
          <div class="carousel-row">
            <!-- Artist card outside carousel -->
            <div class="carousel-card artist-card hover-glow scale-in">
              <div class="artist-image silver-bg">
                <img src="../assets/poli2.png" alt="Artist Name" class="image-fit"/>
              </div>
              <h3 class="artist-name">Christian Roncea</h3>
              <p class="gallery-art-title">Furby Collection</p>
            </div>
            <!-- Carousel with product cards -->
            <div class="carousel">
              <div class="carousel-card product-card hover-glow scale-in" v-for="n in 7" :key="`product-${n}`" :style="`animation-delay: ${n * 0.2 + 0.2}s`">
                <div class="product-image silver-bg"></div>
                <h3 class="product-title">Product {{ n }}</h3>
                <p class="gallery-art-title">Artwork Title {{ n }}</p>
              </div>
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
          <div class="artist-card hover-glow scale-in" v-for="n in 3" :key="`artist-${n}`" :style="`animation-delay: ${n * 0.2}s`">
            <div class="artist-image blue-bg"> 
              <img src="../assets/poli.jpg" alt="Artist Name" class="image-fit"/>
            </div>
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

<script setup>
function scrollToNextSection() {
  const home = document.querySelector('.home');
  const sections = home.querySelectorAll('.section-scroll');
  const currentScroll = home.scrollTop;
  for (let i = 0; i < sections.length; i++) {
    const sectionTop = sections[i].offsetTop;
    if (sectionTop > currentScroll + 10) {
      home.scrollTo({
        top: sectionTop,
        behavior: 'smooth'
      });
      break;
    }
  }
}
</script>

<style scoped>
.carousel-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 60vh;
  gap: var(--space-xl);
}
/* Logo Bar */
.logo-bar {
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  background: transparent;
  pointer-events: none;
}
.site-logo {
  width: 96px;
  height: auto;
  margin: 1.5rem 0 0 0;
  filter: drop-shadow(0 2px 16px #0008);
  pointer-events: auto;
}
.scroll-indicator-container {
  position: absolute; /* or fixed, depending on your layout */
  bottom: 0.5rem; /* or wherever you want it */
  left: 50%;
  transform: translateX(-50%);
}
.scroll-arrow {
  width: 100px;
  height: auto;
  opacity: 0.8;
}
.scroll-arrow:hover {
 animation: float 2s infinite;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  height: 70vh;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: var(--space-2xl) 0;
}

.home {
  background: linear-gradient(135deg, #050510 0%, #181a2e86 100%);
  color: var(--color-silver);
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  position: relative;
}

.background-shape {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 75vw;
  height: 75vh;
  max-width: 80%;
  max-height: 80%;
  transform: translate(-50%, -50%);
  z-index: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.background-shape img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0.9;
}

.hero-background-logo {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 100vw;
  height: 100vh;
  max-width: 100%;
  max-height: 100%;
  transform: translate(-50%, -50%);
  z-index: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.hero-background-logo .leather-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 1;
  z-index: 1;
}
.hero-background-logo .logo-bg {
  position: absolute;
  top: 5%;
  width: 70%;
  height: 70%;
  object-fit: contain;
  opacity: 0.85;
  z-index: 2;
}

.home > *:not(.hero-background-logo) {
  position: relative;
  z-index: 1;
}

.section-scroll {
  scroll-snap-align: start;
  min-height: 100vh;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}


.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  margin-bottom: var(--space-lg);
  font-weight: 900;
  text-shadow: #0061d0ff 1px 0 10px;
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
  position: absolute;
  left: 0;
  right: 0;
  bottom: 20%;
  width: 100%;
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
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
}
.carousel-container {
  height: 65vh;
  width: 90%;
  min-height: 65vh;
  min-width: 90vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.carousel {
  display: flex;
  flex-direction: row;
  align-items: start;
  justify-content: center;
  gap: var(--space-xl);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}
.carousel-card {
  height: 50vh;
  width: 20vw;
  background: var(--color-black);
  border: 2px solid var(--color-silver);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  min-width: 220px;
  max-width: 260px;
  color: var(--color-silver);
  box-shadow: 0 0 24px var(--color-cyber-blue);
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  align-items: start;
  object-fit: cover;
}
.artist-card .artist-image {
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
  display: flex;
  align-items: center;
  justify-content: center;
  object-fit: contain;
}
.product-card .product-image {
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-fit {
  width: 100%;
  height: 100%;
  object-fit: contain;    /* or 'contain' for full image without cropping */
  object-position: center;
  display: block;
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
  position: absolute;
  top: 5%;
  left: 50%;
  transform: translateX(-50%);
  width: max-content;
  text-align: center;
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
