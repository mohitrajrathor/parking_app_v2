<template>
  <div class="chart-container bg-white rounded-4 p-4 mb-4">
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from 'chart.js';
import { computed } from 'vue';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const props = defineProps({
  professionDist: {
    type: Object,
    required: true
  }
});

const chartData = computed(() => {
  const labels = Object.keys(props.professionDist);
  const data = Object.values(props.professionDist);
  return {
    labels,
    datasets: [
      {
        label: 'Profession Distribution',
        data,
        backgroundColor: [
          '#0d6efd',
          '#6ea8fe',
          '#b6d4fe',
          '#e7f1ff',
          '#f8f9fa',
        ],
        borderColor: '#fff',
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
      text: 'User Profession Distribution',
      color: '#000',
      font: {
        size: 18,
        weight: 'bold',
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
  background-color: #fff;
  border-radius: 1rem;
}
</style>
