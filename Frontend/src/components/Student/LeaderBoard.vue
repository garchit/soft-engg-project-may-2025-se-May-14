<template>
  <div class="leaderboard-main-container">
    <h1>LEADERBOARD</h1>

    <!-- Top 3 Rectangular Tiles -->
    <div class="top-three-container">
      <div class="top-card gold" v-if="rankedStudents[0]">
        <div class="medal-icon">🥇</div>
        <div class="info">
          <div class="name">{{ rankedStudents[0].username }}</div>
          <div class="score">{{ rankedStudents[0].score }}</div>
        </div>
      </div>
      <div class="top-card silver" v-if="rankedStudents[1]">
        <div class="medal-icon">🥈</div>
        <div class="info">
          <div class="name">{{ rankedStudents[1].username }}</div>
          <div class="score">{{ rankedStudents[1].score }}</div>
        </div>
      </div>
      <div class="top-card bronze" v-if="rankedStudents[2]">
        <div class="medal-icon">🥉</div>
        <div class="info">
          <div class="name">{{ rankedStudents[2].username }}</div>
          <div class="score">{{ rankedStudents[2].score }}</div>
        </div>
      </div>
    </div>

    <!-- Scrollable Leaderboard Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>USERNAME</th>
            <th>RANK</th>
            <th>SCORE</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stud in rankedStudents.slice(3)" :key="stud.username">
            <td>{{ stud.username }}</td>
            <td>{{ stud.rank }}</td>
            <td>{{ stud.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';

let studentData = ref([]);

const rankedStudents = computed(() => {
  return [...studentData.value]
    .sort((a, b) => b.score - a.score)
    .map((s, i) => ({ ...s, rank: i + 1 }));
});

onMounted(() =>
  studentData.value = [
    { username: "alice", score: 87 },
    { username: "bob", score: 72 },
    { username: "charlie", score: 93 },
    { username: "diana", score: 65 },
    { username: "edward", score: 78 },
    { username: "fiona", score: 88 },
    { username: "george", score: 91 },
    { username: "hannah", score: 69 },
    { username: "ian", score: 74 },
    { username: "julia", score: 82 },
    { username: "kyle", score: 67 },
    { username: "laura", score: 95 },
    { username: "mike", score: 80 },
    { username: "nina", score: 84 },
    { username: "oliver", score: 76 },
    { username: "paula", score: 90 },
    { username: "quentin", score: 66 },
    { username: "rachel", score: 79 },
    { username: "sam", score: 70 },
    { username: "tina", score: 83 },
    { username: "ursula", score: 68 },
    { username: "victor", score: 86 },
    { username: "wendy", score: 73 },
    { username: "xander", score: 89 },
    { username: "yasmine", score: 77 }
  ]
);
</script>

<style scoped>
/* MAIN CONTAINER */
.leaderboard-main-container {
  width: 90%;
  max-width: 1200px;
  margin: 40px auto;
  background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
  padding: 30px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* TITLE */
h1 {
  font-size: 52px;
  font-weight: bold;
  margin-bottom: 30px;
}

/* TOP 3 TILES */
.top-three-container {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 40px;
}

.top-card {
  display: flex;
  align-items: center;
  width: 280px;
  padding: 20px 25px;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-weight: bold;
  font-size: 20px;
  background: rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.top-card:hover {
  transform: scale(1.05);
}

.medal-icon {
  font-size: 50px;
  margin-right: 20px;
}

.info {
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 22px;
  color: #111;
}

.score {
  font-size: 18px;
  color: #444;
}

.gold {
  border: 3px solid gold;
  background-color: #fff9c4;
}

.silver {
  border: 3px solid silver;
  background-color: #e0e0e0;
}

.bronze {
  border: 3px solid #cd7f32;
  background-color: #ffe0b2;
}

/* TABLE STYLES */
.table-container {
  max-height: 450px;
  width: 100%;
  overflow-y: auto;
  border-radius: 15px;
  box-shadow: 10px 10px 20px rgba(0,0,0,0.15);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  font-size: 20px;
  color: #000;
}

thead {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.3);
}

th {
  padding: 20px;
  font-weight: 600;
  font-size: 1.2em;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

td {
  padding: 20px;
}

tr {
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

tr:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.01);
}

</style>
