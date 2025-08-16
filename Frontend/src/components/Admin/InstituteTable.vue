<template>
    <InteractiveLayout>
      <div class="main-container">
          <!-- <h1>INSTITUTES</h1><br><br> -->
          <div class="table-container">
            <table>
                <thead>
                  <tr>
                    <th style="width: 40%;">INSTITUTE NAME
                      <i
                        class="bi bi-search clickable-icon"
                        @click="showNameSearch = !showNameSearch"
                      ></i>
                      <div
                        v-if="showNameSearch"
                        class="search-container"
                      >
                        <input
                          type="text"
                          v-model="searchName"
                          placeholder="Search..."
                        />
                      </div>
                    </th>
                    <th style="width: 30%;">STUDENTS ENROLLED
                      <i
                        class="bi bi-funnel clickable-icon"
                        @click="showStudentFilter = !showStudentFilter"
                      ></i>
                      <div
                        v-if="showStudentFilter"
                        class="search-container"
                      >
                        <select v-model="studentFilterType">
                          <option value="">All</option>
                          <option value="less">Less than</option>
                          <option value="more">More than</option>
                        </select>
                        <input
                          type="number"
                          v-model.number="studentFilterValue"
                          placeholder="Number"
                        />
                      </div>
                    </th>
                    <th style="width: 30%;">ACTIONS</th>
                  </tr>
                </thead>
                <tbody>
                    <!-- Loading state -->
                    <tr v-if="loading">
                      <td colspan="3" style="text-align: center; padding: 20px;">
                        Loading institutes...
                      </td>
                    </tr>
                    
                    <!-- Error state -->
                    <tr v-else-if="error">
                      <td colspan="3" style="text-align: center; padding: 20px; color: red;">
                        {{ error }}
                      </td>
                    </tr>
                    
                    <!-- Data rows -->
                    <tr v-else v-for="inst in filteredInstitutes" :key="inst.id">
                        <td>{{ inst.name }}</td>
                        <td style="text-align: center;">{{ inst.total_students }}</td>
                        <td>
                          <!-- <a href="#" class="text-primary me-2" title="Edit" style="color: black;" @click.prevent="editInstitute(inst)">
                            <i class="bi bi-pencil-square"></i>
                          </a>
                          <a href="#" class="text-danger me-2" title="Delete" style="color: red;" @click.prevent="deleteInstitute(inst)">
                            <i class="bi bi-trash"></i>
                          </a> -->
                          <!-- <a href="#" class="text-warning" title="Block" style="color: black !important;" @click.prevent="blockInstitute(inst)">
                            <i class="bi bi-slash-circle"></i>
                          </a> -->
                          <a 
  href="#" 
  class="text-warning" 
  :title="inst.blocked ? 'Unblock' : 'Block'" 
  style="color: black !important;" 
  @click.prevent="blockInstitute(inst)"
>
  <i :class="inst.blocked ? 'bi bi-check-circle' : 'bi bi-slash-circle'"></i>
</a>

                        </td>
                    </tr>
                </tbody>
            </table>
          </div>
      </div>
    </InteractiveLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import InteractiveLayout from './AdminLayout.vue'

// Reactive data
let institutes = ref([])
const loading = ref(false)
const error = ref('')

// Toggle states
const showNameSearch = ref(false)
const showStudentFilter = ref(false)

// Search/filter states
const searchName = ref('')
const studentFilterType = ref('')
const studentFilterValue = ref(null)

// API function to fetch institutes
const fetchInstitutes = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://127.0.0.1:5000/Finance_Tutor/all_institute')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    institutes.value = data
  } catch (err) {
    error.value = `Failed to fetch institutes: ${err.message}`
    console.error('Error fetching institutes:', err)
  } finally {
    loading.value = false
  }
}

// Action handlers
const editInstitute = (institute) => {
  console.log('Edit institute:', institute)
  // Implement edit functionality
}

const deleteInstitute = (institute) => {
  if (institute.id === -1) {
    alert("You cannot delete Independent Students!")
    return
  }
  
  if (confirm(`Are you sure you want to delete ${institute.name}?`)) {
    console.log('Delete institute:', institute)
    // Implement delete functionality
  }
}

const blockInstitute = async (institute) => {
  console.log("ccc",institute);
  if (institute.id === -1) {
    alert("You cannot block me!!")
    return
  }
  
  const action = institute.blocked ? 'unblock' : 'block'
  
  if (confirm(`Are you sure you want to ${action} ${institute.name}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/Finance_Tutor/toggle_block_institute/${institute.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      console.log("Response:", response);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.message) {
        // Success - refresh the institutes list to get updated data
        await fetchInstitutes()
        alert(`Institute ${action}ed successfully!`)
      } else if (data.error) {
        alert(`Error: ${data.error}`)
      }
      
    } catch (error) {
      console.error('Error toggling block status:', error)
      alert(`Failed to ${action} institute: ${error.message}`)
    }
  }
}


// Computed property for filtered institutes
const filteredInstitutes = computed(() => {
  return institutes.value.filter(inst => {
    const matchesName = inst.name.toLowerCase().includes(searchName.value.toLowerCase())
    let matchesStudents = true

    if (studentFilterType.value && studentFilterValue.value !== null) {
      if (studentFilterType.value === 'less') {
        matchesStudents = inst.total_students < studentFilterValue.value
      } else if (studentFilterType.value === 'more') {
        matchesStudents = inst.total_students > studentFilterValue.value
      }
    }

    return matchesName && matchesStudents
  })
})

// Fetch data on component mount
onMounted(() => {
  fetchInstitutes()
})
</script>

<style scoped>
h1 {
  font-size: 42px;
  color: white;
}

.main-container {
  background: #ffffff3d;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  /* padding: 40px; */
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin: 20px;
  width: 97%;
  height: calc(100vh - 100px);
  overflow-y: auto;
}

.table-container {
  width: 100%;
  max-height: 100%;
  overflow-y: auto;
  border-radius: 15px;
  background: #ffffff3d;
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
  z-index: 2;
  background: #ffddc8;
}

th {
  padding: 12px;
  font-weight: 600;
  font-size: 1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.15);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

td {
  padding: 10px;
}

tr {
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

tr:hover {
  background:#ffffff4d;
  transform: scale(1.01);
}

i.bi {
  font-weight: bold;
  font-size: 1.1em;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
  vertical-align: middle;
}

.search-container {
  margin-top: 5px;
  display: flex;
  gap: 5px;
  justify-content: center;
}

.search-container input,
.search-container select {
  padding: 4px 6px;
  font-size: 0.85rem;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  outline: none;
  background: rgba(255, 255, 255, 0.7);
}

.search-container input:focus,
.search-container select:focus {
  border-color: #007bff;
}

.clickable-icon {
  margin-left: 8px;
  cursor: pointer;
  font-size: 1rem;
  color: rgba(0, 0, 0, 0.6);
}

.clickable-icon:hover {
  color: #007bff;
}
</style>
