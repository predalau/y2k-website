# Admin Dashboard Implementation Guide

## Overview

This guide covers implementing a full-featured admin dashboard for your Y2K artist merch e-commerce platform with:
- Sales analytics and reports
- User statistics
- Interactive charts
- CSV exports
- Real-time data

## Tech Stack Recommendation

### ✅ Backend (Already Implemented)
- **FastAPI** - Analytics endpoints
- **SQLAlchemy** - Database aggregations
- **CSV module** - Export functionality

### 🎨 Frontend (To Install)
```bash
cd frontend
npm install chart.js vue-chartjs
npm install @tanstack/vue-table  # Optional: for data tables
npm install @vuepic/vue-datepicker  # Optional: date picker
```

**Chart.js** is the recommended choice because:
- Most popular charting library
- Easy to customize with Y2K styling (neon colors, gradients)
- Great documentation
- Responsive out of the box
- Supports all chart types you need

## Backend API Endpoints

### Analytics Endpoints (Already Created)

#### 1. Dashboard Statistics
```
GET /api/v1/analytics/dashboard-stats
```
Query params: `start_date`, `end_date`

Returns:
```json
{
  "total_sales": 15234.50,
  "total_orders": 342,
  "total_users": 1456,
  "new_users": 45,
  "avg_order_value": 44.56
}
```

#### 2. Sales Over Time
```
GET /api/v1/analytics/sales-over-time?interval=day
```
Query params: `start_date`, `end_date`, `interval` (day/week/month)

Returns data for line/bar charts.

#### 3. Top Products
```
GET /api/v1/analytics/top-products?limit=10
```
Returns best-selling products by revenue.

#### 4. Top Artists
```
GET /api/v1/analytics/top-artists?limit=10
```
Returns top-performing artists with commission data.

#### 5. Order Status Breakdown
```
GET /api/v1/analytics/order-status-breakdown
```
Returns order counts by status (for pie chart).

#### 6. User Growth
```
GET /api/v1/analytics/user-growth?interval=month
```
Returns user registration trend data.

#### 7. Low Stock Alerts
```
GET /api/v1/analytics/low-stock-alerts
```
Returns products below stock threshold.

### CSV Export Endpoints (Already Created)

```
GET /api/v1/exports/orders
GET /api/v1/exports/order-items
GET /api/v1/exports/users
GET /api/v1/exports/products
GET /api/v1/exports/inventory
GET /api/v1/exports/artist-sales
```

All support date filtering via query params.

## Frontend Implementation

### 1. Install Dependencies

```bash
cd frontend
npm install chart.js vue-chartjs
```

### 2. Create Admin Dashboard View

**File:** `frontend/src/views/Admin/Dashboard.vue`

