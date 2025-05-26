<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title
} from 'chart.js'

ChartJS.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend, Title)

export default {
  name: 'AgeDistributionChart',
  data() {
    return {
      chart: null,
      chartData: {
        labels: ['18–24', '25–34', '35–44', '45–54', '55–64', '65+'],
        datasets: [
          {
            label: 'Users',
            data: [150, 300, 220, 180, 100, 60],
            backgroundColor: [
              '#FF6F61',
              '#FFA07A',
              '#FF8C42',
              '#FFD166',
              '#E29578',
              '#F4A261'
            ],
            borderRadius: 6,
            barThickness: 40
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'User Age Distribution',
            font: {
              size: 18
            }
          },
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => ` ${context.raw} users`
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Age Groups'
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Users'
            },
            ticks: {
              stepSize: 50
            }
          }
        }
      }
    }
  },
  mounted() {
    const ctx = this.$refs.canvas.getContext('2d')
    this.chart = new ChartJS(ctx, {
      type: 'bar',
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
