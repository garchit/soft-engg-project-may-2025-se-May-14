<template>
  <div class="learn-container">
    <div class="main-content">
      <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">Approve Students</div>
          <div class="page-caption">
            Manage student approvals efficiently.
          </div>
        </div>
      </header>
      </div>
      <div class="course-content">
        <input type="text" v-model="searchQuery" class="search-bar" placeholder="Search by name..." />
        <div class="table-container">
            <table>
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
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router';
import Sidebar from '../Institute/Sidebar.vue';
import { useToast } from 'vue-toast-notification';

const searchQuery = ref('');
const students = ref([]);
const toast = useToast();
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
    toast.error("Failed:", e.message);
  }
};

onMounted(fetchStudents);

const filteredStudents = computed(() => {
  return students.value
    .filter(student =>
      student.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
    .sort((a, b) => Number(a.class) - Number(b.class))
})

// --- THIS IS THE CORRECTED FUNCTION ---
async function approveOrReject(studentId, action) {
  try {
    const confirmMessage = action === 1 
      ? "Are you sure you want to approve this student?" 
      : "Are you sure you want to reject this student?";
      
    if (!confirm(confirmMessage)) {
      return; // User cancelled the action
    }

    const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/verify_student/${studentId}`, {
      method: "PUT",
      credentials: 'include',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ verified: action })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'An error occurred.');
    }

    toast.success(data.message);
    await fetchStudents(); // Refresh the list of students

  } catch (e) {
    toast.error(`Failed to process action: ${e.message}`);
  }
}
</script>


<style scoped>
.learn-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 100vh;
}

.main-content {
  display: flex;
  align-items: center;
  width: 100%;
}

h1{
  padding-top: 10px;
  text-align: center;
  font-size: 42px;
  color: white;
}

.course-content {
  background: #ffffff3d;
  height: calc(100vh - 280px);
  margin: 10px 32px 0 32px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 40px;
  overflow-y: auto;
}

.table-container {
  max-height: 450px;
  width: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: #ffffff2d;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  font-size: 20px;
  color: #000000a5;

}

thead {
  position: sticky;
  top: 0;
  background: #ffddc8;
}

th {
  padding: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.15);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

td {
  padding: 10px;
}

tr {
  font-size: 0.8rem;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

tr:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.01);
}

.search-bar {
  width: 35%; 
  margin: 2px 0 10px 10px; 
  display: block;    
  padding: 8px 10px;
  font-size: 12px;
  background: #ffffff67;
  border: 1px solid #ffffff2d;
  border-radius: 6px;
  box-sizing: border-box;
  align-self: flex-end;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
}

.student-table thead{
  position: sticky;
  top: 0;
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
  border-radius: 5px;
  width: 28px;
  height: 28px;
  font-size: 18px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, background-color 0.2s;
}

.tick {
  background-color: #10b981cc;
  color: white;
}
.tick:hover {
  background-color: #059669;
  transform: scale(1.05);
}

.cross {
  background-color: #ef4444cc;
  color: white;
  margin-left: 10px;
}
.cross:hover {
  background-color: #dc2626;
  transform: scale(1.05);
}

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 23px 0 18px;
}

.page-heading-box {
  width: 85%;
  padding: 1rem 0 2rem 0;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.page-heading {
  font-size: 3rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

.page-caption {
  font-size: 0.8rem;
  font-weight: 500;
  color: #ffffffcc;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  margin-top: -0.5rem;
}
</style>