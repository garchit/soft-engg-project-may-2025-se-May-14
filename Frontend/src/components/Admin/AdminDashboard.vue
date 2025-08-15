<template>
    <InteractiveLayout>
      <div class="admin-page">
          <div class="main-container">
            <!-- <h2 class="section-title">INSIGHTS</h2> -->
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
                  <div class="chart-container">
                    <h3 class="chart-title">Class Distribution</h3>
                    <div style="width:180px; height:180px; margin:10px auto;">
                      <Pie :data="chartData" :options="chartOptions" />
                    </div>
                    <div class="chart-legend">
                    <div class="legend-item" v-for="(label, index) in chartData.labels" :key="label">
                      <span class="legend-color" :style="{ backgroundColor: chartData.datasets[0].backgroundColor[index] }"></span>
                      <span class="legend-text">{{ label }}</span>
                    </div>
                  </div>
                  </div>
                </div>
      
                <div class="stat-card students-card">
                  <div class="stat-icon">👥</div>
                  <div class="stat-content">
                    <h3>Total Students</h3>
                    <p class="stat-number">{{ totalStudents }}</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- <h2 class="section-title">Top Performing Schools</h2> -->
            <!-- <div class="table-section">
              <div class="podium-container">
                <div class="podium-item second-place">
                  <div class="medal-wrapper">
                    <div class="medal silver">🥈</div>
                    <div class="school-info">
                      <h4>{{ allInstitutes[0].institute_name }}</h4>
                      <p class="score">{{ allInstitutes[1].average_score }}%</p>
                    </div>
                  </div>
                </div>
      
                <div class="podium-item first-place">
                  <div class="medal-wrapper">
                    <div class="medal gold">🥇</div>
                    <div class="school-info">
                      <h4>{{ allInstitutes[0].institute_name }}</h4>
                      <p class="score">{{ allInstitutes[0].average_score }}%</p>
                    </div>
                  </div>
                </div>
      
                <div class="podium-item third-place">
                  <div class="medal-wrapper">
                    <div class="medal bronze">🥉</div>
                    <div class="school-info">
                      <h4>{{ allInstitutes[2].institute_name }}</h4>
                      <p class="score">{{ allInstitutes[2].average_score }}%</p>
                    </div>
                  </div>
                </div>
              </div>
              </div> -->
              <div class="table-container">
                <table class="institute-table">
                  <thead>
                    <tr>
                      <th style="width: 15%">Rank</th>
                      <th style="width: 30%">Institute Name</th>
                      <th style="width: 20%">Average Score</th>
                      <th style="width: 35%">Performance</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(inst, rank) in allInstitutes" :key="inst.institute_id" class="table-row">
                      <td class="rank-cell">
                        <span class="rank-badge">{{ rank + 1}}</span>
                      </td>
                      <td class="institute-cell">{{ inst.institute_name }}</td>
                      <td class="score-cell">{{ inst.average_score }}%</td>
                      <td class="performance-cell">
                        <div class="progress-bar">
                          <div class="progress-fill" :style="{ width: inst.average_score + '%' }"></div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
          </div>
          </div>
    </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import InteractiveLayout from './AdminLayout.vue';

let totalInstitutes = ref();
let totalTeachers = ref();
let totalStudents = ref();
let allInstitutes = ref([]);
let countClass = ref({});

ChartJS.register(Title, Tooltip, Legend, ArcElement);
const chartData = ref({
  labels: [],
  datasets: [{
    label: 'Students',
    data: [],
    backgroundColor: [
      '#FF6B6B',
      '#4ECDC4',
      '#45B7D1',
      '#96CEB4',
      '#FFEAA7'
    ],
    borderWidth: 0,
    hoverOffset: 8,
  }],
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

async function adminDashboardData() {
  try {
    const response = await fetch("http://127.0.0.1:5000/Finance_Tutor/admin/home");
    
    if (!response.ok) throw new Error("Server Error");
    
    const data = await response.json();

    totalInstitutes.value = data.total_institutes;
    totalStudents.value = data.total_students;
    totalTeachers.value = data.total_teachers;
    countClass.value = data.count_class;

    const sortedInstitutes = data.institute_info.sort((a, b) => b.average_score - a.average_score);
    allInstitutes.value = sortedInstitutes;
  } catch (e) {
    alert("Error fetching dashboard data");
    console.error(e);
  }
}

  watch(countClass, (newVal) => {
  chartData.value = {
    labels: Object.keys(newVal),
    datasets: [{
      label: 'Students',
      data: Object.values(newVal),
      backgroundColor: [
        '#FF6B6B',
        '#4ECDC4',
        '#45B7D1',
        '#96CEB4',
        '#FFEAA7'
      ],
      borderWidth: 0,
      hoverOffset: 8,
    }],
  };
}, { immediate: true });

onMounted(() => {
  adminDashboardData();
});


</script>

<style scoped>

.admin-page {
  display: flex;
}

.main-container {
  background: #ffffff3d;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin: 20px;
  width: 100%;
  height: calc(100vh - 100px);
  overflow-y: auto;
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
  margin: 0 40px 30px 40px;
}

.insights-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 10px;
  align-items: center;
}

.stat-card {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 3em;
  margin-bottom: 15px;
}

.stat-content h3 {
  color: #000000aa;
  font-size: 1em;
  font-weight: 600;
  margin-bottom: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.stat-number {
  color: #000000aa;
  font-size: 3em;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.chart-wrapper {
  text-align: center;
}

.chart-title {
  color: #000000aa;
  font-size: 1em;
  font-weight: 600;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.chart-container {
  width: 280px;
  height: 280px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 15px 30px;
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
  max-height: 330px;
  width: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: #ffffff3d;
  margin: 20px 0 0 0;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  font-size: 20px;
  color: #000000a5;
}

thead {
  position: sticky;
  top: 0;
  background: #ffddc8;
}

th {
  padding: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.15);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

td {
  padding: 10px;
}

tr {
  font-size: 0.8rem;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

tr:hover {
  background: #ffffff4d;
  transform: scale(1.01);
}

.rank-badge {
  /* background: #ffffffd; */
  color: #000000aa;
  /* padding: 8px 15px; */
  /* border-radius: 15px; */
  font-weight: 700;
  font-size: 1.1em;
  /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); */
}

.institute-cell {
  font-weight: 600;
  font-size: 1.1em;
}

.score-cell {
  font-weight: 700;
  font-size: 1.2em;
  color: #000000aa;
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