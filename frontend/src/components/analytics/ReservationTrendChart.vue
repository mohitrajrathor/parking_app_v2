<template>
  <div class="bg-white rounded-4">
    <h4 class="fs-5 fw-semibold mb-4 text-dark">Daily Reservation Trend</h4>
    <div class="w-100" style="height:300px">
      <canvas ref="reservationChartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  dailyReservations: {
    type: Object,
    required: true
  },
  themeColor: {
    type: String,
    default: '#0d6efd' // Project theme color
  }
})

const reservationChartCanvas = ref(null)
let reservationChartInstance = null

const renderChart = () => {
  const reservationsObj = props.dailyReservations || {};
  const labels = Object.keys(reservationsObj);
  const data = Object.values(reservationsObj);

  if (!labels.length) {
    // No data, clear chart
    if (reservationChartInstance) {
      reservationChartInstance.destroy();
      reservationChartInstance = null;
    }
    return;
  }

  if (reservationChartInstance) {
    reservationChartInstance.destroy();
  }

  reservationChartInstance = new Chart(reservationChartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Reservations',
        data,
        borderColor: props.themeColor,
        backgroundColor: props.themeColor + '33', // 20% opacity
        fill: true,
        tension: 0.35,
        pointRadius: 3,
        pointBackgroundColor: props.themeColor
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: '#4B5563' } // theme gray
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#4B5563' }
        }
      },
      plugins: {
        legend: {
          labels: { color: '#374151' }
        },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.parsed.y} reservations`
          }
        }
      }
    }
  })
}

watch(() => props.dailyReservations, renderChart, { deep: true })
onMounted(renderChart)
</script>

<style scoped>
canvas {
  width: 100%;
  height: 100%;
  background: #fff;
  border-radius: 1rem;
}
</style>
