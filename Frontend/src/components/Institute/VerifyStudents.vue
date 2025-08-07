<template>
  <div class="verify-students-page">
    <Sidebar />
    <div class="verify-students-container">
      <h1>APPROVE STUDENTS</h1>
      <div class="table-container">
        <!-- Search Bar -->
        <input type="text" v-model="searchQuery" class="search-bar" placeholder="Search by name..." />

        <div class="table-scroll">
          <!-- Table -->
          <table class="student-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Class</th>
                <th>Date of Birth</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id">
                <td>{{ student.name }}</td>
                <td>{{ student.class }}</td>
                <td>{{ student.dob }}</td>
                <td>
                  <button class="action-btn tick" @click="approveOrReject(student.id, 1)"><i class="bi bi-check-lg"></i></button> 
                  <button class="action-btn cross" @click="approveOrReject(student.id, -1)"><i class="bi bi-x-lg"></i></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router';
import Sidebar from '../Institute/Sidebar.vue';

const searchQuery = ref('');
const students = ref([]);
const router = useRoute();
const instituteId = router.params.institute_id;

async function fetchStudents(){
  try {
    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/unverified_students/${instituteId}`, {
      method: "GET",
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Failed to fetch Students");
    }

    const data = await response.json();
    students.value = data.students;

  } catch (e) {
    alert("Failed:", e.message);
  }
};

onMounted(fetchStudents);

// Filtered List
const filteredStudents = computed(() => {
  return students.value
    .filter(student =>
      student.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
    .sort((a, b) => Number(a.class) - Number(b.class))
})

async function approveOrReject(studentId, action) {
  try {
    const confirmAction = confirm("Are you sure you want to verify the student?");
    
    if (confirmAction) {
      const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/verify_student/${studentId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ "verified": action })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error verifying student');
      }

      const data = await response.json();
      alert(data.message);

      await fetchStudents();
    }
  } catch (e) {
    alert("Failed to verify/unverify: " + e.error);
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.verify-students-page{
  height: 100vh;
  display: flex;
}

.verify-students-container{
  height: 100vh;
  width: 100vw;
}
h1{
  padding-top: 10px;
  text-align: center;
  font-size: 42px;
  color: white;
}

.table-container {
  max-width: 800px;
  height: 70vh;
  margin: 50px auto;
  padding: 20px;
  border-radius: 12px;

  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);

  border: 1px solid #cbd5e1;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-bar {
  width: 300px; 
  margin: 0 auto; 
  display: block;    
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #0ea5e9;
  border-radius: 6px;
  box-sizing: border-box;
}
.search-bar:focus {
  outline: none;
  border-color: #0369a1;
  box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3);
}

.table-scroll {
  overflow-y: auto;
  flex-grow: 1;
}

.table-scroll::-webkit-scrollbar {
  width: 6px;
}
.table-scroll::-webkit-scrollbar-track {
  background-color: transparent;
}
.table-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
}

.student-table thead{
  position: sticky;
  top: 0;
  /* background: linear-gradient(135deg, #4FC3F7 0%, #1976D2 100%); */
  background-color: rgba(255, 255, 255, 0.6);
  color: #334155;
  z-index: 1;
}

.student-table th,
.student-table td {
  font-size: 1.25rem;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.student-table th {
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.student-table tbody tr:hover {
  background-color: rgba(14, 165, 233, 0.15);
  backdrop-filter: blur(3px);
}

.action-btn {
  border: none;
  border-radius: 50%;
  width: 34px;
  height: 34px;
  font-size: 18px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, background-color 0.2s;
}

.tick {
  background-color: #10b981;
  color: white;
}
.tick:hover {
  background-color: #059669;
  transform: scale(1.05);
}

.cross {
  background-color: #ef4444;
  color: white;
  margin-left: 10px;
}
.cross:hover {
  background-color: #dc2626;
  transform: scale(1.05);
}


</style>
