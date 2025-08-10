<template>
  <div class="teacher-progress-page">
    <div class="content">
      <h1 class="section-title">{{ teacherName }}'s Progress</h1>
      
      <main class="main-container">
        <!-- Students Table Section -->
        <div class="students-section">
          <div v-if="studentData.length === 0" class="no-students">
            <p>No students assigned to this teacher</p>
          </div>
          
          <div v-else class="table-container">
            <table class="students-table">
              <thead>
                <tr>
                  <th style="width: 33.33%;">Name</th>
                  <th style="width: 33.33%;">Date of Birth</th>
                  <th style="width: 33.33%;">Progress</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="stud in studentData" :key="stud.student_name">
                  <td>{{ stud.student_name }}</td>
                  <td>{{ stud.dob }}</td>
                  <td>
                    <div class="tube">
                      <div class="fill" :style="{ width: stud.overall_progress + '%' }"></div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Charts Section -->
        <div v-if="studentData.length > 0" class="insights">
          <div class="chart-container">
            <canvas id="doughnutChart"></canvas>
            <p>Rank Distribution</p>
          </div>

          <div class="average-ranking">
            {{ averageRanking }}
            <div class="rank-label">Avg Rank</div>
          </div>

          <div class="chart-container">
            <canvas id="barChart"></canvas>
            <p>Topic wise average score</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import Chart from 'chart.js/auto';

import Navbar from '../Student/Navbar.vue'; // Import Navbar component
import Sidebar from './Sidebar.vue'; // Import Sidebar component

const router = useRoute();

const teacherName = ref(router.query.name);
const studentData = ref([]);
const averageRanking = ref(15);
const teacherId = ref(router.params.teacher_id); 
const instituteId = ref(router.params.institute_id);

let doughnutChartInstance = null
let barChartInstance = null

const renderCharts = () => {
  // Destroy old instances if they exist
  if (doughnutChartInstance) doughnutChartInstance.destroy()
  if (barChartInstance) barChartInstance.destroy()

  // Only render charts if there are students
  if (studentData.value.length === 0) return;

  // Doughnut Chart
  const doughnutCtx = document.getElementById('doughnutChart')?.getContext('2d')
  if (doughnutCtx) {
    doughnutChartInstance = new Chart(doughnutCtx, {
      type: 'doughnut',
      data: {
        labels: ['Ranks 1–10', 'Ranks 11–20', 'Ranks 21+'],
        datasets: [
          {
            data: [5, 8, 12],
            backgroundColor: ['#FF6384', '#4BC0C0', '#FFCE56'],
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }

  // Bar Chart
  const barCtx = document.getElementById('barChart')?.getContext('2d')
  if (barCtx) {
    barChartInstance = new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: ['Borrowing', 'Stocks', 'Finance', 'Loans', 'Investment'],
        datasets: [
          {
            label: 'Avg Score (%)',
            data: [68, 75, 82, 71, 89],
            backgroundColor: '#36A2EB'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    })
  }
}

const fetchTeacherProgress = async () => {
  try {
    const res = await fetch(
      `http://127.0.0.1:5000/Finance_Tutor/teacher_wise_progress/${instituteId.value}`,
      {
        headers: { Accept: 'application/json' }
      }
    )
    if (!res.ok) {
      alert('response not found')
      return
    }

    const data = await res.json()
    const filtered = data.teacher_progress.filter(item => item.teacher_id == teacherId.value)
    studentData.value = filtered.length > 0 ? filtered[0].student_details : []
    
    // Use nextTick to ensure DOM is updated before rendering charts
    await new Promise(resolve => setTimeout(resolve, 100));
    renderCharts()
  } catch (e) {
    console.error('Error fetching teacher data:', e)
  }
}

onMounted(fetchTeacherProgress);

watch(
  () => [router.params.teacher_id, router.query.name],
  ([newTeacherId, newTeacherName]) => {
    teacherId.value = newTeacherId
    teacherName.value = newTeacherName
    fetchTeacherProgress()
  }
)
</script>

<style scoped>
.teacher-progress-page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
}

.content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.section-title {
  color: white;
  font-size: 2.5em;
  font-weight: 700;
  margin: 0 0 20px 0;
  text-align: center;
}

.main-container {
  height: calc(100vh - 140px); /* Fixed height minus title and padding */
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow: hidden;
}

.students-section {
  flex: 1;
  min-height: 0;
  margin-bottom: 20px;
}

.no-students {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 1.2em;
  font-weight: 500;
}

.table-container {
  height: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
}

/* Custom scrollbar for table */
.table-container::-webkit-scrollbar {
  width: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  position: sticky;
  top: 0;
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
  z-index: 1;
}

th, td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

th {
  font-weight: 600;
  color: #333;
}

td {
  color: #555;
}

tr:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.tube {
  width: 90%;
  max-width: 250px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  overflow: hidden;
  margin: 0 auto;
}

.fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  transition: width 0.5s ease-in-out;
}

.insights {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 15px;
  flex-wrap: nowrap;
  height: 280px;
  min-height: 280px;
}

.chart-container {
  flex: 1;
  max-width: 280px;
  height: 260px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 25px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.chart-container canvas {
  flex: 1;
  width: 100% !important;
  height: 100% !important;
}

.chart-container p {
  margin: 10px 0 0 0;
  font-size: 0.9em;
  font-weight: 500;
  color: #555;
  text-align: center;
}

.average-ranking {
  width: 180px;
  height: 180px;
  border: 8px solid #ff9800;
  background: linear-gradient(135deg, #ffeb3b, #ffc107);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 32px;
  font-weight: bold;
  color: #333;
  position: relative;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.rank-label {
  font-size: 14px;
  position: absolute;
  bottom: 20px;
  color: #444;
  font-weight: 600;
}
</style>