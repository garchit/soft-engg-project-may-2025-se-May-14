<template>
    <div class="learn-container">
      <div class="main-content">
        <header class="profile-header">
          <div class="page-heading-box">
            <div class="page-heading">{{ instituteName }}</div>
            <div class="page-caption">
              Overview of the institute's performance and top teachers.
            </div>
          </div>
        </header>
      </div>
      <div class="course-content">
        <div class="top-teachers-podium">
          <div class="top-card " >
            <!-- v-if="topTeachers[2]"> -->
            <div class="medal-icon bronze">🥉</div>
            <div class="info">
              <!-- <div class="name">{{ topTeachers[2].name }}</div>-->
              <div class="name">Teacher03</div>
            </div>
          </div>
          <div class="top-card " >
          <!-- v-if="topTeachers[0]"> -->
            <div class="medal-icon gold">🥇</div>
            <div class="info">
              <!-- <div class="name">{{ topTeachers[0].name }}</div>-->
              <div class="name">Teacher01</div>
            </div>
          </div>
          <div class="top-card ">
           <!-- v-if="topTeachers[1]"> -->
            <div class="medal-icon silver">🥈</div>
            <div class="info">
              <!-- <div class="name">{{ topTeachers[1].name }}</div> -->
              <div class="name">Teacher02</div>
            </div>
          </div>
          <div class="unit-divider"></div>
        </div>

        <div class="charts-container">
          <div class="chart-card">
            <Bar :data="topTeachersData" :options="horizontalBarOptions" :width="0" :height="10" />
          </div>
          <div class="chart-card">
            <Bar :data="scoreDistributionData" :width="0" :height="10" />
          </div>
          <div class="chart-card">
            <Bar :data="topicFrequencyData" :width="0" :height="10" />
          </div>
        </div>

        <div class="unit-cards">
          <div class="unit-card" v-for="data in cardsData" :key="data.title">
            <div class="unit-divider"></div>
            <div class="unit-header">
              <p>{{ data.title }}</p> <p class="unit-description">{{ data.value }}</p>
            </div>
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
  { title: 'Your Score', value: averageInstituteScore },
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
.learn-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 100vh;
}

.main-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 23px 0 18px;
}

.page-heading-box {
  width: 85%;
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

.course-content {
  background: #ffffff3d;
  height: calc(100vh - 280px);
  margin: 10px 32px 0 32px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 40px;
}

.unit-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  width: 100%;
  margin-top: 10px;
}

.unit-card {
  border-radius: 15px;
  padding: 10px 20px 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.unit-divider {
  height: 3px;
  width: 100%;
  background: linear-gradient(to right,rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.1));
  margin: 2px 0 10px 0;
  border: none;
}

.unit-header {
  font-size: 1.4rem;
  background: white; 
  background-clip: text;
  color: white;
  text-align: center;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4);
}
.unit-header p {
  display: inline;
  margin: 0 5px; /* small gap between them */
}

.unit-description {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.charts-container {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  justify-content: center;
  gap: 30px;
  width: 100%;
  margin: 0px 10px 0px 10px;
}

.chart-card {
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 300px;
  height: 250px;
  flex: 1 1 0;
  background: #ffffff4d;
}

.top-teachers-podium {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.top-card {
  display: flex;
  align-items: center;
  width: 280px;
  padding: 10px 15px 0 15px;
  border-radius: 15px;
  /* box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); */
  font-weight: bold;
  font-size: 2rem;
  /* background: rgba(255, 255, 255, 0.2); */
  /* transition: transform 0.3s ease; */
  /* border: 3px solid #ffffff3d; */
  /* background-color: #ffffff1d; */
  /* box-shadow: 0 0 2px #cd7f32, 0 0 20px rgba(205, 127, 50, 0.4); */
}

.medal-icon {
  font-size: 2.7rem;
  margin-right: 8px;
  text-shadow: 1px 2px 5px rgba(0, 0, 0, 0.3);
}

.medal-icon.gold {
  text-shadow: 0 0 12px #ffd7004d, 0 0 24px #ffd7004d;
  transform: scale(1.2);
}
.medal-icon.silver {
  text-shadow: 0 0 12px #c0c0c04d, 0 0 24px #c0c0c04d;
  transform: scale(0.9);
}
.medal-icon.bronze {
  text-shadow: 0 0 12px #cd7f324d, 0 0 24px #cd7f324d;
  transform: scale(0.9);
}

.info {
  display: flex;
  flex-direction: column; 
  align-items: flex-start; 
  gap: 1px; 
}

.name {
  font-size: 1.1rem;
  color: #ffffff;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
}

</style>
