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
  name: 'ProfessionDistributionChart',
  data() {
    return {
      chart: null,
      chartData: {
        labels: ['Developer', 'Designer', 'Marketer', 'Manager', 'Sales', 'Other'],
        datasets: [
          {
            label: 'Profession Distribution',
            data: [300, 180, 120, 90, 110, 70],
            backgroundColor: [
              '#F94144', // red
              '#F3722C', // orange
              '#F9C74F', // yellow
              '#F9844A', // coral
              '#F8961E', // tangerine
              '#FBCB7E'  // peach
            ],
            borderWidth: 1,
            hoverOffset: 12
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
            text: 'User Profession Distribution',
            font: {
              size: 18
            }
          },
          tooltip: {
            callbacks: {
              label: context => ` ${context.label}: ${context.raw} users`
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
  height: 400px;
}
</style>
