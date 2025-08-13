<template>
  <div class="teacher-progress-page">
      <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">{{ teacherName }}'s Progress</div>
          <div class="page-caption">
            Check your teacher's progress here and send them AI generated report.
          </div>
        </div>
          <button class="generate-report-btn" @click="alert('Feature will be available soon')">
            Generate Report
            <span class="sparkle sparkle1"></span>
            <span class="sparkle sparkle2"></span>
            <span class="sparkle sparkle3"></span>
          </button>
      </header>
      <main class="main-container">
        <!-- Charts Section -->
        <div v-if="studentData.length > 0" class="insights">
          <div class="chart-container">
            <canvas id="doughnutChart"></canvas>
            <p>Rank Distribution</p>
          </div>

          <div class="average-ranking">
            <div class="rank-label">Avg Rank</div>
            <div class="rank-labell">{{ averageRanking }}</div>
          </div>

          <div class="chart-container">
            <canvas id="barChart"></canvas>
            <p>Topic wise average score</p>
          </div>
        </div>
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
      </main>
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
            position: 'left',
            labels: {
            boxWidth: 15, 
            padding: 5   
          }
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
  flex: 1;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  margin-bottom: 20px;
}

.profile-header {
  width: 90%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 22px 0px 20px 0px;
  flex-wrap: wrap;
}

.page-heading-box {
  width: 82%;
  padding: 1rem 0 2rem 0;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.page-heading {
  font-size: 3rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

.page-caption {
  font-size: 0.8rem;
  font-weight: 500;
  color: #ffffffcc;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  margin-top: -0.5rem;
}

.generate-report-btn {
  position: relative;
  padding: 1.2rem 0.9rem;
  width: 150px;
  border-radius: 15px;
  background: #ffffff2d;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  color: #fff;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-align: center;
  overflow: hidden;
}
.generate-report-btn:hover {
  background: #20b45766;
  transform: scale(1.05);
}

/* Sparkle base style */
.sparkle {
  position: absolute;
  width: 8px;
  height: 8px;
  width: 18px;
  height: 18px;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffffff'><path d='M12 2l2 6 6 2-6 2-2 6-2-6-6-2 6-2z'/></svg>") no-repeat center;
  background-size: contain;
  opacity: 0;
  animation: sparkle-pop 1.5s infinite ease-in-out;
}

/* Different sparkles with varied timing & size */
.sparkle1 { bottom: 15%; left: 9%; animation-delay: 0s; }
.sparkle2 { bottom: 50%; left: 84%; animation-delay: 1s; }
.sparkle3 { bottom: 75%; left: 74%; animation-delay: 0.5s; }

@keyframes sparkle-pop {
  0% {
    transform: scale(0) rotate(0deg);
    opacity: 0;
  }
  20% {
    transform: scale(1) rotate(45deg);
    opacity: 1;
  }
  50% {
    transform: scale(1.3) rotate(90deg);
    opacity: 1;
  }
  80% {
    transform: scale(1) rotate(135deg);
    opacity: 1;
  }
  100% {
    transform: scale(0) rotate(180deg);
    opacity: 0;
  }
}

.section-title {
  color: white;
  font-size: 2.5em;
  font-weight: 700;
  margin: 0 0 20px 0;
  text-align: center;
}

.main-container {
  width: 100%;
  background: #ffffff4d;
  padding: 30px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  height: calc(100vh - 270px);
}

.students-section {
  width: 100%;
  flex: 1;
  min-height: 100px;
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
  max-height: 450px;
  width: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: #ffffff2d;
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
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.01);
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
  width: 90%;
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 45px;
  flex-wrap: nowrap;
}

.chart-container {
  flex: 1;
  height: 100%;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 25px 0 0 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.chart-container canvas {
  flex: 1;
  width: 80% !important;
  height: 80% !important;
}

.chart-container p {
  margin: 10px;
  font-size: 0.9em;
  font-weight: 500;
  color: #555;
  text-align: center;
}

.average-ranking {
  width: 150px;
  height: 150px;
  border: 2px solid #ffffff4d;
  background: #ffffff3d;
  border-radius: 20px;
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
  font-size: 15px;
  position: absolute;
  top: 30px;
  color: #444;
  font-weight: 600;
}

.rank-labell {
  font-size: 30px;
  position: absolute;
  top: 60px;
  color: #444;
  font-weight: 600;
}

</style>