<template>
    <div class="progress-donut-chart">
      <Pie :data="chartData" :options="chartOptions" :plugins="[progressDotPlugin]" />
      <div class="progress-text">
        <p class="percentage">{{ progress }}%</p>
        <p class="label">PROGRESS</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, watch, ref } from 'vue';
  import { Pie } from 'vue-chartjs';
  import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
  } from 'chart.js';
  
  ChartJS.register(ArcElement, Tooltip, Legend);
  
  const props = defineProps({
    progress: {
      type: Number,
      required: true,
      default: 0,
    },
  });
  
  const animatedProgress = ref(0);
  

  watch(
    () => props.progress,
    (newVal) => {
      const start = animatedProgress.value;
      const end = newVal;
      const duration = 1000;
      const startTime = performance.now();
  
      const animate = (now) => {
        const elapsed = now - startTime;
        const t = Math.min(elapsed / duration, 1); // clamp 0-1
        animatedProgress.value = start + (end - start) * easeOutCubic(t);
        if (t < 1) requestAnimationFrame(animate);
      };
  
      requestAnimationFrame(animate);
    },
    { immediate: true }
  );
  

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }
  

  const chartData = computed(() => ({
    datasets: [
      {
        data: [animatedProgress.value, 100 - animatedProgress.value],
        backgroundColor: ['#29B6F6', '#e0e0e0'],
        borderWidth: 0,
        hoverOffset: 0,
      },
    ],
  }));
  

  const progressDotPlugin = {
    id: 'progressDotPlugin',
    afterDatasetsDraw(chart) {
      const meta = chart.getDatasetMeta(0);
      if (!meta || !meta.data[0]) return;
  
      const ctx = chart.ctx;
      const value = chart.data.datasets[0].data[0];
      const total = 100;
      const angle = (value / total) * 2 * Math.PI - Math.PI / 2;
  
      const { x: centerX, y: centerY } = meta.data[0];
      const radius = meta.data[0].outerRadius - 10; 
  
      const dotX = centerX + Math.cos(angle) * radius;
      const dotY = centerY + Math.sin(angle) * radius;
  
      ctx.save();
      ctx.beginPath();
      ctx.arc(dotX, dotY, 12, 0, 2 * Math.PI); 
      ctx.fillStyle = '#29B6F6'; 
      ctx.strokeStyle = '#fff'; 
      ctx.lineWidth = 4; 
      ctx.fill();
      ctx.stroke();
      ctx.closePath();
      ctx.restore();
    },
  };
  

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };
  </script>
  
  <style scoped>
  .progress-donut-chart {
    position: relative;
    width: 100%;
    max-width: 300px;
    aspect-ratio: 1 / 1;
    margin: auto;
  }
  
  .progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
  }
  
  .percentage {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
  }
  
  .label {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
    letter-spacing: 1px;
  }
  </style>
  