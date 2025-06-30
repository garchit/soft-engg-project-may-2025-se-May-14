<template>
    <div ref="backgroundRef" class="interactive-background">
      <Navbar class="navbar" />
  
      <div
        v-for="ripple in ripples"
        :key="ripple.id"
        class="ripple"
        :style="{ left: ripple.x + 'px', top: ripple.y + 'px' }"
      ></div>
  
      <div class="student-page">
        <StudentSidebar />
  
        <div class="student-content">
            <h1 class="dashboard-title" style="text-align: center; color: white;">HOME</h1><br /><br />
  
          <div class="main-container">
              <div class="donut-chart-section">
              <div class="donut-chart-container">
                <DonutChart :progress="80" />
              </div>
              <div style="width: 40px;"></div> 
              <div class="rank">
                <h2 style="color: white; text-align: center;">Rank: 1</h2>
              </div>
              <div class="calendar-wrapper">
                <StreakCalendar />
              </div>
            
            </div>
  
            <h2 class="insights-header" style="text-align: center; color: white; font-weight: bold; font-size: 1.5em;margin-top: 20px; margin-bottom: 2px;">Units Completed</h2>
            <div class="charts-section">
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
                <CCardImage orientation="center" src="/src/assets/demand&supply.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 5px;">
                  <CCardText>Demand & Supply</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                <CCardImage orientation="center" src="/src/assets/borrowing.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 10px;">
                  <CCardText>Borrowing</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                <CCardImage orientation="center" src="/src/assets/budgeting.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 10px;">
                  <CCardText>Budgeting</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
                <CCardImage orientation="center" src="/src/assets/personal finance.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 5px;">
                  <CCardText>Personal Finance</CCardText>
                </CCardBody>
                </CCard>
            </div>

  
            <h2 class="insights-header" style="text-align: center; color: white;font-weight: bold; font-size: 1.5em; margin-top: 20px; margin-bottom: 2px;">Recommended For You</h2>
            <div class="charts-section">
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
                <CCardImage orientation="center" src="/src/assets/demand&supply.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 5px;">
                  <CCardText>Demand & Supply</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                <CCardImage orientation="center" src="/src/assets/borrowing.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 10px;">
                  <CCardText>Borrowing</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                <CCardImage orientation="center" src="/src/assets/budgeting.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 10px;">
                  <CCardText>Budgeting</CCardText>
                </CCardBody>
                </CCard>
                <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
                <CCardImage orientation="center" src="/src/assets/personal finance.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
                <CCardBody style="text-align: center; padding: 5px;">
                  <CCardText>Personal Finance</CCardText>
                </CCardBody>
                </CCard>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import Navbar from './Navbar.vue'; 
  import StreakCalendar from './Calendar.vue';
  import StudentSidebar from './StudentSidebar.vue';
  import { CCard, CCardImage, CCardBody, CCardText } from '@coreui/vue';
  import DonutChart from '../donutChart.vue'; 
  import demandSupplyImage from '@/assets/demand&supply.jpg';
  

  const backgroundRef = ref(null);
  const ripples = ref([]);
  let rippleId = 0;
  
  const createRipple = (event) => {
    const rect = backgroundRef.value.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
  
    const newRipple = { id: rippleId++, x, y, opacity: 1 };
    ripples.value.push(newRipple);
  
    setTimeout(() => {
      const index = ripples.value.findIndex((r) => r.id === newRipple.id);
      if (index > -1) ripples.value.splice(index, 1);
    }, 1000);
  };
  
  const updateBackgroundColor = (event) => {
    if (!backgroundRef.value) return;
    const rect = backgroundRef.value.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
  
    backgroundRef.value.style.background = `
      radial-gradient(circle at ${x}% ${y}%,
        rgba(255, 200, 0, 0.6) 0%,
        rgba(229, 76, 145, 0.5) 50%,
        rgba(128, 123, 123, 0.4) 100%
      )
    `;
  };
  
  const handleMouseMove = (event) => updateBackgroundColor(event);
  const handleClick = (event) => createRipple(event);
  
  onMounted(() => {
    if (backgroundRef.value) {
      backgroundRef.value.addEventListener('mousemove', handleMouseMove);
      backgroundRef.value.addEventListener('click', handleClick);
    }
  });
  
  onUnmounted(() => {
    if (backgroundRef.value) {
      backgroundRef.value.removeEventListener('mousemove', handleMouseMove);
      backgroundRef.value.removeEventListener('click', handleClick);
    }
  });
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  
  .interactive-background {
    width: 100%;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    transition: background 0.3s ease;
    font-family: 'Poppins', sans-serif;
  }
  
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: #ffffffac; /* Navbar background color */
    z-index: 1000;
    display: flex;
    padding: 0 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .ripple {
    position: absolute;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: ripple-fade 1s ease-out;
  }
  
  @keyframes ripple-fade {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 0.9;
    }
    100% {
      transform: translate(-50%, -50%) scale(4);
      opacity: 0;
    }
  }
  
  .student-page {
    display: flex;
    flex-direction: row;
    padding-top: 60px; 
  }
  
  .student-content {
    flex: 1;
    padding: 20px;
    margin-left: 250px; 
  }
  
  .main-container {
    background: rgba(255, 255, 255, 0.303);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(86, 83, 83, 0.2);
    margin: 20px auto;
    width: 90%;
    height: auto;
  }
  
  .calendar-wrapper {
    margin-top: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40%;
  }
  
  .donut-chart-section {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .donut-chart-container {
    width: 300px;
    height: 300px;
  }
  
  .charts-section {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 20px;
    border: 10px solid #E54C91; 
    background-color: rgba(250, 250, 250, 0.747);
    border-radius: 15px; 
    padding: 20px;
  }
  
  .unit-card {
    width: 150px;
    height: 100px;
    background: linear-gradient(135deg, #a628b192, #3059a190, #5298b0a8); 
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 10px;
  }
  
  .rank {
    background-color: #7AC70C;
    padding: 10px;
    border-radius: 10px;
    color: white;
    margin-top: 20px;
    text-align: center;
    width: 20%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>