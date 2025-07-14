<template>
    <div class="calendar-container">
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
          class="calendar-day"
        >
          <span v-if="day.streak" class="fire">🔥</span>
          <span class="day-number">{{ day.day }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  
  const daysOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  
  const today = new Date();
  const currentMonth = ref(today.getMonth());
  const currentYear = ref(today.getFullYear());
  
  const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };
  
  const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month, 1).getDay();
  };
  
  const generateCalendarDays = (month, year) => {
    const daysInMonth = getDaysInMonth(month, year);
    const firstDay = getFirstDayOfMonth(month, year);
  
    const days = [];
  
    for (let i = 0; i < firstDay; i++) {
      days.push({ day: '', streak: false });
    }
  
    for (let i = 1; i <= daysInMonth; i++) {
      // Simulate streaks on random days for now
      const streak = Math.random() > 0.5;
      days.push({ day: i, streak });
    }
  
    return days;
  };
  
  const calendarDays = computed(() =>
    generateCalendarDays(currentMonth.value, currentYear.value)
  );
  
  const currentMonthName = computed(() =>
    new Date(currentYear.value, currentMonth.value).toLocaleString('default', {
      month: 'long',
    })
  );
  
  const goToPrevMonth = () => {
    if (currentMonth.value === 0) {
      currentMonth.value = 11;
      currentYear.value--;
    } else {
      currentMonth.value--;
    }
  };
  
  const goToNextMonth = () => {
    if (currentMonth.value === 11) {
      currentMonth.value = 0;
      currentYear.value++;
    } else {
      currentMonth.value++;
    }
  };
  </script>
  
  <style scoped>
  .calendar-container {
    margin-top: 30px;
    padding: 20px;
    background: #1b1b1b;
    border-radius: 20px;
    color: white;
    width: 300px;
    height: 300px;
    margin-left: auto;
    margin-right: auto;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 1.1rem;
  }
  
  .arrow {
    cursor: pointer;
    font-size: 1.5rem;
  }
  
  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
    text-align: center;
    font-size: 0.75rem;
    flex-grow: 1;
    margin-top: 10px;
  }
  
  .day-name {
    font-weight: bold;
    padding: 4px 0;
    word-break: break-word;
  }
  
  .calendar-day {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    aspect-ratio: 1 / 1;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
  }
  
  .day-number {
    z-index: 1;
    position: relative;
    font-size: 0.9rem;
  }
  
  .fire {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 2rem;
    opacity: 0.7;
    pointer-events: none;
    z-index: 0;
  }
  </style>
  