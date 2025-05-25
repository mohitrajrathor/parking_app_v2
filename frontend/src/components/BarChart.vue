<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script>
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

// Register required chart.js modules
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

export default {
  name: 'ParkingChart',
  components: { Bar },
  data() {
    return {
      // You can fetch this from an API later
      parkingData: [
        { time: '9 AM', total: 100, used: 40 },
        { time: '10 AM', total: 100, used: 60 },
        { time: '11 AM', total: 100, used: 80 },
        { time: '12 PM', total: 100, used: 70 }
      ]
    }
  },
  computed: {
    chartData() {
      return {
        labels: this.parkingData.map(d => d.time),
        datasets: [
          {
            label: 'Used Lots',
            data: this.parkingData.map(d => d.used),
            backgroundColor: '#F44336', // Red
            stack: 'stack1'
          },
          {
            label: 'Free Lots',
            data: this.parkingData.map(d => d.total - d.used),
            backgroundColor: '#E0E0E0', // Gray
            stack: 'stack1'
          }
        ]
      }
    },
    chartOptions() {
      const max = Math.max(...this.parkingData.map(d => d.total))
      return {
        backgroundColor: {
          color: '#e3f2fd' // light blue background
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top'
          },
          title: {
            display: true,
            text: 'Parking Lot Usage Over Time', // 🔹 Your Chart Title
            font: {
              size: 18,
              weight: 'bold'
            },
            padding: {
              top: 10,
              bottom: 20
            }
          },
          tooltip: {
            callbacks: {
              label: context => `${context.dataset.label}: ${context.raw}`
            }
          }
        },
        scales: {
          x: { stacked: true },
          y: {
            stacked: true,
            beginAtZero: true,
            max: max
          }
        }
      }
    }

  }
}
</script>

<style scoped>
/* Optional: to make the chart taller */
canvas {
  height: 300px !important;
}
</style>
