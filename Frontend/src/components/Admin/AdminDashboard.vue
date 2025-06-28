<template>
    <div ref="backgroundRef" class="interactive-background">
      <div
        v-for="ripple in ripples"
        :key="ripple.id"
        class="ripple"
        :style="{ left: ripple.x + 'px', top: ripple.y + 'px' }"
      ></div>
  
      <div class="admin-page">
        <Sidebar />
  
        <div class="admin-content">
          <h1 class="dashboard-title" style="text-align: center;">Hi Admin</h1><br /><br />
  
          <div class="main-container">
            <h2 class="table-title" style="text-align: center;">Top Performing Schools</h2>
  
            <div class="table-container">
              <div class="badges-section">
              <div class="badge">
                <img src="@/components/assets/silver-medal.png" alt="Silver Medal" class="badge-icon" />
                <div class="badge-text">
                  <p>Institute B</p>
                  <p>Score: 90</p>
                </div>
              </div>
              <div class="badge">
                <img src="@/components/assets/gold-medal.png" alt="Gold Medal" class="badge-icon" />
                <div class="badge-text">
                  <p>Institute A</p>
                  <p>Score: 95</p>
                </div>
              </div>
              <div class="badge">
                <img src="@/components/assets/bronze-medal.png" alt="Bronze Medal" class="badge-icon" />
                <div class="badge-text">
                  <p>Institute C</p>
                  <p>Score: 85</p>
                </div>
              </div>
            </div>
  
              <table class="admin-table">
                <thead>
                  <tr>
                    <th>INSTITUTE NAME</th>
                    <th>RANK</th>
                    <th>AVG SCORE</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="inst in institutes.slice(3)" :key="inst.name">
                    <td>{{ inst.name }}</td>
                    <td>{{ inst.rank }}</td>
                    <td>{{ inst.avg_score }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
  
            <h2 class="insights-header" style="text-align: center;">INSIGHTS</h2>
            <div class="charts-section">
              <div class="total-institutes-card">
                <h3>TOTAL INSTITUTES</h3>
                <p>{{ totalInstitutes }}</p>
              </div>
              <div class="chart-container">
                <Pie :data="chartData" :options="chartOptions" />
              </div>
              <div class="total-student-card">
                <h3>TOTAL STUDENTS</h3>
                <p>{{ totalStudent }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import Sidebar from './Sidebar.vue';
  import { Pie } from 'vue-chartjs';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
  } from 'chart.js';
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement);
  
  const chartData = ref({
    labels: ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'],
    datasets: [
      {
        label: 'Class Distribution',
        data: [120, 100, 80, 60, 40],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        hoverOffset: 4,
      },
    ],
  });
  
  const chartOptions = ref({
    responsive: true,
    plugins: {
      legend: {
        display: false, 
      },
      tooltip: {
        enabled: true, 
      },
    },
  });
  
  const institutes = ref([
    { name: 'Institute A', rank: 1, avg_score: 95 },
    { name: 'Institute B', rank: 2, avg_score: 90 },
    { name: 'Institute C', rank: 3, avg_score: 85 },
    { name: 'Institute D', rank: 4, avg_score: 80 },
    { name: 'Institute E', rank: 5, avg_score: 75 },
  ]);
  
  const totalInstitutes = ref(institutes.value.length);
  const totalStudent = ref(500); 
  
  const backgroundRef = ref(null);
  const ripples = ref([]);
  let rippleId = 0;
  
  const createRipple = (event) => {
    const rect = backgroundRef.value.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
  
    const newRipple = { id: rippleId++, x, y, opacity: 1 };
    ripples.value.push(newRipple);
  
    setTimeout(() => {
      const index = ripples.value.findIndex((r) => r.id === newRipple.id);
      if (index > -1) ripples.value.splice(index, 1);
    }, 1000);
  };
  
  const updateBackgroundColor = (event) => {
    if (!backgroundRef.value) return;
    const rect = backgroundRef.value.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
  

    backgroundRef.value.style.background = `
      radial-gradient(circle at ${x}% ${y}%,
        rgba(255, 200, 0, 0.6) 0%, /* Muted Yellow */
        rgba(229, 76, 145, 0.5) 50%, /* Muted Pink */
        rgba(128, 123, 123, 0.4) 100% /* Muted Gray */
      )
    `;
  };
  
  const handleMouseMove = (event) => updateBackgroundColor(event);
  const handleClick = (event) => createRipple(event);
  
  onMounted(() => {
    if (backgroundRef.value) {
      backgroundRef.value.addEventListener('mousemove', handleMouseMove);
      backgroundRef.value.addEventListener('click', handleClick);
    }
  });
  
  onUnmounted(() => {
    if (backgroundRef.value) {
      backgroundRef.value.removeEventListener('mousemove', handleMouseMove);
      backgroundRef.value.removeEventListener('click', handleClick);
    }
  });
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  
  .interactive-background {
    width: 100%;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    transition: background 0.3s ease;
    font-family: 'Poppins', sans-serif;
  }
  
  .main-container {
    background: rgba(255, 255, 255, 0.303); 
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(86, 83, 83, 0.2);
    margin: 20px auto;
    width: 90%; 
    height: auto; 
  }
  
  .ripple {
    position: absolute;
    width: 12px; 
    height: 12px;
    background: rgba(255, 255, 255, 0.4); 
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: ripple-animation 0.6s linear;
  }
  
  @keyframes ripple-animation {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
    }
    100% {
      transform: translate(-50%, -50%) scale(1.8);
      opacity: 0;
    }
  }
  
  .admin-page {
    display: flex;
  }
  
  .admin-content {
    flex-grow: 1;
    padding: 20px;
    margin-left: 250px; 
    overflow-y: auto;
  }
  
  .table-container {
    width: 85%;
    margin: 20px auto; 
    padding: 20px;
    background: #1cb1f6ab;
    border: 10px solid #ffd900b9; 
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .badges-section {
    display: flex;
    justify-content: center;
    gap: 40px; 
    margin-bottom: 20px;
  }
  .badge {
    display: flex;
    flex-direction: column; 
    align-items: center;
    text-align: center;
    gap: 10px; 
    background: none; 
    box-shadow: none; 
    border: none;
  }
  
  .badge-icon {
    width: 80px;
    height: 80px;
    object-fit: contain;
  }
  
  .badge-text {
    margin-top: 10px; 
    font-size: 14px;
    font-weight: bold;
    color: white;
  }
  
  .admin-table {
    width: 70%;
    border-collapse: collapse;
    text-align: center;
    margin: 0 auto; 
  }
  
  .admin-table th,
  .admin-table td {
    padding: 10px;
    border: 1px solid rgba(117, 108, 108, 0.293);
  }
  
  .admin-table thead th {
    background: rgba(116, 112, 112, 0.187);
    color: white;
  }
  
  .admin-table tbody tr:hover {
    background: rgba(118, 114, 114, 0.1);
  }
  
  .charts-section {
    display: flex;
    flex-direction: row;
    gap: 20px;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  
  .chart-container {
    width: 200px; 
    height: 200px; 
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(128, 123, 123, 0.1);
    border-radius: 10px;
    padding: 10px;
  }
  
  .total-institutes-card {
    width: 200px;
    height: 200px;
    background: #e54c91ba;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  }
  
  .total-student-card {
    width: 200px;
    height: 200px;
    background: #1cb1f6ab;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  
  }
  </style>