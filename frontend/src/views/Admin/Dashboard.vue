<template>
  <div class="admin-dashboard">
    <h1 class="chrome-title">AEVVM Dashboard</h1>

    <!-- Date Range Filter -->
    <div class="dashboard-filters glass">
      <div class="filter-group">
        <label>Start Date:</label>
        <input type="date" v-model="startDate" @change="fetchData" class="input" />
      </div>
      <div class="filter-group">
        <label>End Date:</label>
        <input type="date" v-model="endDate" @change="fetchData" class="input" />
      </div>
      <button class="btn btn-secondary" @click="clearFilters">Clear Filters</button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="shimmer">Loading dashboard data...</div>
    </div>

    <!-- Key Stats Cards -->
    <div v-else class="stats-grid">
      <div class="stat-card chrome-card fade-in-up">
        <h3 class="chrome-text">Total Sales</h3>
        <p class="stat-value">${{ formatNumber(stats.total_sales) }}</p>
      </div>
      <div class="stat-card chrome-card fade-in-up" style="animation-delay: 0.1s">
        <h3 class="chrome-text">Orders</h3>
        <p class="stat-value">{{ stats.total_orders }}</p>
      </div>
      <div class="stat-card chrome-card fade-in-up" style="animation-delay: 0.2s">
        <h3 class="chrome-text">Users</h3>
        <p class="stat-value">{{ stats.total_users }}</p>
        <p class="stat-sub">+{{ stats.new_users }} new</p>
      </div>
      <div class="stat-card chrome-card fade-in-up" style="animation-delay: 0.3s">
        <h3 class="chrome-text">Avg Order</h3>
        <p class="stat-value">${{ formatNumber(stats.avg_order_value) }}</p>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="charts-row">
      <div class="chart-container card glass fade-in-up">
        <h3>Sales Over Time</h3>
        <div class="chart-wrapper">
          <Line v-if="salesChartData.labels.length > 0" :data="salesChartData" :options="chartOptions" />
          <p v-else class="no-data">No sales data available</p>
        </div>
      </div>
      <div class="chart-container card glass fade-in-up" style="animation-delay: 0.1s">
        <h3>Order Status Distribution</h3>
        <div class="chart-wrapper">
          <Doughnut v-if="statusChartData.labels.length > 0" :data="statusChartData" :options="doughnutOptions" />
          <p v-else class="no-data">No order data available</p>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="charts-row">
      <div class="chart-container card glass fade-in-up">
        <h3>Top Products by Revenue</h3>
        <div class="chart-wrapper">
          <Bar v-if="productsChartData.labels.length > 0" :data="productsChartData" :options="barOptions" />
          <p v-else class="no-data">No product data available</p>
        </div>
      </div>
      <div class="chart-container card glass fade-in-up" style="animation-delay: 0.1s">
        <h3>Top Artists by Sales</h3>
        <div class="chart-wrapper">
          <Bar v-if="artistsChartData.labels.length > 0" :data="artistsChartData" :options="barOptions" />
          <p v-else class="no-data">No artist data available</p>
        </div>
      </div>
    </div>

    <!-- Export Buttons -->
    <div class="export-section glass">
      <h3>Export Data</h3>
      <div class="export-buttons">
        <button class="btn btn-primary hover-glow" @click="exportOrders">
          📊 Export Orders
        </button>
        <button class="btn btn-primary hover-glow" @click="exportUsers">
          👥 Export Users
        </button>
        <button class="btn btn-primary hover-glow" @click="exportProducts">
          📦 Export Products
        </button>
        <button class="btn btn-primary hover-glow" @click="exportArtistSales">
          🎨 Export Artist Sales
        </button>
      </div>
    </div>

    <!-- Recent Orders Table -->
    <div class="recent-orders card glass">
      <h3>Recent Orders</h3>
      <div v-if="recentOrders.length === 0" class="no-data">
        No recent orders
      </div>
      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>Order #</th>
              <th>Customer</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in recentOrders" :key="order.id" class="hover-scale">
              <td><strong>{{ order.order_number }}</strong></td>
              <td>{{ order.customer_email }}</td>
              <td class="chrome-text">${{ formatNumber(order.total_amount) }}</td>
              <td><span :class="`status-badge status-${order.status}`">{{ order.status }}</span></td>
              <td>{{ formatDate(order.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Line, Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import apiClient from '@/api/client'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

// State
const loading = ref(true)
const startDate = ref('')
const endDate = ref('')
const stats = ref({
  total_sales: 0,
  total_orders: 0,
  total_users: 0,
  new_users: 0,
  avg_order_value: 0
})
const salesData = ref([])
const statusData = ref([])
const topProducts = ref([])
const topArtists = ref([])
const recentOrders = ref([])

// Y2K Color Palette
const colors = {
  chrome: '#c0c0c0',
  steel: '#6a6a6a',
  iron: '#4a4a4a',
  concrete: '#95a5a6',
  graphite: '#3d3d3d'
}

// Clear filters
const clearFilters = () => {
  startDate.value = ''
  endDate.value = ''
  fetchData()
}

// Fetch all dashboard data
const fetchData = async () => {
  loading.value = true
  const params = {}
  if (startDate.value) params.start_date = startDate.value
  if (endDate.value) params.end_date = endDate.value

  try {
    // Fetch dashboard stats
    const statsRes = await apiClient.get('/analytics/dashboard-stats', { params })
    stats.value = statsRes.data

    // Fetch sales over time
    const salesRes = await apiClient.get('/analytics/sales-over-time', {
      params: { ...params, interval: 'day' }
    })
    salesData.value = salesRes.data.data

    // Fetch status breakdown
    const statusRes = await apiClient.get('/analytics/order-status-breakdown', { params })
    statusData.value = statusRes.data.statuses

    // Fetch top products
    const productsRes = await apiClient.get('/analytics/top-products', {
      params: { ...params, limit: 5 }
    })
    topProducts.value = productsRes.data.products

    // Fetch top artists
    const artistsRes = await apiClient.get('/analytics/top-artists', {
      params: { ...params, limit: 5 }
    })
    topArtists.value = artistsRes.data.artists

    // Fetch recent orders
    const ordersRes = await apiClient.get('/analytics/recent-orders', {
      params: { limit: 10 }
    })
    recentOrders.value = ordersRes.data.orders
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    alert('Error loading dashboard data. Make sure the backend is running!')
  } finally {
    loading.value = false
  }
}

// Chart Data
const salesChartData = computed(() => ({
  labels: salesData.value.map(d => d.period),
  datasets: [{
    label: 'Sales ($)',
    data: salesData.value.map(d => d.total_sales),
    borderColor: colors.chrome,
    backgroundColor: colors.chrome + '40',
    tension: 0.1,
    fill: true
  }]
}))

const statusChartData = computed(() => {
  // Map status names to their corresponding colors
  const statusColors = {
    'paid': '#c0ffc0',        // Light Chrome Green
    'pending': '#ffff80',     // Chrome Yellow
    'processing': '#8080ff',  // Chrome Blue
    'shipped': '#ffb380',     // Chrome Orange
    'delivered': '#80ff80',   // Bright Chrome Green
    'cancelled': '#ff8080',   // Chrome Red
    'refunded': '#ff66cc'     // Chrome Pink
  }

  return {
    labels: statusData.value.map(d => d.status),
    datasets: [{
      data: statusData.value.map(d => d.count),
      backgroundColor: statusData.value.map(d => statusColors[d.status] || '#808080'),
      borderWidth: 2,
      borderColor: '#1a1a1a'
    }]
  }
})

const productsChartData = computed(() => ({
  labels: topProducts.value.map(p => p.name),
  datasets: [{
    label: 'Revenue ($)',
    data: topProducts.value.map(p => p.revenue),
    backgroundColor: colors.steel,
    borderColor: colors.steel,
    borderWidth: 1
  }]
}))

const artistsChartData = computed(() => ({
  labels: topArtists.value.map(a => a.name),
  datasets: [{
    label: 'Revenue ($)',
    data: topArtists.value.map(a => a.revenue),
    backgroundColor: colors.concrete,
    borderColor: colors.concrete,
    borderWidth: 1
  }]
}))

// Chart Options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#fff',
        font: {
          family: 'Space Grotesk, sans-serif',
          size: 14
        }
      }
    }
  },
  scales: {
    y: {
      ticks: {
        color: '#fff',
        font: {
          family: 'Space Grotesk, sans-serif'
        }
      },
      grid: { color: '#ffffff20' }
    },
    x: {
      ticks: {
        color: '#fff',
        font: {
          family: 'Space Grotesk, sans-serif'
        }
      },
      grid: { color: '#ffffff20' }
    }
  }
}

