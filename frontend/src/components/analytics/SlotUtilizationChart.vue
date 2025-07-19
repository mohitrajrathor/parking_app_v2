<template>
  <div class="card border-0 rounded-4 bg-white">
    <div class="card-body">
      <h4 class="card-title fw-bold mb-3 text-black">Slot Utilization</h4>
      <div class="d-flex justify-content-center align-items-center">
        <canvas ref="slotChartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Chart, ArcElement, Tooltip, Legend, Title } from 'chart.js';
Chart.register(ArcElement, Tooltip, Legend, Title);

const props = defineProps({
  totalSlots: { type: Number, required: true },
  bookedSlots: { type: Number, required: true },
  themeColor: { type: String, default: '#0d6efd' }
});

const slotChartCanvas = ref(null);
let slotChartInstance = null;

const renderChart = () => {
  const availableSlots = props.totalSlots - props.bookedSlots;
  if (slotChartInstance) slotChartInstance.destroy();
  slotChartInstance = new Chart(slotChartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Booked Slots', 'Available Slots'],
      datasets: [
        {
          data: [props.bookedSlots, availableSlots],
          backgroundColor: [props.themeColor, '#E5E7EB'],
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
          text: 'Slot Utilization',
          color: '#000',
          font: { size: 18, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.label}: ${ctx.raw} slots`
          }
        }
      }
    }
  });
};

onMounted(renderChart);
watch(() => [props.bookedSlots, props.totalSlots], renderChart);
</script>

<style scoped>
canvas {
  width: 100%;
  max-height: 220px;
  background: #fff;
  border-radius: 1rem;
}
</style>
