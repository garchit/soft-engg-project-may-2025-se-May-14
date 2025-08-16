<template>
    <InteractiveLayout>
        <div class="learn-container">
            <div class="main-content">
                <header class="profile-header">
                    <div class="page-heading-box">
                        <div class="page-heading">Learning Page</div>
                        <div class="page-caption">
                            These courses are your cheat codes to mastering money. Find what excites you and start your financial adventure now!
                        </div>
                    </div>
                </header>
            </div>
            <div class="course-content">
                <div class="unit-cards">
                    <div class="unit-card" v-for="unit in unitsWithScores" :key="unit.course_id">
                        <div class="unit-header">
                            <h3>{{ unit.course_title }}</h3>
                        </div>
                        <div class="unit-divider"></div>
                        <!-- Unit Image -->
                        <img
                            :src="unit.image"
                            alt="Unit Image"
                            class="unit-image"
                        />
                        <p class="unit-description">{{ unit.course_description }}</p>
                        <div class="button-container">
                              <div class="score-box"> Your Score: {{ unit.score }} </div>
                              <button
                              class="start-button"
                              @click="$router.push(`/student-learn/${unit.course_id}`)">
                              ▶ Start Learning
                              </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import InteractiveLayout from '../InteractiveLayout.vue';

const API_BASE = "/Finance_Tutor";
const currentUserId = localStorage.getItem('user_id') || "1"; // fallback user ID
const currentUsername = localStorage.getItem('username') || "Hitesh123"; // fallback username

const units = ref([]);
const scores = ref([]);

// Merge units with scores + images
const unitsWithScores = computed(() =>
  units.value.map(unit => {
    const scoreObj = scores.value.find(s => s.course_id === unit.course_id);
    return {
      ...unit,
      score: scoreObj?.marks_scored !== null && scoreObj ? `${scoreObj.marks_scored}%` : "--", // fallback text
      image: getUnitImage(unit.course_id),
    };
  })
);

onMounted(async () => {
  try {
    // Fetch all units (titles, descriptions)
    const unitsRes = await axios.get(`${API_BASE}/course`);
    units.value = unitsRes.data.course_detail || [];

    // Fetch scores for current user
    const scoresRes = await axios.get(`${API_BASE}/user_courses/${currentUserId}`);
    scores.value = scoresRes.data.courses || [];
  } catch (err) {
    console.error('Error fetching data:', err);
  }
});

// Images in your /src/assets folder
const unitImages = {
  1: new URL('@/assets/unit1.png', import.meta.url).href,
  2: new URL('@/assets/unit2.png', import.meta.url).href,
  3: new URL('@/assets/unit3.png', import.meta.url).href,
  4: new URL('@/assets/unit4.png', import.meta.url).href,
  5: new URL('@/assets/unit5.png', import.meta.url).href,
  6: new URL('@/assets/unit6.png', import.meta.url).href,
  7: new URL('@/assets/unit7.png', import.meta.url).href,
  8: new URL('@/assets/unit8.png', import.meta.url).href,
  9: new URL('@/assets/unit9.png', import.meta.url).href,
  10: new URL('@/assets/unit10.png', import.meta.url).href,
  11: new URL('@/assets/unit11.png', import.meta.url).href,
  12: new URL('@/assets/unit12.png', import.meta.url).href
};

const getUnitImage = (id) => {
  return unitImages[id] || new URL('@/assets/default.png', import.meta.url).href;
};
</script>


<style scoped>
.learn-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  min-height: 100vh;
  height: 100vh;
  font-family: 'Poppins', sans-serif;
  padding-bottom: 80px;
}

.main-content {
  flex: 1;
  display: flex;
  padding: 0 32px;
  align-items: center;
  width: 100%;
}

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 22px;
  margin-bottom: 18px;
  background: none;
  border: none;
  box-shadow: none;
}

.page-heading-box {
  width: 90%;
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
  background: #ffffff4d;
  margin: 5px 32px 0 32px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 550px;
  padding: 15px 40px 35px 40px;
  overflow-y: auto;
}

.unit-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); /* 2 per row */
  gap: 25px;
  width: 100%;
  margin-top: 20px;
}

.unit-card {
  background-color: #ffddc859;
  border-radius: 15px;
  border: 2px solid #ffddc859;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.unit-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.unit-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}


.unit-divider {
  height: 2px;
  width: 100%;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.1));
  margin: 2px 0 15px 0;
  border: none;
}

.unit-header h3 {
  font-size: 1.3rem;
  background: #c13e79; /* Deep berry pink */
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}

.unit-description {
  font-size: 0.8rem;
  font-weight: 500;
  color: #00000088;
  text-shadow: 1px 1px 4px rgba(255, 255, 255, 0.2);
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  justify-content: flex-end; /* Aligns button to right */
  margin-top: auto; /* Pushes button to the bottom of card */
}

.score-box {
  border: 2px solid transparent; /* Reserve space for border */
  border-radius: 8px;
  background: linear-gradient(#ffddc8, #ffddc8) padding-box, /* Inner bg */
              linear-gradient(90deg, #c13e79, #ff6fa0) border-box; /* Border gradient */
  color: #c13e79;
  padding: 6px 12px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.start-button {
  background: linear-gradient(90deg, #c13e79, #ff6fa0); /* Berry pink → softer pink */
  color: #fff;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: background-color 0.3s ease;
}

.start-button:hover {
  background: #b02e6a; /* Darker berry hover */
}

</style>