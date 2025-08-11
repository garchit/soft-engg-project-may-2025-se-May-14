<template>
  <InteractiveLayout>
    <div class="student-page">

      <div class="student-content">
        <h1 class="dashboard-title" style="text-align: center; font-family: 'poppins'; color: white; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">Welcome, Donna</h1><br /><br />

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

          <h2 class="insights-header" style="text-align: center; font-family: 'poppins'; color: black; font-weight: bold; font-size: 1.5em; margin-top: 50px; margin-bottom: 2px;">Units Completed</h2>
          <div class="charts-section">
            <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
              <CCardImage orientation="center" src="/src/assets/demand&supply.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
              <CCardBody style="text-align: center; padding: 10px;">
                <CCardText>Demand & Supply 
                            Grade: A 
                </CCardText>
                
              </CCardBody>
            </CCard>
            <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
              <CCardImage orientation="center" src="/src/assets/borrowing.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
              <CCardBody style="text-align: center; padding: 10px;">
                <CCardText>Borrowing 
                  Grade S
                </CCardText>

              </CCardBody>
            </CCard>
            <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center;">
              <CCardImage orientation="center" src="/src/assets/budgeting.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
              <CCardBody style="text-align: center; padding: 10px;">
                <CCardText>Budgeting                 
                            Grade A
                </CCardText>
              </CCardBody>
            </CCard>
            <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px;">
              <CCardImage orientation="center" src="/src/assets/personal finance.jpg" style="width: 100%; height: 70%; object-fit: cover;" />
              <CCardBody style="text-align: center; padding: 10px;">
                <CCardText>Personal Finance
                            Grade B
                </CCardText>
              </CCardBody>
            </CCard>
          </div>

          <h2 class="insights-header" style="text-align: center; font-family: 'poppins'; color: black; font-weight: bold; font-size: 1.5em; margin-top: 40px; margin-bottom: 2px;">Recommended For You</h2>
          <div class="charts-section">
            <CCard style="width: 150px; height: 150px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 10px; transition: transform 0.3s ease, box-shadow 0.3s ease;" 
              class="hover-card">
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
  </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Navbar from './Navbar.vue'; 
import StreakCalendar from './Calendar.vue';
import StudentSidebar from './StudentSidebar.vue';
import { CCard, CCardImage, CCardBody, CCardText } from '@coreui/vue';
import DonutChart from '../donutChart.vue'; 
import InteractiveLayout from '../InteractiveLayout.vue';
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.app-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
  position: relative;
  overflow: hidden;
}

.dashboard-title{
  font-family: 'Poppins', sans-serif;
  color: white;
  text-align: center;
  margin-top: 20px;
  font-size: 2.5em;
  font-weight: bold;
  position: absolute;
}

.student-page {
  display: flex;
  flex-direction: row;
  /* padding-top: 60px;  */
}

.student-content {
  flex: 1;
  padding: 20px;
  /* margin-left: 250px;  */
}

.main-container {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  backdrop-filter: blur(50px); 
  border: 1px solid rgba(255, 255, 255, 0.2); 
  padding: 30px;
  border-radius: 15px;
  box-shadow: 5px 10px rgba(30, 29, 29, 0.2);
  /* margin: 20px auto; */
  width: 1000px;
  height: 1000px;
  justify-content: center;
  align-items: center;
  position: relative;
  left: 60%;
  transform: translateX(-50%);
}



.calendar-wrapper {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  margin-right: 20px;
  align-items: center;
  width: 300px;
  height: 200px;
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Add smooth transition for hover effects */
}

.calendar-wrapper:hover {
  transform: scale(1.1); /* Slightly enlarge the element */
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3); /* Add a more prominent shadow */
}



.donut-chart-section {
  display: flex;
  justify-content: space-around; /* Distribute elements evenly with equal spacing */
  align-items: center; /* Align elements vertically in the center */
  margin-bottom: 20px;
  font-family: 'poppins', sans-serif;
  color: black;
  margin-left: 20px; /* Add left margin for spacing */
}

.donut-chart-container {
  width: 300px; 
  height: 300px; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  transition: transform 0.3s ease, box-shadow 0.3s ease; 
  overflow: hidden; 
}

.donut-chart-container:hover {
  transform: scale(1.1); /* Slightly enlarge the element */
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3); /* Add a more prominent shadow */
}

.charts-section {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 20px;
  border: 10px solid #c7427e; 
  background-color: rgba(250, 250, 250, 0.747);
  box-shadow: 0 10px 30px #96325fae;
  border-radius: 15px; 
  padding: 20px;
}



.rank {
  background-color: rgb(222, 189, 4);
  padding: 10px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
  width: 20%;
  box-shadow: 1px 10px rgb(189, 161, 2);
  margin-right: 60px;
  font-family: 'poppins', sans-serif;
  margin-left: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.rank:hover {
  transform: scale(1.1); 
  box-shadow: 0 15px 30px rgba(189, 161, 2, 0.5); 
}
</style>