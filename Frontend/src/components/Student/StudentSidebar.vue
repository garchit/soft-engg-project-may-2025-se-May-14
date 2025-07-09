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
            to="/student-lectures" 
            class="nav-link" 
            :class="{ active: activeLink === 'LEARN' }"
            @click="setActiveLink('student-lectures')"
          >
            LEARN
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            to="/student-practice" 
            class="nav-link" 
            :class="{ active: activeLink === 'PRACTICE' }"
            @click="setActiveLink('student-practice')"
          >
            PRACTICE
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeLink = ref('home');

const setActiveLink = (linkName) => {
  activeLink.value = linkName;
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh; /* Full height */
  background-color: rgba(255, 255, 255, 0.659);
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
  margin: 0;
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
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background-color: #e54c9196;
  text-decoration: none;
}

.nav-link.active {
  background-color: #81AB40;
  color: #e54c917b;
}

.nav-link.active:hover {
  color: #E54C91;
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