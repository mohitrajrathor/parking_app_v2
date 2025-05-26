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
  name: 'ParkingDemandChart',
  data() {
    return {
      chart: null,
      chartData: {
        labels: [
          'Early Morning',
          'Morning Rush',
          'Midday',
          'Afternoon',
          'Evening Rush',
          'Night'
        ],
        datasets: [
          {
            label: 'Parking Demand',
            data: [40, 120, 80, 60, 150, 70],
            backgroundColor: [
              '#FFB74D', // Warm Orange
              '#FF7043', // Coral
              '#FDD835', // Amber
              '#FF8A65', // Light Coral
              '#F4511E', // Deep Orange
              '#F9A825'  // Golden Yellow
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
            text: 'Time of Day vs Parking Demand',
            font: {
              size: 18
            }
          },
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: context => ` ${context.label}: ${context.raw} vehicles`
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time of Day'
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Parking Demand'
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
  height: 450px;
}
</style>
