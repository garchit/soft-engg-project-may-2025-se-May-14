<template>
  <InteractiveLayout>
  <div class="main-content">
    <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">Leaderboard</div>
          <div class="page-caption">
            Monitor your rank and stay motivated to keep earning more points.
          </div>
        </div>
        <div class="your-rank-box" v-if="currentUser">
          <div class="rank-title">Your Rank</div>
          <div class="rank-info">
            <div class="rank-number">{{ currentUser.rank }}</div>
          </div>
          <div class="progress-info">
            Rank up in {{ pointsToNextRank }} XP
          </div>
        </div>
      </header>
  <div class="leaderboard-container">  
    <!-- Top 3 Rectangular Tiles -->
    <div class="top-three-container">
      <div class="top-card silver" v-if="rankedStudents[1]">
        <div class="medal-icon">🥈</div>
        <div class="info">
          <div class="name">{{ rankedStudents[1].username }}</div>
          <div class="score">{{rankedStudents[1].score}} XP</div>
        </div>
      </div>
      <div class="top-card gold" v-if="rankedStudents[0]">
        <div class="medal-icon">🥇</div>
        <div class="info">
          <div class="name">{{ rankedStudents[0].username }}</div>
          <div class="score">{{rankedStudents[0].score}} XP</div>
        </div>
      </div>
      <div class="top-card bronze" v-if="rankedStudents[2]">
        <div class="medal-icon">🥉</div>
        <div class="info">
          <div class="name">{{ rankedStudents[2].username }}</div>
          <div class="score">{{rankedStudents[2].score}} XP</div>
        </div>
      </div>
    </div>

    <!-- Scrollable Leaderboard Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>RANK</th>
            <th>USERNAME</th>
            <th>SCORE</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stud in rankedStudents.slice(3)" :key="stud.username">
            <td>{{ stud.rank }}</td>
            <td>{{ stud.username }}</td>
            <td>{{ stud.score > 0 ? stud.score + ' XP' : 'No XP Yet' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
  </InteractiveLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from 'axios';
import InteractiveLayout from '../InteractiveLayout.vue';

const studentData = ref([]);
const currentUser = ref({});
const pointsToNextRank = ref(0);
const currentUsername = localStorage.getItem('username') || "Hitesh123";
const API_BASE = "/Finance_Tutor";

async function fetchLeaderboard() {
  try {
    const res = await axios.get(`${API_BASE}/user_leaderboard`);
    console.log("Leaderboard API Response:", res.data);
    studentData.value = res.data.leaderboard || [];
  } catch (err) {
    console.error("Failed to fetch leaderboard:", err);
  }
}

async function fetchCurrentUserRank() {
  try {
    const res = await axios.get(`${API_BASE}/user_rank/${currentUsername}`);
    console.log("Current User API Response:", res.data);
    currentUser.value = res.data || {};
    pointsToNextRank.value = res.data.points_to_next_rank || 0;
  } catch (err) {
    console.error("Failed to fetch current user rank:", err);
  }
}

const rankedStudents = computed(() => {
  return studentData.value.map((s, i) => ({
    ...s,
    rank: s.rank,
    score: s.rewards ?? 0
  }));
});

onMounted(() => {
  console.log("Leaderboard component mounted");
  fetchLeaderboard();
  fetchCurrentUserRank();
});
</script>

<style scoped>
/* MAIN CONTAINER */
.leaderboard-container {
  width: 100%;
  background: #ffffff4d;
  padding: 30px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  max-height: 550px;
}

/* TITLE */
.main-content {
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
  width: 78%;
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

.your-rank-box {
  padding: 0.9rem 0.9rem;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  text-align: center;
  color: #fff;
  min-width: 200px;
}

.rank-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: -0.6rem;
  color: #ffffffd4;
}

.rank-info {
  font-size: 3rem;
  font-weight: 700;
}

.progress-info {
  margin-top: -0.6rem;
  font-size: 0.9rem;
  color: #ffe07b;
}

/* TOP 3 TILES */
.top-three-container {
  display: flex;
  gap: 40px;
  justify-content: center;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.top-card {
  display: flex;
  align-items: center;
  width: 280px;
  padding: 10px 15px;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-weight: bold;
  font-size: 2rem;
  background: rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.top-card:hover {
  transform: scale(1.05);
}

.medal-icon {
  font-size: 2.5rem;
  margin-right: 20px;
}

.info {
  display: flex;
  flex-direction: column; 
  align-items: flex-start; 
  gap: 1px; 
}

.name {
  font-size: 1rem;
  color: #000000bc;
}

.score {
  font-size: 0.65rem;
  color: #000000bc;
}

.gold {
  border: 3px solid gold;
  background-color: #fff9c4;
  box-shadow: 0 0 15px gold, 0 0 30px rgba(255, 215, 0, 0.5);
  transform: scale(1.1);
}

.silver {
  border: 3px solid silver;
  background-color: #e0e0e0;
  box-shadow: 0 0 10px silver, 0 0 20px rgba(192, 192, 192, 0.4);
}

.bronze {
  border: 3px solid #cd7f32;
  background-color: #ffe0b2;
  box-shadow: 0 0 10px #cd7f32, 0 0 20px rgba(205, 127, 50, 0.4);
}

/* TABLE STYLES */
.table-container {
  max-height: 450px;
  width: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: #ffffff2d;

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

</style>
