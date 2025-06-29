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

// Dummy data for user growth
const chartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
  datasets: [
    {
      label: 'Users',
      data: [50, 80, 120, 180, 250, 320, 400],
      borderColor: '#1976d2',
      backgroundColor: 'rgba(25, 118, 210, 0.2)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#42a5f5',
      pointBorderColor: '#1976d2',
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
        color: '#1976d2',
        font: {
          size: 14,
          weight: 'bold',
        },
      },
    },
    title: {
      display: true,
      text: 'User Growth Over Time',
      color: '#1976d2',
      font: {
        size: 18,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#1976d2',
      },
      grid: {
        display: false,
      },
    },
    y: {
      ticks: {
        color: '#1976d2',
      },
      grid: {
        color: 'rgba(25, 118, 210, 0.1)',
      },
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
  padding: 1rem;
  background-color: #e3f2fd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}
</style>
