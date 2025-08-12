<template>
  <div class="calendar-container">
    <div class="streak-display">
      <span class="streak-number">{{ currentStreak }}</span>
      <span class="streak-label">{{ currentStreak === 1 ? 'Day' : 'Days' }} Streak 🔥</span>
    </div>

    <div class="calendar-header">
      <span @click="goToPrevMonth" class="arrow">&lt;</span>
      <h2>{{ currentMonthName }} {{ currentYear }}</h2>
      <span @click="goToNextMonth" class="arrow">&gt;</span>
    </div>

    <div class="calendar-grid">
      <div class="day-name" v-for="day in daysOfWeek" :key="day">{{ day }}</div>
      <div
        v-for="(day, index) in calendarDays"
        :key="index"
        :class="['calendar-day', { 'blank': !day.day }]"
      >
        <span v-if="day.streak" class="fire">🔥</span>
        <span class="day-number">{{ day.day }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineExpose } from 'vue';
import axios from 'axios'; // Using axios for consistency

// --- STATE ---
const daysOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
const currentMonth = ref(new Date().getMonth());
const currentYear = ref(new Date().getFullYear());
const streakDates = ref(new Set());
const currentStreak = ref(0);
const API_BASE = "/Finance_Tutor"; // Using the proxied path

// --- API CALL ---
const fetchStreakData = async () => {
  try {
    const response = await axios.get(`${API_BASE}/user/streak/calendar`);
    const data = response.data;
    
    if (data.checkins) {
      streakDates.value = new Set(data.checkins);
    }
    if (data.streak) {
      currentStreak.value = data.streak;
    }

  } catch (error) {
    console.error("Error fetching streaks:", error.response ? error.response.data : error.message);
  }
};

// --- LIFECYCLE HOOK ---
onMounted(() => {
  // This will be called by the parent component (StudentHome) after check-in
  // but we can leave the initial call here as well.
  fetchStreakData();
});

defineExpose({
  fetchStreakData
});

// --- CALENDAR LOGIC ---
const calendarDays = computed(() => {
  const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay();
  const days = [];
  for (let i = 0; i < firstDay; i++) { days.push({ day: '', streak: false }); }
  for (let i = 1; i <= daysInMonth; i++) {
    const isoDate = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    days.push({ day: i, streak: streakDates.value.has(isoDate) });
  }
  return days;
});

const currentMonthName = computed(() => new Date(currentYear.value, currentMonth.value).toLocaleString('default', { month: 'long' }));
const goToPrevMonth = () => { if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value--; } else { currentMonth.value--; } };
const goToNextMonth = () => { if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++; } else { currentMonth.value++; } };
</script>

<style scoped>
/* ALL YOUR ORIGINAL CSS IS PRESERVED */
.streak-display { text-align: center; margin-bottom: 15px; padding: 8px; background: rgba(229, 76, 145, 0.1); border-radius: 10px; }
.streak-number { font-size: 1.8rem; font-weight: 700; color: #E54C91; display: block; }
.streak-label { font-size: 0.9rem; font-weight: 500; color: #333; }
.calendar-container { font-family: 'Poppins', sans-serif; padding: 15px; background: rgba(255, 255, 255, 0.4); border-radius: 15px; color: #333; width: 100%; max-width: 320px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); box-sizing: border-box; }
.calendar-header { display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1rem; padding: 0 5px; margin-bottom: 10px; }
.arrow { cursor: pointer; font-size: 1.5rem; color: #E54C91; transition: transform 0.2s ease; }
.arrow:hover { transform: scale(1.2); }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; text-align: center; }
.day-name { font-weight: 600; font-size: 0.7rem; color: #555; padding-bottom: 5px; }
.calendar-day { background: rgba(255, 255, 255, 0.5); border-radius: 8px; aspect-ratio: 1 / 1; display: flex; justify-content: center; align-items: center; position: relative; font-size: 0.85rem; font-weight: 500; transition: background-color 0.3s, transform 0.3s; }
.calendar-day:not(.blank):hover { background-color: rgba(255, 255, 255, 0.9); transform: scale(1.05); }
.calendar-day.blank { background: transparent; }
.day-number { z-index: 1; }
.fire { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 2rem; opacity: 0.75; z-index: 0; pointer-events: none; }
</style>