<template>
  <div ref="backgroundRef" class="layout-page">
    <Navbar class="navbar"/>
    <div
      v-for="ripple in ripples"
      :key="ripple.id"
      class="ripple"
      :style="{ left: ripple.x + 'px', top: ripple.y + 'px' }"
    ></div>
    
    <div class="layout">
      <Sidebar @add-teacher="showAddTeacher = true" />

      <main class="main-content">
        <!-- Overlay Form -->
        <div v-if="showAddTeacher" class="overlay">
          <div class="form-box">
            <h3 class="form-title">Add Teacher</h3>
            <input v-model="teacherName" placeholder="Teacher Name" class="form-input" />
            <input v-model="teacherEmail" placeholder="Teacher Email" class="form-input" type="email"/>
            <input v-model="teacherClass" type="number" min="1" max="8" placeholder="Teacher Class" class="form-input" />
            <div class="form-actions">
              <button @click="addTeacher" class="btn btn-save">Save</button>
              <button @click="showAddTeacher = false" class="btn btn-cancel">Cancel</button>
            </div>
          </div>
        </div>

        <!-- Page-specific content -->
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from './Sidebar.vue'
import { useToast } from 'vue-toast-notification'
import { useRoute } from 'vue-router'
import Navbar from './Navbar.vue'

const toast = useToast();
const route = useRoute();

const showAddTeacher = ref(false)
const instituteId = route.params.institute_id;

const teacherName = ref('')
const teacherClass = ref(null)
const teacherEmail = ref('')

const backgroundRef = ref(null)
const ripples = ref([])
let rippleId = 0

const createRipple = (event) => {
  const rect = backgroundRef.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  const newRipple = { id: rippleId++, x, y, opacity: 1 }
  ripples.value.push(newRipple)

  setTimeout(() => {
    const index = ripples.value.findIndex((r) => r.id === newRipple.id)
    if (index > -1) ripples.value.splice(index, 1)
  }, 1000)
}

const updateBackgroundColor = (event) => {
  if (!backgroundRef.value) return
  const rect = backgroundRef.value.getBoundingClientRect()
  const x = ((event.clientX - rect.left) / rect.width) * 100
  const y = ((event.clientY - rect.top) / rect.height) * 100

  backgroundRef.value.style.background = `
    radial-gradient(circle at ${x}% ${y}%,
      rgba(255, 200, 0, 0.6) 0%,
      rgba(229, 76, 145, 0.5) 50%,
      rgba(128, 123, 123, 0.4) 100%
    )`
}

const handleMouseMove = (event) => updateBackgroundColor(event)
const handleClick = (event) => createRipple(event)

onMounted(() => {
  if (backgroundRef.value) {
    backgroundRef.value.addEventListener('mousemove', handleMouseMove)
    backgroundRef.value.addEventListener('click', handleClick)
  }
})
onUnmounted(() => {
  if (backgroundRef.value) {
    backgroundRef.value.removeEventListener('mousemove', handleMouseMove)
    backgroundRef.value.removeEventListener('click', handleClick)
  }
})

async function addTeacher() {
  try {
    const response = await fetch('http://127.0.0.1:5000/Finance_Tutor/teacher', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        institute_id: instituteId,
        name: teacherName.value,
        class_teacher: teacherClass.value,
        email: teacherEmail.value,
        password: "password"
      })
    });

    const data = await response.json();
    showAddTeacher.value = false

    if (!response.ok) {
      throw new Error(data.message || 'Teacher Add Failed');
    }

    toast.success(`Added Teacher: ${teacherName.value} (Class: ${teacherClass.value})`)
    window.location.reload()
  } catch (error) {
    console.log(error.message)
    toast.error(error.message);
  }
}
</script>

<style scoped>
.layout-page {
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  transition: background 0.3s ease;
  font-family: 'Poppins', sans-serif;
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

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #EBCCD3;
  z-index: 1000;
  display: flex;
  padding: 0 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.layout {
  display: flex;
  flex-direction: row;
  padding-top: 60px;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: 250px;
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.form-box {
  background: #ffddc8dd;
  backdrop-filter: blur(4px);
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 500px;
}

.form-title {
  margin-bottom: 25px;
  font-size: 18px;
  text-align: center;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-save {
  background-color: #4caf50;
  color: white;
}

.btn-save:hover {
  background-color: #43a047;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
}

.btn-cancel:hover {
  background-color: #d32f2f;
}
</style>