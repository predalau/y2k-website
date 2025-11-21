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

    <!-- Products Section -->
    <section class="products-section section-scroll">
      <h2 class="section-title neon-text-blue text-center mb-5">Shop Collection</h2>
      <div class="container">
        <div v-if="loading" class="loading-state">
          <div class="loader"></div>
          <p>Loading products...</p>
        </div>
        <div v-else class="carousel-wrapper">
          <div class="products-grid" ref="productsGrid">
            <div class="product-item hover-glow"
                 v-for="(product, index) in products.slice(0, 6)"
                 :key="product.id"
                 :ref="el => { if (el) productRefs[index] = el }"
                 :class="{ 'in-view': visibleProducts[index] }">
            <div class="product-img-container">
              <img v-if="product.images && product.images.length > 0"
                   :src="product.images[0].image_url"
                   :alt="product.name"
                   class="product-img"/>
              <div v-else class="product-img-placeholder">
                <span>{{ product.name.charAt(0) }}</span>
              </div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-price">${{ product.base_price }}</p>
              <button class="btn btn-primary hover-glow add-to-cart" @click="handleAddToCart(product)">
                Add to Cart
              </button>
              </div>
            </div>
          </div>
        </div>
        <button class="carousel-scroll-arrow carousel-scroll-left"
                @click="scrollCarouselPrev"
                v-if="products.length > 0 && canScrollLeft">
            <img src="@/assets/scroll_arrow.png" alt="Scroll Previous" />
        </button>
        <button class="carousel-scroll-arrow carousel-scroll-right"
                @click="scrollCarouselNext"
                v-if="products.length > 0 && canScrollRight">
            <img src="@/assets/scroll_arrow.png" alt="Scroll Next" />
        </button>
      </div>
    </section>

        <!-- Gallery Highlights Section -->
    <section class="gallery-highlights section-scroll">
      <h2 class="section-title neon-text-silver text-center mb-5">Featured Artists</h2>
      <div class="carousel-container">
          <div class="carousel-row">
            <!-- Artist card outside carousel -->
            <div class="carousel-card artist-card hover-glow scale-in" style="background-image: url('../src/assets/poli2.png'); background-size: 65%; background-position: center; background-repeat: no-repeat;">
              <h3 class="artist-name">Christian Roncea</h3>
              <p class="gallery-art-title">Furby Collection</p>
            </div>
            <!-- Carousel with product cards -->
            <div class="carousel">
              <div class="carousel-card product-card hover-glow scale-in" v-for="n in 3" :key="`product-${n}`" :style="`animation-delay: ${n * 0.2 + 0.2}s`">
                <div class="product-image silver-bg"></div>
                <h3 class="product-title">Product {{ n }}</h3>
                <p class="gallery-art-title">Artwork Title {{ n }}</p>
              </div>
            </div>
          </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta section-scroll">
      <div class="container">
        <div class="cta-content glass p-5">
          <h2 class="cta-title mb-3">
            Join the AEVVM movement
          </h2>
          <p class="cta-text mb-4">
            Sign up now and get exclusive access to our artist collaborations and limited-edition drops.
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
import { ref, onMounted, onUnmounted } from 'vue'
import apiClient from '../api/client.js'
import { useCart } from '../composables/useCart'

const products = ref([])
const loading = ref(true)
const { addToCart } = useCart()

// Carousel animation refs
const productsGrid = ref(null)
const productRefs = ref([])
const visibleProducts = ref(Array(6).fill(false))
let observer = null

// Carousel scroll arrow visibility
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

// Fetch products from API
const fetchProducts = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/products/')
    // API returns array directly, not wrapped in products property
    products.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    loading.value = false
  }
}

// Add to cart handler
const handleAddToCart = async (product) => {
  // Get product with variants
  try {
    const productResponse = await apiClient.get(`/products/${product.id}`)
    const productData = productResponse.data
    const variants = productData.variants
    if (variants && variants.length > 0) {
      const success = await addToCart(variants[0].id, 1)
      if (success) {
        alert(`${product.name} added to cart!`)
      }
    } else {
      alert('No variants available for this product')
    }
  } catch (error) {
    console.error('Error adding to cart:', error)
    alert('Failed to add to cart')
  }
}

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

// Check scroll position to show/hide arrows
const updateArrowVisibility = () => {
  if (!productsGrid.value) return

  const { scrollLeft, scrollWidth, clientWidth } = productsGrid.value

  // Can scroll left if we're not at the start
  canScrollLeft.value = scrollLeft > 10

  // Can scroll right if we're not at the end
  canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 10
}

// Scroll carousel to next item
const scrollCarouselNext = () => {
  if (productsGrid.value) {
    const scrollAmount = 320 + 32; // card width + gap
    productsGrid.value.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    });
  }
}

// Scroll carousel to previous item
const scrollCarouselPrev = () => {
  if (productsGrid.value) {
    const scrollAmount = 320 + 32; // card width + gap
    productsGrid.value.scrollBy({
      left: -scrollAmount,
      behavior: 'smooth'
    });
  }
}

onMounted(() => {
  fetchProducts()

  // Setup intersection observer for carousel animations
  setTimeout(() => {
    if (productsGrid.value) {
      observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            const index = productRefs.value.indexOf(entry.target)
            if (index !== -1) {
              visibleProducts.value[index] = entry.isIntersecting
            }
          })
        },
        {
          root: productsGrid.value,
          threshold: 0.6,
          rootMargin: '0px'
        }
      )

      productRefs.value.forEach((el) => {
        if (el) observer.observe(el)
      })

      // Add scroll event listener to update arrow visibility
      productsGrid.value.addEventListener('scroll', updateArrowVisibility)
      // Initial check
      updateArrowVisibility()
    }
  }, 100)
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
  if (productsGrid.value) {
    productsGrid.value.removeEventListener('scroll', updateArrowVisibility)
  }
})
</script>

