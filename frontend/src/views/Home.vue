<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1 class="hero-title holographic fade-in-up">
          Welcome to Y2K Shop
        </h1>
        <p class="hero-subtitle neon-text-blue fade-in-up" style="animation-delay: 0.2s">
          Experience the Future of Retro Shopping
        </p>
        <div class="hero-buttons fade-in-up" style="animation-delay: 0.4s">
          <button class="btn btn-primary hover-glow">
            Shop Now
          </button>
          <button class="btn btn-secondary hover-glow">
            View Collection
          </button>
        </div>
      </div>
      
      <!-- Animated Background Elements -->
      <div class="bg-shapes">
        <div class="shape shape-1 float"></div>
        <div class="shape shape-2 float" style="animation-delay: 0.5s"></div>
        <div class="shape shape-3 float" style="animation-delay: 1s"></div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2 class="section-title neon-text text-center mb-5">
          Why Shop With Us?
        </h2>
        <div class="grid grid-3">
          <div class="card card-glow scale-in" v-for="(feature, index) in features" :key="index" :style="`animation-delay: ${index * 0.1}s`">
            <div class="feature-icon" :class="`neon-text-${feature.color}`">
              {{ feature.icon }}
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content glass p-5">
          <h2 class="cta-title holographic mb-3">
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

.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  margin-bottom: var(--space-lg);
  font-weight: 900;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  margin-bottom: var(--space-2xl);
  font-weight: 300;
}

.hero-buttons {
  display: flex;
  gap: var(--space-lg);
  justify-content: center;
  flex-wrap: wrap;
}

/* Background Animated Shapes */
.bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: var(--color-cyber-pink);
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
