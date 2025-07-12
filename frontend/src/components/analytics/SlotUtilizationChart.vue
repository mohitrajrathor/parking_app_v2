<template>
  <div class="p-4 bg-white rounded-xl">
    <h4 class="text-xl font-semibold mb-4">Slot Utilization</h4>
    <canvas ref="slotChartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(DoughnutController, ArcElement, Tooltip, Legend)

const props = defineProps({
  totalSlots: { type: Number, required: true },
  bookedSlots: { type: Number, required: true },
  themeColor: { type: String, default: '#0d6efd' }
})

const slotChartCanvas = ref(null)
let slotChartInstance = null

const renderChart = () => {
  const availableSlots = props.totalSlots - props.bookedSlots

  const data = {
    labels: ['Booked Slots', 'Available Slots'],
    datasets: [
      {
        data: [props.bookedSlots, availableSlots],
        backgroundColor: [props.themeColor, '#E5E7EB'], // Theme and Gray
        borderWidth: 0,
      },
    ],
  }

  const options = {
    responsive: true,
    cutout: '70%',
    rotation: -90,
    circumference: 180,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#374151',
        },
      },
      tooltip: {
        callbacks: {
          label: context => `${context.label}: ${context.parsed} slots`
        }
      },
    },
  }

  if (slotChartInstance) slotChartInstance.destroy()

  slotChartInstance = new Chart(slotChartCanvas.value, {
    type: 'doughnut',
    data,
    options,
  })
}

onMounted(renderChart)
watch(() => [props.bookedSlots, props.totalSlots], renderChart)
</script>

<style scoped>
canvas {
  width: 100%;
  max-height: 250px;
  background: #fff;
  border-radius: 1rem;
}
</style>
