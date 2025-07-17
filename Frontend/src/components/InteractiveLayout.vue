<!-- InteractiveLayout.vue -->
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
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from './Student/Navbar.vue'
import StudentSidebar from './Student/StudentSidebar.vue'

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
</script>

<style scoped>
.interactive-background {
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

.student-page {
  display: flex;
  flex-direction: row;
  padding-top: 60px;
  height: 100vh;
  overflow: hidden;
}

.student-content {
  flex: 1;
  margin-left: 250px;
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
</style>
