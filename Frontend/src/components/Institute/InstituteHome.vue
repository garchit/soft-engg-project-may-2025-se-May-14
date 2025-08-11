<template>
  <div class="institute-home-page">
    <div class="container">
      <h1>{{ instituteName }}</h1>

      <!-- Info Cards -->
      <div class="cards-container">
        <div class="card" v-for="data in cardsData" :key="data.title">
          <h2>{{ data.title }}</h2>
          <p class="card-value">{{ data.value }}</p>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-container">
        <div class="chart-card">
          <Bar :data="topTeachersData" :options="horizontalBarOptions" />
        </div>
        <div class="chart-card">
          <Bar :data="scoreDistributionData" />
        </div>
        <div class="chart-card">
          <Bar :data="topicFrequencyData" />
        </div>
      </div>

      <!-- Medal Cards -->
      <div class="top-teachers-cards">
        <div class="gold medal-card">
          <div class="medal-icon">🥇</div>
          <p>Mr. Sharma</p>
        </div>
        <div class="silver medal-card">
          <div class="medal-icon">🥈</div>
          <p>Ms. Rao</p>
        </div>
        <div class="bronze medal-card">
          <div class="medal-icon">🥉</div>
          <p>Mr. Mehta</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Bar } from 'vue-chartjs';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toast-notification';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const toast = useToast();
const route = useRoute();

// Data
const instituteId = route.params.institute_id;
const instituteName = ref('');
const totalTeachers = ref(null);
const averageInstituteScore = ref(null);
const totalStudents = ref(null);
let teacherProgressData = ref([]);

async function instituteDashboard() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/institute_info/${instituteId}`);
    
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || "Error fetching institute dashboard data");

    instituteName.value = data.name;
    totalTeachers.value = data.total_teachers;
    averageInstituteScore.value = data.average_institute_score;
    totalStudents.value = data.total_students;

  } catch (e) {
    toast.error(e.message || e.toString());
  }
}

async function instituteTeacherData(){
  try{
    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/teacher_wise_progress/${instituteId}`);
  
    const data = await response.json();
    teacherProgressData = data.teacher_progress;
    if(!response.ok) throw new Error(data.error || "Error fetching Teacher Data");

    console.log(teacherProgressData);
  } catch(e){
    toast.error(e.message || e.toString());
  }
}

onMounted(() => {
  instituteDashboard();
  instituteTeacherData();
})

const cardsData = ref([
  { title: 'Total Teachers', value: totalTeachers },
  { title: 'Average Institute Score', value: averageInstituteScore },
  { title: 'Total Students', value: totalStudents },
]);

// Chart Data
const topTeachersData = {
  labels: teacherProgressData.value.map(teacher => teacher.name),
  datasets: [
    {
      label: 'Performance',
      data: teacherProgressData.value.map(teacher => teacher.teacher_progress),
      backgroundColor: '#007bff',
    },
  ],
};

const horizontalBarOptions = {
  indexAxis: 'y',
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Top Teachers' },
  },
};

const scoreDistributionData = {
  labels: ['Class 6', 'Class 7', 'Class 8', 'Class 9'],
  datasets: [
    {
      label: 'Average Score',
      data: [72, 78, 74, 80],
      backgroundColor: '#4bc0c0',
    },
  ],
};

const topicFrequencyData = {
  labels: ['Stocks', 'Bonds', 'Mutual Funds', 'Crypto'],
  datasets: [
    {
      label: 'Topic Frequency',
      data: [40, 25, 20, 10],
      backgroundColor: '#36a2eb',
    },
  ],
};
</script>

<style scoped>
.institute-home-page {
  height: 100vh;
  display: flex;
}
.container {
  height: 100%;
  width: 100%;
  backdrop-filter: blur(12px);
  padding-bottom: 100px;
}
h1 {
  text-align: center;
  font-size: 42px;
  padding-top: 10px;
  color: white;
}
.cards-container {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  margin: 50px auto;
  border: 1px solid #cbd5e1;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  width: 80%;
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
}
.card {
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 250px;
  padding: 20px 0;
  margin: 10px 0;
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  text-align: center;
}
.card:hover {
  transform: scale(1.05);
}
.card-value {
  font-size: 1.5rem;
  text-align: center;
}

.charts-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  width: 90%;
  margin: 50px auto;
}
.chart-card {
  width: 30%;
  min-width: 280px;
  margin: 10px;
  padding: 20px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.top-teachers-cards {
  width: 80%;
  margin: 50px auto;
  display: flex;
  justify-content: space-evenly;
}
.medal-card {
  width: 250px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

  text-align: center;
  backdrop-filter: blur(10px);
}
.medal-card:hover {
  transform: scale(1.05);
}
.medal-icon {
  font-size: 48px;
}
.gold {
  background: linear-gradient(135deg, #f6e27a, #e6c200, #d4af37);
}
.silver {
  background: linear-gradient(135deg, #b8b8b8, #e6e6e6, #ffffff);
  border: 1px solid #a9a9a9;
}
.bronze {
  background: linear-gradient(135deg, #cd7f32, #b87333, #a97142);
  border: 1px solid #8b5e3c;
}
</style>
