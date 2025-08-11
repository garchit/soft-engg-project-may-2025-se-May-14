<template>
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
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import { useToast } from 'vue-toast-notification'
import { useRoute } from 'vue-router'

const toast = useToast();
const route = useRoute();

const showAddTeacher = ref(false)
const instituteId = route.params.institute_id;


const teacherName = ref('')
const teacherClass = ref(null)
const teacherEmail = ref('')


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
.layout {
  display: flex;
}
.main-content {
  flex: 1;
  position: relative;
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
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 320px;
}

.form-title {
  margin-bottom: 15px;
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
