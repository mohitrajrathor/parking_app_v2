<template>
  <div class="chart-container bg-white rounded-4 p-4 mb-4">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import { computed } from 'vue';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const props = defineProps({
  ageDist: {
    type: Object,
    required: true
  }
});

const chartData = computed(() => {
  const labels = Object.keys(props.ageDist);
  const data = Object.values(props.ageDist);
  return {
    labels,
    datasets: [
      {
        label: 'User Count',
        data,
        backgroundColor: '#6ea8fe',
        borderColor: '#0d6efd',
        borderWidth: 2,
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
      text: 'User Age Distribution',
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
        text: 'Age Group',
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
        text: 'User Count',
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
