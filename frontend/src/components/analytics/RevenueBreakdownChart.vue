<template>
  <div class="card border-0 rounded-4 bg-white">
    <div class="card-body">
      <h4 class="card-title fw-bold mb-3 text-black">Spending Breakdown</h4>
      <div class="d-flex justify-content-center align-items-center">
        <canvas ref="donutChartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Chart, ArcElement, Tooltip, Legend, Title } from 'chart.js';
Chart.register(ArcElement, Tooltip, Legend, Title);

const props = defineProps({
  bookingRevenue: { type: Number, required: true },
  leaveRevenue: { type: Number, required: true },
  themeColor: { type: String, default: '#0d6efd' }
});

const donutChartCanvas = ref(null);
let chartInstance = null;

const createDonutChart = () => {
  const booking = props.bookingRevenue ?? 0;
  const leaving = props.leaveRevenue ?? 0;
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(donutChartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Booking', 'Leaving'],
      datasets: [
        {
          label: 'Revenue',
          data: [booking, leaving],
          backgroundColor: [props.themeColor, '#ffc107'],
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      rotation: -90,
      circumference: 180,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#000', font: { weight: 'bold' } }
        },
        title: {
          display: false,
          text: 'Revenue Breakdown',
          color: '#000',
          font: { size: 18, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: ctx => `₹ ${ctx.raw}`
          }
        }
      }
    }
  });
};

onMounted(createDonutChart);
watch(() => [props.bookingRevenue, props.leaveRevenue], createDonutChart);
</script>

<style scoped>
canvas {
  width: 100%;
  max-height: 220px;
  background: #fff;
  border-radius: 1rem;
}
</style>
