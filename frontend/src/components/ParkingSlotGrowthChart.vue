<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'ParkingSlotTrendChart',
  data() {
    return {
      chart: null,
      chartData: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        datasets: [
          {
            label: 'Parking Slots Available',
            data: [100, 120, 140, 160, 180, 200, 220, 240],
            borderColor: '#F9A825', // Warm Yellow
            backgroundColor: 'rgba(249, 168, 37, 0.2)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#F9A825'
          },
          {
            label: 'Slots Booked',
            data: [20, 35, 50, 65, 85, 100, 120, 150],
            borderColor: '#E64A19', // Deep Orange
            backgroundColor: 'rgba(230, 74, 25, 0.2)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#E64A19'
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top'
          },
          title: {
            display: true,
            text: 'Parking Slot Trends Over Time',
            font: {
              size: 18
            }
          },
          tooltip: {
            callbacks: {
              label: context => ` ${context.dataset.label}: ${context.raw}`
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Month'
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Slots'
            },
            ticks: {
              stepSize: 20
            }
          }
        }
      }
    }
  },
  mounted() {
    const ctx = this.$refs.canvas.getContext('2d')
    this.chart = new ChartJS(ctx, {
      type: 'line',
      data: this.chartData,
      options: this.chartOptions
    })
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 450px;
}
</style>