<style scoped>
.carousel-row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
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
  justify-content: flex-start;
  gap: var(--space-xl);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-left: 0;
  padding-bottom: var(--space-md);
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
  box-shadow: 0 0 24px var(--color-silver);
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  align-items: start;
  object-fit: cover;
}
.artist-card {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  justify-content: flex-end;
}
.artist-card .artist-name,
.artist-card .gallery-art-title {
  background: rgba(0, 0, 0, 0.7);
  padding: var(--space-sm);
  border-radius: var(--radius-sm);
  backdrop-filter: blur(4px);
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
  text-shadow: 0 0 8px var(--color-gray-light), 0 0 16px var(--color-silver);
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
  background: var(--color-black) opacity(0.95);
  border: 2px solid var(--color-silver-blue);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  min-width: 220px;
  max-width: 260px;
  color: var(--color-silver-blue);
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

/* Products Section */
.products-section {
  padding: var(--space-2xl) 0;
  position: relative;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 70vh;
}

.products-grid {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: var(--space-xl);
  height: 70vh;
  max-height: 70vh;
  padding: 0 var(--space-2xl);
  align-items: center;
  position: relative;
}

/* Carousel scroll arrows */
.carousel-scroll-arrow {
  position: absolute;
  top: 50%;
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 100;
  transition: all var(--transition-base);
  padding: 0;
}

.carousel-scroll-right {
  right: 5vw;
  transform: translateY(-50%) rotate(-90deg);
}

.carousel-scroll-right:hover {
  transform: translateY(-50%) rotate(-90deg) scale(1.15);
  filter: drop-shadow(0 0 12px rgba(192, 192, 192, 0.6));
}

.carousel-scroll-left {
  left: 5vw;
  transform: translateY(-50%) rotate(90deg);
}

.carousel-scroll-left:hover {
  transform: translateY(-50%) rotate(90deg) scale(1.15);
  filter: drop-shadow(0 0 12px rgba(192, 192, 192, 0.6));
}

.carousel-scroll-arrow img {
  width: 96px;
  height: 96px;
  opacity: 0.6;
  transition: opacity var(--transition-base);
}

.carousel-scroll-arrow:hover img {
  opacity: 0.9;
}

/* Edge fade indicators for scroll hint */
.products-section::before,
.products-section::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 120px;
  pointer-events: none;
  z-index: 10;
  opacity: 0.8;
}

.products-section::before {
  left: 0;
  background: linear-gradient(to right,
    rgba(5, 5, 16, 0.95) 0%,
    rgba(5, 5, 16, 0.7) 40%,
    transparent 100%
  );
}

.products-section::after {
  right: 0;
  background: linear-gradient(to left,
    rgba(5, 5, 16, 0.95) 0%,
    rgba(5, 5, 16, 0.7) 40%,
    transparent 100%
  );
}

.product-item {
  background: var(--color-black);
  border: 2px solid var(--color-cyber-blue);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  min-width: 320px;
  max-width: 320px;
  height: 60vh;
  flex-shrink: 0;
  scroll-snap-align: center;

  /* Brutalist carousel animation - default state (out of view) */
  opacity: 0.4;
  transform: scale(0.88);
  filter: grayscale(0.6) brightness(0.7);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* In-view state - sharp, mechanical transition */
.product-item.in-view {
  opacity: 1;
  transform: scale(1);
  filter: grayscale(0) brightness(1);
  border-color: var(--color-silver);
}

.product-item:hover {
  transform: scale(1) translateY(-5px);
  box-shadow: 0 8px 32px rgba(0, 250, 255, 0.3);
}

.product-item.in-view:hover {
  border-color: var(--color-cyber-blue);
}

.product-img-container {
  width: 100%;
  height: 68%;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-cyber-blue);
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.product-name {
  font-size: var(--font-lg);
  color: var(--color-silver);
  margin: 0;
}

.product-price {
  font-size: var(--font-xl);
  color: var(--color-cyber-blue);
  font-weight: bold;
  margin: 0;
}

.add-to-cart {
  width: 100%;
  margin-top: var(--space-sm);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: var(--space-lg);
}

.loading-state p {
  color: var(--color-chrome);
  font-size: var(--font-lg);
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* Product Image Placeholder */
.product-img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-steel);
  font-size: 4rem;
  font-weight: 900;
  color: var(--color-chrome);
  text-transform: uppercase;
}

/* Scrollbar styling for carousel */
.products-grid::-webkit-scrollbar {
  height: 12px;
}

.products-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

.products-grid::-webkit-scrollbar-thumb {
  background: var(--color-cyber-blue);
  border-radius: 10px;
  border: 2px solid rgba(0, 0, 0, 0.3);
}

.products-grid::-webkit-scrollbar-thumb:hover {
  background: var(--color-silver);
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

  /* Smaller cards on mobile */
  .products-grid {
    padding: 0 var(--space-lg);
    gap: var(--space-lg);
  }

  .product-item {
    min-width: 260px;
    max-width: 260px;
    height: 55vh;
  }

  .products-section::before,
  .products-section::after {
    width: 80px;
  }

  .carousel-scroll-right {
    right: 10vw;
  }

  .carousel-scroll-left {
    left: 10vw;
  }

  .carousel-scroll-arrow img {
    width: 64px;
    height: 64px;
  }
}
</style>
