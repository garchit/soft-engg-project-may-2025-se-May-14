<script setup>
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';


ChartJS.register(Title, Tooltip, Legend, ArcElement);


const chartData = {
  labels: ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'], 
  datasets: [
    {
      label: 'Class Distribution',
      data: [120, 100, 80, 60, 40], 
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'], 
      hoverOffset: 4,
    },
  ],
};


const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false, 
    },
    title: {
      display: true,
      text: 'Top 5 Most Enrolled Classes',
      font: {
        family: 'Poppins', 
        size: 16, 
      },
      color: '#FFFFFF', 
    },
  },
};
</script>

<template>
  <div class="pie-chart-container">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.pie-chart-container {
  width: 100%;
  max-width: 400px; 
  margin: 0 auto; 
}
</style>
