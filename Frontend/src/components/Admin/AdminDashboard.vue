<template>

    <div class="admin-page">
      <Navbar />
      <Sidebar />

      <div class="admin-content">
        <div class="main-container">

          <h2 class="section-title">INSIGHTS</h2>
          <div class="insights-container">
            <div class="insights-grid">
              <div class="stat-card institutes-card">
                <div class="stat-icon">🏫</div>
                <div class="stat-content">
                  <h3>Total Institutes</h3>
                  <p class="stat-number">{{ totalInstitutes }}</p>
                </div>
              </div>
              
              <div class="chart-wrapper">
                <h3 class="chart-title">Class Distribution</h3>
                <div class="chart-container">
                  <Pie :data="chartData" :options="chartOptions" />
                </div>
                <div class="chart-legend">
                  <div class="legend-item" v-for="(label, index) in chartData.labels" :key="label">
                    <span class="legend-color" :style="{ backgroundColor: chartData.datasets[0].backgroundColor[index] }"></span>
                    <span class="legend-text">{{ label }}</span>
                  </div>
                </div>
              </div>
              
              <div class="stat-card students-card">
                <div class="stat-icon">👥</div>
                <div class="stat-content">
                  <h3>Total Students</h3>
                  <p class="stat-number">{{ totalStudent }}</p>
                </div>
              </div>
            </div>
          </div>

          <h2 class="section-title">Top Performing Schools</h2>
          <div class="table-section">
            <div class="podium-container">
              <div class="podium-item second-place">
                <div class="medal-wrapper">
                  <div class="medal silver">🥈</div>
                  <div class="school-info">
                    <h4>{{ institutes[1].name }}</h4>
                    <p class="score">{{ institutes[1].avg_score }}%</p>
                  </div>
                </div>
              </div>
              
              <div class="podium-item first-place">
                <div class="medal-wrapper">
                  <div class="medal gold">🥇</div>
                  <div class="school-info">
                    <h4>{{ institutes[0].name }}</h4>
                    <p class="score">{{ institutes[0].avg_score }}%</p>
                  </div>
                </div>
              </div>
              
              <div class="podium-item third-place">
                <div class="medal-wrapper">
                  <div class="medal bronze">🥉</div>
                  <div class="school-info">
                    <h4>{{ institutes[2].name }}</h4>
                    <p class="score">{{ institutes[2].avg_score }}%</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="table-container">
              <table class="performance-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Institute Name</th>
                    <th>Average Score</th>
                    <th>Performance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="inst in institutes.slice(3)" :key="inst.name" class="table-row">
                    <td class="rank-cell">
                      <span class="rank-badge">{{ inst.rank }}</span>
                    </td>
                    <td class="institute-cell">{{ inst.name }}</td>
                    <td class="score-cell">{{ inst.avg_score }}%</td>
                    <td class="performance-cell">
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: inst.avg_score + '%' }"></div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Sidebar from './Sidebar.vue';
import Navbar from '../Student/Navbar.vue';
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
      label: 'Students',
      data: [120, 100, 80, 60, 40],
      backgroundColor: [
        '#FF6B6B',
        '#4ECDC4', 
        '#45B7D1',
        '#96CEB4',
        '#FFEAA7'
      ],
      borderWidth: 0,
      hoverOffset: 8,
    },
  ],
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#fff',
      borderWidth: 1,
      cornerRadius: 8,
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
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.interactive-background {
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  transition: background 0.3s ease;
  font-family: 'Poppins', sans-serif;
}


.admin-page {
  display: flex;
}

.admin-content {
  flex-grow: 1;
  padding: 20px;
  margin-left: 250px;
  overflow-y: auto;
  margin-top: 60px;
}

.main-container {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  width: 80%;
  font-family: 'poppins', sans-serif;
  max-width: 1400px;
}

.section-title {
  text-align: center;
  color: rgb(0, 0, 0);
  font-size: 2.5em;
  font-weight: 700;
  margin-bottom: 30px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: 1px;
}

.insights-container {
  margin-bottom: 50px;
}

.insights-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 30px;
  align-items: center;
}

.stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  font-size: 3em;
  margin-bottom: 15px;
}

.stat-content h3 {
  color: rgb(0, 0, 0);
  font-size: 1.2em;
  font-weight: 600;
  margin-bottom: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.stat-number {
  color: #000000;
  font-size: 3em;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.chart-wrapper {
  text-align: center;
}

.chart-title {
  color: rgb(0, 0, 0);
  font-size: 1.5em;
  font-weight: 600;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.chart-container {
  width: 300px;
  height: 300px;
  margin: 0 auto 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 20px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-text {
  color: rgb(0, 0, 0);
  font-size: 0.9em;
  font-weight: 500;
}


.table-section {
  margin-top: 40px;
}

.podium-container {
  display: flex;
  justify-content: center;
  align-items: end;
  gap: 20px;
  margin-bottom: 40px;
}

.podium-item {
  text-align: center;
  transition: transform 0.3s ease;
}

.podium-item:hover {
  transform: translateY(-5px);
}

.first-place {
  order: 2;
}

.second-place {
  order: 1;
}

.third-place {
  order: 3;
}

.medal-wrapper {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.medal {
  font-size: 4em;
  margin-bottom: 15px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.school-info h4 {
  color: rgb(0, 0, 0);
  font-size: 1.3em;
  font-weight: 600;
  margin-bottom: 5px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.school-info .score {
  color: #000000;
  font-size: 1.8em;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.table-container {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.performance-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  color: rgb(0, 0, 0);
}

.performance-table th {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  padding: 20px;
  text-align: left;
  font-weight: 600;
  font-size: 1.1em;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.performance-table th:first-child {
  border-radius: 15px 0 0 0;
}

.performance-table th:last-child {
  border-radius: 0 15px 0 0;
}

.table-row {
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.02);
}

.performance-table td {
  padding: 20px;
  font-size: 1em;
}

.rank-badge {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #333;
  padding: 8px 15px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1.1em;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.institute-cell {
  font-weight: 600;
  font-size: 1.1em;
}

.score-cell {
  font-weight: 700;
  font-size: 1.2em;
  color: #000000;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1e74bb, #44A08D);
  border-radius: 10px;
  transition: width 0.8s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

@media (max-width: 1200px) {
  .insights-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .chart-container {
    width: 250px;
    height: 250px;
  }
}

@media (max-width: 768px) {
  .admin-content {
    margin-left: 0;
    padding: 10px;
  }
  
  .main-container {
    padding: 20px;
  }
  
  .podium-container {
    flex-direction: column;
    align-items: center;
  }
  
  .podium-item {
    order: unset !important;
  }
  
  .performance-table {
    font-size: 0.9em;
  }
  
  .performance-table th,
  .performance-table td {
    padding: 15px 10px;
  }
}
</style>