const barOptions = {
  ...chartOptions,
  indexAxis: 'y'
}

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        color: '#fff',
        font: {
          family: 'Space Grotesk, sans-serif',
          size: 14
        }
      }
    }
  }
}

// Export Functions
const exportOrders = () => {
  const params = new URLSearchParams()
  if (startDate.value) params.append('start_date', startDate.value)
  if (endDate.value) params.append('end_date', endDate.value)

  const url = `${apiClient.defaults.baseURL}/exports/orders?${params.toString()}`
  window.open(url, '_blank')
}

const exportUsers = () => {
  const url = `${apiClient.defaults.baseURL}/exports/users`
  window.open(url, '_blank')
}

const exportProducts = () => {
  const url = `${apiClient.defaults.baseURL}/exports/products`
  window.open(url, '_blank')
}

const exportArtistSales = () => {
  const params = new URLSearchParams()
  if (startDate.value) params.append('start_date', startDate.value)
  if (endDate.value) params.append('end_date', endDate.value)

  const url = `${apiClient.defaults.baseURL}/exports/artist-sales?${params.toString()}`
  window.open(url, '_blank')
}

// Utilities
const formatNumber = (num) => {
  return Number(num || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.admin-dashboard {
  padding: var(--space-xl);
  max-width: 1600px;
  margin: 0 auto;
  min-height: 100vh;
}

.loading {
  text-align: center;
  padding: var(--space-3xl);
  font-size: 1.5rem;
}

.dashboard-filters {
  display: flex;
  gap: var(--space-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
  align-items: flex-end;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.filter-group label {
  font-weight: bold;
  color: var(--color-chrome);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.filter-group .input {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-steel);
  background: rgba(0, 0, 0, 0.7);
  color: var(--color-chrome);
  font-family: 'Arial', sans-serif;
}

.filter-group .input:focus {
  border-color: var(--color-chrome);
  outline: none;
  box-shadow: 0 0 0 2px rgba(192, 192, 192, 0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.stat-card {
  padding: var(--space-xl);
  text-align: center;
}

.stat-card h3 {
  font-size: 1.2rem;
  margin-bottom: var(--space-md);
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  margin: var(--space-md) 0;
  font-family: 'Orbitron', sans-serif;
}

.stat-sub {
  color: var(--color-concrete);
  font-size: 1.2rem;
  margin-top: var(--space-sm);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.chart-container {
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
}

.chart-container h3 {
  margin-bottom: var(--space-lg);
  color: var(--color-chrome);
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 700;
}

.chart-wrapper {
  flex: 1;
  min-height: 300px;
  max-height: 400px;
  position: relative;
}

.no-data {
  text-align: center;
  padding: var(--space-3xl);
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.export-section {
  margin: var(--space-xl) 0;
  padding: var(--space-xl);
}

.export-section h3 {
  margin-bottom: var(--space-lg);
  color: var(--color-chrome);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 700;
}

.export-buttons {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.recent-orders {
  padding: var(--space-xl);
}

.recent-orders h3 {
  margin-bottom: var(--space-lg);
  color: var(--color-chrome);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 700;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: var(--space-md);
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  color: var(--color-chrome);
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

tbody tr {
  transition: all var(--transition-base);
}

tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(5px);
}

.status-badge {
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: bold;
  text-transform: uppercase;
  display: inline-block;
}

.status-paid { background: var(--color-paid); color: black; }
.status-pending { background: var(--color-pending); color: black; }
.status-processing { background: var(--color-processing); color: white; }
.status-shipped { background: var(--color-shipped); color: white; }
.status-delivered { background: var(--color-delivered); color: black; }
.status-cancelled { background: var(--color-cancelled); color: white; }
.status-refunded { background: var(--color-refunded); color: white; }

/* Brutalist Chrome Styling */
.chrome-title {
  font-size: var(--font-5xl);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 4px;
  background: var(--gradient-metallic);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--space-2xl);
  font-family: 'Arial Black', sans-serif;
}

.chrome-text {
  color: var(--color-chrome);
  letter-spacing: 1px;
  font-weight: 700;
}

.chrome-card {
  background: var(--bg-card);
  border: 1px solid var(--color-iron);
  box-shadow: var(--shadow-steel);
  transition: all var(--transition-base);
}

.chrome-card:hover {
  border-color: var(--color-chrome);
  box-shadow: var(--shadow-metallic);
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: 1fr;
  }

  .chart-wrapper {
    max-height: 350px;
  }
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: var(--space-md);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .stat-value {
    font-size: 2rem;
  }

  .chart-wrapper {
    max-height: 300px;
  }

  .dashboard-filters {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
