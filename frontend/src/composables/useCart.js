import { ref, computed } from 'vue'
import apiClient from '../api/client'

// Shared cart state
const cart = ref({
  items: [],
  total: 0,
  item_count: 0
})

const loading = ref(false)

// Generate or get session ID for guest carts
const getSessionId = () => {
  let sessionId = localStorage.getItem('cart_session_id')
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('cart_session_id', sessionId)
  }
  return sessionId
}

export function useCart() {
  const sessionId = getSessionId()

  // Fetch cart from backend
  const fetchCart = async () => {
    try {
      loading.value = true
      const response = await apiClient.get('/cart/', {
        params: { session_id: sessionId }
      })
      cart.value = response.data
    } catch (error) {
      console.error('Error fetching cart:', error)
    } finally {
      loading.value = false
    }
  }

  // Add item to cart
  const addToCart = async (variantId, quantity = 1) => {
    try {
      loading.value = true
      await apiClient.post('/cart/', {
        variant_id: variantId,
        quantity
      }, {
        params: { session_id: sessionId }
      })
      await fetchCart() // Refresh cart
      return true
    } catch (error) {
      console.error('Error adding to cart:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // Update cart item quantity
  const updateItemQuantity = async (cartItemId, newQuantity) => {
    try {
      await apiClient.put(`/cart/${cartItemId}`, {
        quantity: newQuantity
      })
      await fetchCart() // Refresh cart
    } catch (error) {
      console.error('Error updating cart item:', error)
    }
  }

  // Remove item from cart
  const removeCartItem = async (cartItemId) => {
    try {
      await apiClient.delete(`/cart/${cartItemId}`)
      await fetchCart() // Refresh cart
    } catch (error) {
      console.error('Error removing cart item:', error)
    }
  }

  // Clear all items from cart
  const clearAllItems = async () => {
    try {
      await apiClient.delete('/cart/', {
        params: { session_id: sessionId }
      })
      await fetchCart() // Refresh cart
    } catch (error) {
      console.error('Error clearing cart:', error)
    }
  }

  // Computed properties
  const itemCount = computed(() => cart.value.item_count || 0)
  const total = computed(() => cart.value.total || 0)
  const items = computed(() => cart.value.items || [])

  return {
    cart,
    loading,
    itemCount,
    total,
    items,
    fetchCart,
    addToCart,
    updateItemQuantity,
    removeCartItem,
    clearAllItems
  }
}
