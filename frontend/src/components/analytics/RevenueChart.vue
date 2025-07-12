<template>
  <div class="p-4 bg-white rounded-xl w-full">
    <h4 class="text-xl font-semibold mb-4">Daily Revenue (Last 30 Days)</h4>
    <div class="relative w-full h-[300px]">
      <canvas ref="revenueChartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {
  Chart,
  registerables
} from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  dailyRevenue: {
    type: Object,
    required: true
  }
})

const revenueChartCanvas = ref(null)
let revenueChartInstance = null

const renderChart = () => {
  const labels = Object.keys(props.dailyRevenue)
  const data = Object.values(props.dailyRevenue)

  if (revenueChartInstance) {
    revenueChartInstance.destroy()
  }

  revenueChartInstance = new Chart(revenueChartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Revenue (₹)',
          data,
          fill: true,
          borderColor: 'rgba(59, 130, 246, 1)',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          tension: 0.3,
          pointRadius: 3,
          pointBackgroundColor: 'rgba(59, 130, 246, 1)'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            maxTicksLimit: 10,
            color: '#4B5563'
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: '#4B5563'
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#374151'
          }
        },
        tooltip: {
          callbacks: {
            label: context => `₹ ${context.parsed.y}`
          }
        }
      }
    }
  })
}

onMounted(() => {
  renderChart()
})

// Re-render chart if prop changes
watch(() => props.dailyRevenue, renderChart, { deep: true })
</script>

<style scoped>
canvas {
  width: 100%;
  height: 100%;
}
</style>