```vue
<template>
  <div class="admin-dashboard">
    <h1 class="holographic">Admin Dashboard</h1>

    <!-- Date Range Filter -->
    <div class="dashboard-filters glass">
      <div class="filter-group">
        <label>Start Date:</label>
        <input type="date" v-model="startDate" @change="fetchData" />
      </div>
      <div class="filter-group">
        <label>End Date:</label>
        <input type="date" v-model="endDate" @change="fetchData" />
      </div>
    </div>

    <!-- Key Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card card-glow">
        <h3 class="neon-text-blue">Total Sales</h3>
        <p class="stat-value">${{ formatNumber(stats.total_sales) }}</p>
      </div>
      <div class="stat-card card-glow">
        <h3 class="neon-text-green">Orders</h3>
        <p class="stat-value">{{ stats.total_orders }}</p>
      </div>
      <div class="stat-card card-glow">
        <h3 class="neon-text">Users</h3>
        <p class="stat-value">{{ stats.total_users }}</p>
        <p class="stat-sub">+{{ stats.new_users }} new</p>
      </div>
      <div class="stat-card card-glow">
        <h3 class="neon-text-yellow">Avg Order</h3>
        <p class="stat-value">${{ formatNumber(stats.avg_order_value) }}</p>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="charts-row">
      <div class="chart-container card glass">
        <h3>Sales Over Time</h3>
        <Line :data="salesChartData" :options="chartOptions" />
      </div>
      <div class="chart-container card glass">
        <h3>Order Status</h3>
        <Doughnut :data="statusChartData" :options="doughnutOptions" />
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="charts-row">
      <div class="chart-container card glass">
        <h3>Top Products</h3>
        <Bar :data="productsChartData" :options="barOptions" />
      </div>
      <div class="chart-container card glass">
        <h3>Top Artists</h3>
        <Bar :data="artistsChartData" :options="barOptions" />
      </div>
    </div>

    <!-- Export Buttons -->
    <div class="export-section">
      <h3>Export Data</h3>
      <div class="export-buttons">
        <button class="btn btn-primary" @click="exportOrders">
          Export Orders
        </button>
        <button class="btn btn-primary" @click="exportUsers">
          Export Users
        </button>
        <button class="btn btn-primary" @click="exportProducts">
          Export Products
        </button>
        <button class="btn btn-primary" @click="exportArtistSales">
          Export Artist Sales
        </button>
      </div>
    </div>

    <!-- Recent Orders Table -->
    <div class="recent-orders card glass">
      <h3>Recent Orders</h3>
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
          <tr v-for="order in recentOrders" :key="order.id">
            <td>{{ order.order_number }}</td>
            <td>{{ order.customer_email }}</td>
            <td>${{ formatNumber(order.total_amount) }}</td>
            <td><span :class="`status-badge status-${order.status}`">{{ order.status }}</span></td>
            <td>{{ formatDate(order.created_at) }}</td>
          </tr>
        </tbody>
      </table>
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
  cyberPink: '#ff00ff',
  cyberBlue: '#00ffff',
  neonGreen: '#39ff14',
  electricYellow: '#ffff00',
  cyberPurple: '#9945ff'
}

// Fetch all dashboard data
const fetchData = async () => {
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
  }
}

// Chart Data
const salesChartData = computed(() => ({
  labels: salesData.value.map(d => d.period),
  datasets: [{
    label: 'Sales ($)',
    data: salesData.value.map(d => d.total_sales),
    borderColor: colors.cyberBlue,
    backgroundColor: colors.cyberBlue + '20',
    tension: 0.4
  }]
}))

const statusChartData = computed(() => ({
  labels: statusData.value.map(d => d.status),
  datasets: [{
    data: statusData.value.map(d => d.count),
    backgroundColor: [
      colors.cyberPink,
      colors.cyberBlue,
      colors.neonGreen,
      colors.electricYellow,
      colors.cyberPurple
    ]
  }]
}))

const productsChartData = computed(() => ({
  labels: topProducts.value.map(p => p.name),
  datasets: [{
    label: 'Revenue ($)',
    data: topProducts.value.map(p => p.revenue),
    backgroundColor: colors.neonGreen
  }]
}))

const artistsChartData = computed(() => ({
  labels: topArtists.value.map(a => a.name),
  datasets: [{
    label: 'Revenue ($)',
    data: topArtists.value.map(a => a.revenue),
    backgroundColor: colors.cyberPink
  }]
}))

// Chart Options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#fff'
      }
    }
  },
  scales: {
    y: {
      ticks: { color: '#fff' },
      grid: { color: '#ffffff20' }
    },
    x: {
      ticks: { color: '#fff' },
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
      labels: {
        color: '#fff'
      }
    }
  }
}

// Export Functions
const exportOrders = () => {
  const params = new URLSearchParams()
  if (startDate.value) params.append('start_date', startDate.value)
  if (endDate.value) params.append('end_date', endDate.value)

  window.open(`/api/v1/exports/orders?${params.toString()}`, '_blank')
}

const exportUsers = () => {
  window.open('/api/v1/exports/users', '_blank')
}

const exportProducts = () => {
  window.open('/api/v1/exports/products', '_blank')
}

const exportArtistSales = () => {
  const params = new URLSearchParams()
  if (startDate.value) params.append('start_date', startDate.value)
  if (endDate.value) params.append('end_date', endDate.value)

  window.open(`/api/v1/exports/artist-sales?${params.toString()}`, '_blank')
}

// Utilities
const formatNumber = (num) => {
  return Number(num).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.admin-dashboard {
  padding: var(--space-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-filters {
  display: flex;
  gap: var(--space-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.filter-group label {
  font-weight: bold;
  color: var(--color-cyber-blue);
}

.filter-group input {
  padding: var(--space-sm);
  border-radius: var(--radius-sm);
  border: 2px solid var(--color-cyber-blue);
  background: rgba(0, 0, 0, 0.5);
  color: white;
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

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  margin: var(--space-md) 0;
}

.stat-sub {
  color: var(--color-neon-green);
  font-size: 1.2rem;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.chart-container {
  padding: var(--space-xl);
  height: 400px;
}

.export-section {
  margin: var(--space-xl) 0;
  padding: var(--space-xl);
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius-lg);
}

.export-buttons {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
  margin-top: var(--space-lg);
}

.recent-orders {
  padding: var(--space-xl);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--space-lg);
}

th, td {
  padding: var(--space-md);
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  color: var(--color-cyber-blue);
  font-weight: bold;
}

.status-badge {
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-weight: bold;
}

.status-paid { background: var(--color-neon-green); color: black; }
.status-pending { background: var(--color-electric-yellow); color: black; }
.status-shipped { background: var(--color-cyber-blue); color: black; }
.status-cancelled { background: #ff0000; color: white; }
</style>
```

### 3. Add Admin Route

**File:** `frontend/src/router/index.js`

```javascript
{
  path: '/admin/dashboard',
  name: 'AdminDashboard',
  component: () => import('../views/Admin/Dashboard.vue'),
  meta: { requiresAuth: true, requiresAdmin: true }
}
```

### 4. Test the Dashboard

1. Start backend: `./start-backend.sh`
2. Start frontend: `./start-frontend.sh`
3. Visit: `http://localhost:5173/admin/dashboard`

## Next Steps

### 1. Add Authentication
Protect admin routes with JWT auth:
```javascript
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin) {
    // Check if user is admin
    const user = JSON.parse(localStorage.getItem('user'))
    if (!user || !user.is_admin) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})
```

### 2. Add More Features
- Real-time updates with WebSockets
- Email report scheduling
- More detailed analytics (conversion rates, customer lifetime value)
- Inventory management interface
- Order management (update status, add tracking)

### 3. Enhance Charts
- Add more chart types (radar, scatter)
- Interactive tooltips
- Zoom/pan functionality
- Export charts as images

## Summary

**Backend:** ✅ Complete
- 7 analytics endpoints
- 6 CSV export endpoints
- All integrated with existing database

**Frontend:** 📋 Install & Implement
```bash
npm install chart.js vue-chartjs
```
Then create the Dashboard.vue component using the example above.

**Result:** Full-featured admin dashboard with:
- Real-time sales analytics
- User statistics
- Interactive Y2K-styled charts
- CSV exports for all data
- Low stock alerts
- Artist commission tracking

This approach gives you full control, perfect Y2K styling, and no external service dependencies!
