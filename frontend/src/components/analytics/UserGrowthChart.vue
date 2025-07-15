<template>
  <div class="chart-container bg-white rounded-4 p-4 mb-4">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Line } from 'vue-chartjs';
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
import { computed } from 'vue';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

const props = defineProps({
  monthlyGrowth: {
    type: Object,
    required: true
  }
});

const chartData = computed(() => {
  const labels = Object.keys(props.monthlyGrowth);
  const data = Object.values(props.monthlyGrowth);
  return {
    labels,
    datasets: [
      {
        label: 'Users Joined',
        data,
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13,110,253,0.2)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#6ea8fe',
        pointBorderColor: '#0d6efd',
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#000',
        font: {
          size: 14,
          weight: 'bold',
        },
      },
    },
    title: {
      display: true,
      text: 'User Growth (Last 12 Months)',
      color: '#000',
      font: {
        size: 18,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#000',
      },
      grid: {
        display: false,
      },
      title: {
        display: true,
        text: 'Month',
        color: '#000',
        font: {
          weight: 'bold'
        }
      }
    },
    y: {
      ticks: {
        color: '#000',
      },
      grid: {
        color: 'rgba(13,110,253,0.1)',
      },
      title: {
        display: true,
        text: 'Users Joined',
        color: '#000',
        font: {
          weight: 'bold'
        }
      }
    }
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
  background-color: #fff;
  border-radius: 1rem;
}
</style>
