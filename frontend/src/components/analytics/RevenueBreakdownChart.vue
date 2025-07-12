<template>
  <div class="p-4 bg-white rounded-xl">
    <h4 class="text-xl font-semibold mb-4">Revenue Breakdown</h4>
    <canvas ref="donutChartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  bookingRevenue: { type: Number, required: true },
  totalRevenue: { type: Number, required: true },
  themeColor: { type: String, default: '#0d6efd' }
})

const donutChartCanvas = ref(null)
let chartInstance = null

const createDonutChart = () => {
  const leavingRevenue = props.totalRevenue - props.bookingRevenue

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(donutChartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Booking', 'Leaving'],
      datasets: [
        {
          label: 'Revenue',
          data: [props.bookingRevenue, leavingRevenue],
          backgroundColor: [props.themeColor, '#ffc107'], // Theme and yellow
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      rotation: -90,           // Start from top
      circumference: 180,      // Half circle
      cutout: '70%',           // Inner radius for donut
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#374151' }
        },
        tooltip: {
          callbacks: {
            label: ctx => `₹ ${ctx.raw}`
          }
        }
      }
    }
  })
}

onMounted(createDonutChart)
watch(() => [props.bookingRevenue, props.totalRevenue], createDonutChart)
</script>

<style scoped>
canvas {
  width: 100%;
  max-height: 250px;
  background: #fff;
  border-radius: 1rem;
}
</style>
