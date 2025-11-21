<template>
  <div class="cart-container" :class="{ 'cart-hidden': !isVisible }">
    <!-- Cart Icon Button -->
    <button class="cart-button chrome-card" @click="toggleCart">
      <img src="@/assets/cross.png" alt="Cart" class="cart-icon" />
      <span v-if="itemCount > 0" class="cart-badge">{{ itemCount }}</span>
    </button>

    <!-- Cart Dropdown -->
    <transition name="cart-slide">
      <div v-if="isOpen" class="cart-dropdown chrome-card">
        <div class="cart-header">
          <h3 class="chrome-text">Shopping Cart</h3>
          <button class="close-btn" @click="toggleCart">×</button>
        </div>

        <div v-if="loading" class="cart-loading">
          <div class="loader"></div>
          <p>Loading cart...</p>
        </div>

        <div v-else-if="items.length === 0" class="cart-empty">
          <p>Your cart is empty</p>
        </div>

        <div v-else class="cart-items">
          <div v-for="item in items" :key="item.id" class="cart-item">
            <div class="item-image">
              <img v-if="item.image_url" :src="item.image_url" :alt="item.product_name" />
              <div v-else class="item-placeholder">{{ item.product_name.charAt(0) }}</div>
            </div>
            <div class="item-details">
              <h4 class="item-name">{{ item.product_name }}</h4>
              <p class="item-variant">{{ item.variant_name }}</p>
              <p class="item-price">${{ item.price }}</p>
            </div>
            <div class="item-actions">
              <div class="quantity-controls">
                <button @click="updateQuantity(item.id, item.quantity - 1)" class="qty-btn">−</button>
                <span class="qty-value">{{ item.quantity }}</span>
                <button @click="updateQuantity(item.id, item.quantity + 1)" class="qty-btn">+</button>
              </div>
              <button @click="removeItem(item.id)" class="remove-btn">Remove</button>
            </div>
          </div>
        </div>

        <div v-if="items.length > 0" class="cart-footer">
          <div class="cart-total">
            <span class="total-label">Total:</span>
            <span class="total-value">${{ total.toFixed(2) }}</span>
          </div>
          <button class="btn btn-primary checkout-btn">Checkout</button>
          <button class="btn btn-secondary clear-btn" @click="clearCart">Clear Cart</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCart } from '../composables/useCart'

const { cart, loading, fetchCart, updateItemQuantity, removeCartItem, clearAllItems } = useCart()

const isOpen = ref(false)
const isVisible = ref(true)

const items = computed(() => cart.value.items || [])
const total = computed(() => cart.value.total || 0)
const itemCount = computed(() => cart.value.item_count || 0)

const toggleCart = () => {
  isOpen.value = !isOpen.value
}

const updateQuantity = async (itemId, newQuantity) => {
  await updateItemQuantity(itemId, newQuantity)
}

const removeItem = async (itemId) => {
  await removeCartItem(itemId)
}

const clearCart = async () => {
  if (confirm('Are you sure you want to clear your cart?')) {
    await clearAllItems()
  }
}

onMounted(() => {
  fetchCart()
})
</script>

<style scoped>
.cart-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.cart-hidden {
  opacity: 0;
  transform: translateY(-20px);
  pointer-events: none;
}

.cart-button {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  border: none;
  background: transparent;
  padding: 0;
  transition: all var(--transition-base);
}

.cart-button:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 0 12px rgba(192, 192, 192, 0.6));
}

.cart-icon {
  width: 50px;
  height: 50px;
  filter: invert(1);
  opacity: 0.7;
  transition: opacity var(--transition-base);
}

.cart-button:hover .cart-icon {
  opacity: 1;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--color-chrome);
  color: var(--color-black);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 900;
  border: 2px solid var(--color-black);
}

.cart-dropdown {
  position: absolute;
  top: 70px;
  right: 0;
  width: 400px;
  max-height: 600px;
  background: var(--bg-card);
  border: 1px solid var(--color-steel);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-steel);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  opacity: 1;
}

.cart-header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--color-steel);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-header h3 {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: var(--font-lg);
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-chrome);
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-base);
}

.close-btn:hover {
  color: var(--color-chrome-light);
}

.cart-loading,
.cart-empty {
  padding: var(--space-3xl);
  text-align: center;
  color: var(--color-concrete);
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-md);
  max-height: 400px;
  background: var(--color-gray-dark);
}

.cart-item {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-iron);
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--gradient-steel);
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--color-chrome);
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: var(--font-base);
  color: var(--color-chrome);
  margin: 0 0 var(--space-xs) 0;
  font-weight: 700;
}

.item-variant {
  font-size: var(--font-sm);
  color: var(--color-concrete);
  margin: 0 0 var(--space-xs) 0;
}

.item-price {
  font-size: var(--font-base);
  color: var(--color-chrome-light);
  font-weight: 700;
  margin: 0;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  align-items: flex-end;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  background: var(--color-graphite);
  border-radius: var(--radius-sm);
  padding: var(--space-xs);
}

.qty-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: var(--color-steel);
  color: var(--color-white);
  cursor: pointer;
  border-radius: var(--radius-sm);
  font-size: var(--font-base);
  font-weight: 700;
  transition: background var(--transition-base);
}

.qty-btn:hover {
  background: var(--color-chrome);
  color: var(--color-black);
}

.qty-value {
  color: var(--color-chrome);
  font-weight: 700;
  min-width: 30px;
  text-align: center;
}

.remove-btn {
  background: none;
  border: none;
  color: var(--color-concrete);
  font-size: var(--font-sm);
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  transition: color var(--transition-base);
}

.remove-btn:hover {
  color: var(--color-chrome);
}

.cart-footer {
  padding: var(--space-lg);
  border-top: 1px solid var(--color-steel);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-xl);
  font-weight: 700;
}

.total-label {
  color: var(--color-concrete);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.total-value {
  color: var(--color-chrome);
}

.checkout-btn,
.clear-btn {
  width: 100%;
}

/* Cart slide animation */
.cart-slide-enter-active,
.cart-slide-leave-active {
  transition: all 0.3s ease;
}

.cart-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.cart-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .cart-dropdown {
    width: 90vw;
    max-width: 350px;
    right: -10px;
  }
}
</style>
