<template>
  <InteractiveLayout>
    <div class="student-dashboard-page">

      <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">
            {{ loading ? 'Loading...' : `Welcome, ${user.full_name}` }}
          </div>
          <div class="page-caption">Your Learning Dashboard</div>
        </div>
      </header>

      <div class="dashboard-content-area">
        <div class="top-stats-section">
          <div class="donut-chart-container">
            <DonutChart :progress="overallProgress" />
          </div>
          <div class="stats-group">
              <div class="rank">
                <h2 style="color: white; text-align: center;">Rank: {{ user.rank || 'N/A' }}</h2>
              </div>
          </div>
          <StreakCalendar ref="calendarComponent" />
        </div>

        <h2 class="section-header">Units Completed</h2>
        <div class="cards-container">
            <CCard v-for="course in completedCourses" :key="course.id" class="info-card">
              <CCardImage orientation="center" :src="course.image_url" class="card-img" />
              <CCardBody class="card-body">
                <CCardText>
                  {{ course.title }}<br>
                  <strong>Grade: {{ course.grade }}</strong>
                </CCardText>
              </CCardBody>
            </CCard>
            <p v-if="!completedCourses.length">You have not completed any units yet.</p>
        </div>

        <h2 class="section-header">Recommended For You</h2>
        <div class="cards-container">
            <CCard v-for="course in recommendedCourses" :key="course.id" class="info-card hover-card" >
              <CCardImage orientation="center" :src="`/src/assets/unit${course.id}.png`" class="card-img"  @error="onImageError"/>
              <CCardBody class="card-body">
                <CCardText>{{ course.title }}</CCardText>
              </CCardBody>
            </CCard>
            <p v-if="!recommendedCourses.length">No recommendations available at the moment.</p>
        </div>
      </div>
    </div>
  </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import StreakCalendar from './Calendar.vue'; 
import { CCard, CCardImage, CCardBody, CCardText } from '@coreui/vue';
import DonutChart from '../donutChart.vue';
import InteractiveLayout from '../InteractiveLayout.vue';

// --- State ---
const user = ref({});
const loading = ref(true);
const calendarComponent = ref(null);
const API_BASE = "/Finance_Tutor";
const overallProgress = ref(0);
const recommendedCourses = ref([]);
const completedCourses = ref([]);

// --- API Calls ---

const fetchUserData = async () => {
  const currentUsername = localStorage.getItem('username');
  if (!currentUsername) { loading.value = false; return; }
  try {
    const response = await axios.get(`${API_BASE}/user_rank/${currentUsername}`);
    user.value = response.data;
  } catch (error) { console.error("Error fetching user data:", error); } 
  finally { loading.value = false; }
};

const performAutomaticCheckIn = async () => {
  try {
    await axios.post(`${API_BASE}/user/streak`);
    if (calendarComponent.value) { calendarComponent.value.fetchStreakData(); }
  } catch (error) { console.error("Error during check-in:", error.response?.data); }
};

const fetchCourseProgress = async () => {
  if (!user.value.id) return;
  try {
    const response = await axios.get(`${API_BASE}/course_progress/${user.value.id}`);
    if (response.data?.overall_progress) {
      overallProgress.value = response.data.overall_progress;
    }
  } catch (error) { console.error("Error fetching course progress:", error.response?.data); }
};

const onImageError = (event) => {
    event.target.src = '/src/assets/default.png';
}

const fetchRecommendations = async () => {
    if (!user.value.id) return;
    try {
        const response = await axios.get(`${API_BASE}/recommended_courses/${user.value.id}`);
        recommendedCourses.value = response.data.recommendations;
    } catch (error) { console.error("Error fetching recommendations:", error.response?.data); }
};

const fetchCompletedCourses = async () => {
    if (!user.value.id) return;
    try {
        const response = await axios.get(`${API_BASE}/user_course_completed/${user.value.id}`);
        completedCourses.value = response.data.completed_courses;
    } catch (error) { console.error("Error fetching completed courses:", error.response?.data); }
};

// --- Lifecycle Hook ---
onMounted(async () => {
  await fetchUserData(); // First, get user data (including the ID)
  
  // Now that we have the user ID, we can call all other functions
  if (user.value.id) {
    fetchCourseProgress();
    performAutomaticCheckIn();
    fetchRecommendations();
    fetchCompletedCourses();
  }
});
</script>

<style scoped>
/* ALL YOUR ORIGINAL CSS IS PRESERVED HERE */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
.student-dashboard-page { padding: 20px; width: 100%; font-family: 'Poppins', sans-serif; max-height: 100vh; overflow-y: auto; }
.profile-header { width: 100%; display: flex; justify-content: center; align-items: center; margin-bottom: 25px; }
.page-heading-box { width: 90%; max-width: 1200px; padding: 1rem 0; border-radius: 20px; border: 2px solid rgba(255, 255, 255, 0.6); background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(8px); box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2); text-align: center; }
.page-heading { font-size: 2.5rem; font-weight: 700; color: #ffffff; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3); min-height: 48px; }
.page-caption { font-size: 1rem; font-weight: 500; color: #ffffffcc; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2); margin-top: -0.5rem; }
.dashboard-content-area { background-color: #ffffff4d; padding: 30px; border-radius: 15px; margin: 0 auto; max-width: 1200px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1); }
.top-stats-section { display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px; margin-bottom: 40px; }
.donut-chart-container { width: 250px; height: 250px; transition: transform 0.3s ease; }
.donut-chart-container:hover { transform: scale(1.05); }
.rank { background-color: #E54C91; padding: 15px 25px; border-radius: 15px; text-align: center; box-shadow: 0 6px 12px rgba(229, 76, 145, 0.4); font-family: 'Poppins', sans-serif; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.rank:hover { transform: scale(1.1); box-shadow: 0 10px 20px rgba(229, 76, 145, 0.5); }
.section-header { text-align: center; font-family: 'Poppins', sans-serif; color: #333; font-weight: 600; font-size: 1.8em; margin-top: 40px; margin-bottom: 20px; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1); }
.cards-container { display: flex; justify-content: center; align-items: center; gap: 25px; flex-wrap: wrap; background-color: rgba(255, 255, 255, 0.5); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); border-radius: 15px; padding: 25px; margin-bottom: 20px; }
.info-card { width: 160px; height: 180px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; transition: transform 0.3s ease, box-shadow 0.3s ease; border: none; }
.info-card.hover-card:hover { transform: translateY(-8px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15); }
.card-img { width: 100%; height: 100px; object-fit: cover; }
.card-body { text-align: center; padding: 10px; font-size: 0.9rem; font-weight: 500; color: #555; width: 100%; }
.stats-group { display: flex; flex-direction: column; gap: 15px; align-items: center; }
</style>