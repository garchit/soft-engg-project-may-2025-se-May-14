<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li class="nav-item">
          <router-link 
            to="/student-home" 
            class="nav-link" 
            :class="{ active: activeLink === 'HOME' }"
            @click="setActiveLink('home')"
          >
            HOME
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            to="/student-learn" 
            class="nav-link" 
            :class="{ active: activeLink === 'LEARN' }"
            @click="setActiveLink('student-learn')"
          >
            LEARN
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            to="/student-practice-content" 
            class="nav-link" 
            :class="{ active: activeLink === 'PRACTICE' }"
            @click="setActiveLink('student-practice')"
          >
            PRACTICE
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            to="/student-leaderboard" 
            class="nav-link" 
            :class="{ active: activeLink === 'LEADERBOARD' }"
            @click="setActiveLink('student-leaderboard')"
          >
            LEADERBOARD
          </router-link>
        </li>
          <li class="nav-item">
          <router-link 
            to="/student-profile" 
            class="nav-link" 
            :class="{ active: activeLink === 'PROFILE' }"
            @click="setActiveLink('studentprofile')"
          >
            PROFILE
          </router-link>
        </li>
      </ul>
    </nav>
     <div class="mascot-container">
      <div class="speech-bubble">
        ASK ME ANYTHING!
      </div>
      <div class="mascot" @click="handleMascotClick">
        <img src="/src/assets/ReviseAvatar.png" alt="Savvy Mascot" class="mascot-face" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeLink = ref('home');

const setActiveLink = (linkName) => {
  activeLink.value = linkName;
};

const handleMascotClick = () => {
  alert('This feature will be available soon!');
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh; /* Full height */
  background-color: #ffffff4b;
  position: fixed;
  left: 0;
  top: 0; /* Start from the top */
  padding: 0;
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 900; /* Lower than Navbar */
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin-bottom: 0px;
  width: 100%;
}

.nav-item {
  width: 100%;
  margin-bottom: 10px;
}

.nav-link {
  display: block;
  width: 100%;
  padding: 15px 20px;
  text-decoration: none;
  color: #ffffff !important;
  font-size: 17px;
  text-align: center !important;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background-color: #e54c9164 !important;
}

.nav-link.active {
  background-color: #81AB40;
  color: #e54c917b;
}

.nav-link.active:hover {
  color: #E54C91;
}

.mascot-container {
  position: absolute;
  bottom: 5px; 
  left: 17%;
  text-align: center;
}

.speech-bubble {
  background: #4a90e2;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: center;
  position: relative;
  margin-bottom: -2rem;
}

.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 20%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-top: 12px solid #4a90e2;
}

.mascot {
  display: flex;
  justify-content: center;
}

.mascot-face {
  width: 110px;
  height: auto;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

.mascot-face:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }

  .nav-link {
    font-size: 18px;
    padding: 12px 15px;
  }
}

@media (max-width: 576px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    box-shadow: none;
    top: 0;
  }

  .sidebar-nav {
    flex-direction: row;
    padding-top: 20px;
  }

  .nav-list {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
  }

  .nav-item {
    flex: 1;
    margin-bottom: 0;
  }

  .nav-link {
    font-size: 16px;
    padding: 10px 5px;
  }
}
</style>