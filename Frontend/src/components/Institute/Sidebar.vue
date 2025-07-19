<template>
  <aside class="sidebar">
    <h2 class="title">SAVVY</h2>
    <nav class="nav-links">
      <router-link :to="`/${instituteId}/institute-home`" class="nav-link" exact-active-class="active">Home</router-link>

      <!-- Teachers Dropdown -->
      <div class="dropdown">
        <div @click="toggleDropdown" class="dropdown-header nav-link">
          <span>Teachers</span>
          <i :class="['bi', isOpen ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
        </div>
        <ul v-if="isOpen" class="dropdown-menu">
          <li v-for="teacher in teachers" :key="teacher.id">
            <router-link 
              :to="{
                path: `/${instituteId}/teacher-progress/${teacher.id}`, 
                query: { name: teacher.name }
              }" 
              class="dropdown-item" 
              :class="{ active: route.params.teacher_id === String(teacher.id) }"
            >
              {{ teacher.name }}(Class: {{ teacher.class }})
            </router-link>
          </li>
        </ul>
      </div>

      <router-link :to="`/${instituteId}/verify-students`" class="nav-link" exact-active-class="active">Students</router-link>
      <router-link to="/profile" class="nav-link" exact-active-class="active">Profile</router-link>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const isOpen = ref(false)
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const teachers = ref([])
const route = useRoute() 
const instituteId = route.params.institute_id

onMounted(async () => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/institute_wise_teachers/${instituteId}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch teachers: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    
    teachers.value = data.teachers

  } catch (error) {
    console.error('Error fetching teacher data:', error)
    alert(`Error fetching teacher data: ${error.message}`)
    teachers.value = [] 
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.sidebar {
  min-width: 250px;
  width: 250px;
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 20px 24px;
  border-right: 1px solid #e5e7eb;
  height: 100vh;
  position: sticky;
  top: 0;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 32px;
  user-select: none;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.nav-link {
  text-decoration: none;
  font-size: 1rem;
  color: #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.25s ease, color 0.25s ease;
  user-select: none;
}

.nav-link:hover {
  background-color: #e2e8f0;
}

.nav-link.active {
  background: white;
  font-weight: 600;
  box-shadow: 0 0 8px rgb(14 165 233 / 0.5);
}

.dropdown {
  display: flex;
  flex-direction: column;
  user-select: none;
  position: relative;
  z-index: 10;
}

.dropdown-header {
  cursor: pointer;
  font-weight: 400;
  color: #334155;
  padding: 10px 16px;
  border-radius: 8px;
  background-color: transparent;
  transition: background-color 0.25s ease;
}

.dropdown-header:hover {
  background-color: #e2e8f0;
}

.dropdown-header span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dropdown-menu {
  margin-top: 8px;
  padding-left: 12px;
  border-left: 2px solid #0ea5e9;
  display: flex;
  flex-direction: column;
  gap: 8px;
  list-style: none;
  position: relative;
  z-index: 20;
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: 250px;
  overflow-y: auto;
}

/* Custom scrollbar styling for dropdown */
.dropdown-menu::-webkit-scrollbar {
  width: 6px;
}
.dropdown-menu::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}
.dropdown-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}
.dropdown-menu::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.dropdown-item {
  font-size: 0.95rem;
  color: #475569;
  width: 100%;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
  display: block; 
}

.dropdown-item:hover {
  background-color: #dbeafe; 
}

.dropdown-item.active {
  background-color: white;
  font-weight: 600;
  color: #475569;
  box-shadow: 0 0 8px rgb(14 165 233 / 0.5);
}

.badge {
  background-color: #0ea5e9;
  color: white;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 9999px;
}

.bi {
  font-size: 1.2rem;
  color: grey;
  user-select: none;
}
</style>
