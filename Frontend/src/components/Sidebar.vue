<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li class="nav-item">
          <a 
            href="#" 
            class="nav-link" 
            :class="{ active: activeLink === 'home' }"
            @click="setActiveLink('home')"
          >
            Home
          </a>
        </li>
        <li class="nav-item">
          <a 
            href="#" 
            class="nav-link" 
            :class="{ active: activeLink === 'about' }"
            @click="setActiveLink('about')"
          >
            About
          </a>
        </li>
        <li class="nav-item">
          <a 
            href="#" 
            class="nav-link" 
            :class="{ active: activeLink === 'services' }"
            @click="setActiveLink('services')"
          >
            Services
          </a>
        </li>
        <li class="nav-item">
          <a 
            href="#" 
            class="nav-link" 
            :class="{ active: activeLink === 'contact' }"
            @click="setActiveLink('contact')"
          >
            Contact
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeLink = ref('home')

const setActiveLink = (linkName) => {
  activeLink.value = linkName
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #FFC800;
  position: fixed;
  left: 0;
  top: 0;
  padding: 0; /* Remove padding to avoid offset */
  font-family: 'Poppins', sans-serif;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex; /* Add flexbox to the sidebar */
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center items vertically */
  align-items: center; /* Center items horizontally */
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
  color: white;
  font-size: 20px;
  font-weight: 500;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #E54C91;
  text-decoration: none;
}

.nav-link.active {
  background-color: #58CC02;
  color: white;
}

.nav-link.active:hover {
  color: #E54C91;
}

/* Responsive design */
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