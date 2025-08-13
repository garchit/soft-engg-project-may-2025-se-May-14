<template>
  <aside class="sidebar">
    <nav class="nav-links">
      <ul class="nav-list">
        <li class="nav-item"><router-link :to="`/${instituteId}/institute-home`" class="nav-link" exact-active-class="active">HOME</router-link></li>

      <!-- Teachers Dropdown -->
      <li class="nav-item">
        <div class="dropdown">
          <div class="dropdown-header">
            <div class="dropdown-title" @click="toggleDropdown">
              <span>TEACHERS
              <i :class="['bi', isOpen ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
            </span></div>
            <button @click.stop="showAddTeacherForm" class="round-button" title="Add Teacher" >+</button>
          </div>

          <ul v-if="isOpen" class="dropdown-menu">
            <li v-if="teachers.length === 0" class="dropdown-item no-teachers">
              No Teachers Added
            </li>
            <li v-else v-for="teacher in teachers" :key="teacher.id" class="teacher-item">
              <router-link 
                :to="{
                  path: `/${instituteId}/teacher-progress/${teacher.id}`, 
                  query: { name: teacher.name }
                }" 
                class="dropdown-item"
                :class="{ active: route.params.teacher_id === String(teacher.id) }"
              >
                {{ teacher.name }} 
                <span class="class-tag">Class {{ teacher.class }}</span>
              </router-link>
            </li>
          </ul>
        </div>
      </li>

      <li><router-link :to="`/${instituteId}/verify-students`" class="nav-link" exact-active-class="active">STUDENTS</router-link></li>
      <li><router-link :to="`/${instituteId}/institute-profile`" class="nav-link" exact-active-class="active">PROFILE</router-link></li>
    </ul></nav>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

const isOpen = ref(false)
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const teachers = ref([])
const toast = useToast()
const route = useRoute() 
const instituteId = route.params.institute_id

// When + is clicked, tell parent to open the form
const showAddTeacher = ref(false)
const emit = defineEmits(['add-teacher'])
const showAddTeacherForm = () => {
  emit('add-teacher')
}

// Get all the teachers of the institute
onMounted(async () => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/institute_wise_teachers/${instituteId}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch teachers: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    
    teachers.value = data.teachers

  } catch (error) {
    toast.error(`Error fetching teacher data: ${error.message}`)
    teachers.value = [] 
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/?family=Poppins:wght@400;500;600&display=swap');

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

.nav-links {
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
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background-color: #e54c9164 !important;
}

.dropdown {
  width: 100%;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  user-select: none;
  position: relative;
  z-index: 10;
}

.dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  border-radius: 6px;
}

.dropdown-header:hover {
  background-color: #e54c9164;
}

.dropdown-header span {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}

.dropdown-title {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #fff;
  font-size: 17px;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
  text-decoration: none;
}
.dropdown-menu {
  margin-top: 8px;
  padding-left: 12px;
  display: flex;
  background: transparent;
  flex-direction: column;
  gap: 8px;
  list-style: none;
  position: relative;
  z-index: 20;
  font-family: 'Poppins', sans-serif;
  padding: 8px 12px;
  max-height: 250px;
  overflow-y: auto;
  width: 100%;
  border: none; /* Remove border */
}

.round-button {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.75);
  color: #e54c91;
  font-size: 18px;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
}

.round-button:hover {
  background-color: rgba(255, 255, 255, 0.9);
}

.teacher-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  color: #ffffff;
  width: 100%;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
  display: block; 
}

.dropdown-item:hover {
  background-color: #e54c9164; 
  color: #fff
}

.dropdown-item.active {
  background-color: #ffffff73;
  font-weight: 600;
  color: #e54c91;
}

.bi {
  color: white;
  user-select: none;
  font-size: 1.0em;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.5), 0 0 5px rgba(0, 0, 0, 0.5); /* Adjust values as needed */

}

@media (max-width: 576px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    box-shadow: none;
    top: 0;
  }

  .nav-links {
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
