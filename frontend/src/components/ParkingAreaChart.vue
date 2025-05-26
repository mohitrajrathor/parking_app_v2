<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js'

ChartJS.register(DoughnutController, ArcElement, Tooltip, Legend, Title)

export default {
  name: 'UrbanRuralParkingChart',
  data() {
    return {
      chart: null,
      chartData: {
        labels: ['Urban Parking', 'Rural Parking'],
        datasets: [
          {
            label: 'Parking Distribution',
            data: [350, 150],
            backgroundColor: ['#FF7043', '#FDD835'], // Warm coral and amber
            hoverOffset: 10
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        rotation: -90,         // Start at the top
        circumference: 180,    // Half circle
        plugins: {
          title: {
            display: true,
            text: 'Urban vs Rural Parking Areas',
            font: {
              size: 18
            }
          },
          legend: {
            position: 'bottom'
          },
          tooltip: {
            callbacks: {
              label: context => `${context.label}: ${context.raw} slots`
            }
          }
        }
      }
    }
  },
  mounted() {
    const ctx = this.$refs.canvas.getContext('2d')
    this.chart = new ChartJS(ctx, {
      type: 'doughnut',
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
  height: 300px;
}
</style>
