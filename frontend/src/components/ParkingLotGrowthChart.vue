<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';
import { Line } from 'vue-chartjs';

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

// Dummy data
const chartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
  datasets: [
    {
      label: 'Parking Lots',
      data: [5, 10, 12, 20, 25, 30, 38],
      borderColor: '#ff6f00',
      backgroundColor: 'rgba(255, 111, 0, 0.3)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#ff9100',
      pointBorderColor: '#ff6f00',
    },
  ],
};

// Chart appearance and responsiveness
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#ff6f00',
        font: {
          size: 14,
          weight: 'bold',
        },
      },
    },
    title: {
      display: true,
      text: 'Parking Lot Growth Over Time',
      color: '#ff6f00',
      font: {
        size: 18,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#ff6f00',
      },
      grid: {
        display: false,
      },
    },
    y: {
      ticks: {
        color: '#ff6f00',
      },
      grid: {
        color: 'rgba(255, 111, 0, 0.2)',
      },
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  padding: 1rem;
  background-color: #fff3e0;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(255, 167, 38, 0.3);
}
</style>
