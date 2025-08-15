<script setup>
import { ref, computed, reactive, watch, nextTick } from 'vue'
import axios from 'axios' // Make sure to install axios: npm install axios
import Sidebar from './Sidebar.vue'
import {
  CTable,
  CTableHead,
  CTableBody,
  CTableHeaderCell,
  CTableRow,
  CTableDataCell,
  CButton,
  CBadge
} from '@coreui/vue'
import InteractiveLayout from './AdminLayout.vue'

// API Configuration
const API_BASE_URL = 'http://localhost:5000/Finance_Tutor' // Update with your API URL

// Store
const quiz = reactive({
  questions: [],
  units: [], // For storing units data
  filters: {
    search: '',
    unit: 'all'
  }
})

// Form states - Updated to match API structure
const forms = reactive({
  add: {
    unit_name: '',
    description: '',
    marks: 1,
    option_a: '',
    option_b: '',
    option_c: '',
    option_d: '',
    correct_option: ''
  },
  edit: {
    id: null,
    unit_name: '',
    description: '',
    marks: 1,
    option_a: '',
    option_b: '',
    option_c: '',
    option_d: '',
    correct_option: ''
  }
})

// Modal states
const modals = reactive({
  add: false,
  edit: false,
  delete: false,
  preview: false
})

// UI states
const ui = reactive({
  loading: false,
  notification: {
    show: false,
    message: '',
    type: 'success'
  },
  animation: {
    newQuestion: false
  }
})

// Computed properties
const filteredQuestions = computed(() => {
  return quiz.questions.filter(q => {
    const matchesSearch = q.description.toLowerCase().includes(quiz.filters.search.toLowerCase())
    const matchesUnit = quiz.filters.unit === 'all' || q.unit_name == quiz.filters.unit
    return matchesSearch && matchesUnit
  })
})

const totalQuestions = computed(() => quiz.questions.length)

const questionsStats = computed(() => {
  const stats = { easy: 0, medium: 0, hard: 0 }
  // Since your API doesn't have difficulty levels, we'll categorize by marks
  quiz.questions.forEach(q => {
    if (q.marks <= 1) stats.easy++
    else if (q.marks <= 3) stats.medium++
    else stats.hard++
  })
  return stats
})

// Validation
const isAddFormValid = computed(() => {
  return forms.add.unit_name &&
         forms.add.description.trim() &&
        //  forms.add.marks > 0 &&
         forms.add.option_a.trim() &&
         forms.add.option_b.trim() &&
         forms.add.option_c.trim() &&
         forms.add.option_d.trim() &&
         ['a', 'b', 'c', 'd'].includes(forms.add.correct_option)
})

const isEditFormValid = computed(() => {
  return forms.edit.unit_name &&
         forms.edit.description.trim() &&
         forms.edit.option_a.trim() &&
         forms.edit.option_b.trim() &&
         forms.edit.option_c.trim() &&
         forms.edit.option_d.trim() &&
         ['a', 'b', 'c', 'd'].includes(forms.edit.correct_option)
})

// API Methods
const fetchUnits = async () => {
  try {
    ui.loading = true
    const response = await axios.get(`${API_BASE_URL}/course`)
    console.log("res",response.data);
    if (response.data && response.data.course_detail) {
      // Map the course data to match the expected units structure
      quiz.units = response.data.course_detail.map(course => ({
        id: course.id,
        name: course.name || course.course_name || course.course_title // Adjust based on your course model
      }))
    }

  } catch (error) {
    console.error('Error fetching courses:', error)
    showNotification('Error fetching courses', 'error')
    
    // Fallback to hardcoded units
  
  } finally {
    ui.loading = false
  }
}



const fetchQuestions = async (unitId = null) => {
  try {
    ui.loading = true
    
    // Always use the single questionsall endpoint
    const response = await axios.get(`${API_BASE_URL}/questionsall`)
    console.log("response", response.data);
    
    if (response.data.questions) {
      // If unitId is provided, filter questions for that specific unit
      if (unitId) {
        console.log("Filtering questions for unit:", unitId)
        quiz.questions = response.data.questions.filter(q => q.unit_id == unitId)
      } else {
        // If no unitId provided, show all questions
        quiz.questions = response.data.questions
      }
    } else {
      quiz.questions = []
    }
    
  } catch (error) {
    console.error('Error fetching questions:', error)
    showNotification('Error fetching questions', 'error')
    quiz.questions = []
  } finally {
    ui.loading = false
  }
}




// Methods
const resetAddForm = () => {
  Object.assign(forms.add, {
    unit_name: '',
    description: '',
    marks: 1,
    option_a: '',
    option_b: '',
    option_c: '',
    option_d: '',
    correct_option: ''
  })
}

const showNotification = (message, type = 'success') => {
  ui.notification = { show: true, message, type }
  setTimeout(() => {
    ui.notification.show = false
  }, 3000)
}

const addQuestion = async () => {
  console.log("chl gya ki naa")
  if (!isAddFormValid.value) return
  
  ui.loading = true
  
  try {
    const response = await axios.post(`${API_BASE_URL}/question`, {
      unit_name: forms.add.unit_name,
      description: forms.add.description,
      marks: parseInt(forms.add.marks),
      option_a: forms.add.option_a,
      option_b: forms.add.option_b,
      option_c: forms.add.option_c,
      option_d: forms.add.option_d,
      correct_option: forms.add.correct_option
    })
    console.log("response", response.data);
    // Refresh questions list
    await fetchQuestions()
    
    // Trigger animation
    ui.animation.newQuestion = true
    await nextTick()
    
    setTimeout(() => {
      ui.animation.newQuestion = false
    }, 600)
    
    resetAddForm()
    modals.add = false
    showNotification('Question added successfully!', 'success')
    
  } catch (error) {
    console.error('Error adding question:', error)
    showNotification(error.response?.data?.error || 'Error adding question', 'error')
  } finally {
    ui.loading = false
  }
}

const deleteQuestion = async (questionId) => {
  ui.loading = true
  
  try {
    await axios.delete(`${API_BASE_URL}/question/${questionId}`)
    
    // Remove from local state
    const index = quiz.questions.findIndex(q => q.id === questionId)
    if (index !== -1) {
      quiz.questions.splice(index, 1)
    }
    
    modals.delete = false
    showNotification('Question deleted successfully!', 'info')
    
  } catch (error) {
    console.error('Error deleting question:', error)
    showNotification(error.response?.data?.error || 'Error deleting question', 'error')
  } finally {
    ui.loading = false
  }
}

const fetchName = async (id) =>{
  console.log("id", id)
    if (!id && id !== 0) return ''

  try {
    const { data } = await axios.get(`${API_BASE_URL}/course/${id}`)

    // backend returns { course_details: {...} }
    const details = data?.course_details ?? {}
    console.log("Course details fetched:", details)
    return (
           // if your model uses `name`
      details.course_title   // fallback field names
      
    )
  } catch (err) {
    console.error(`Failed to fetch course ${id}:`, err)
    return ''
  }
}

// const openEditModal = (question) => {
//   console.log("Editing question:", question)
//   forms.edit = {
//     id: question.id,
//     unit_name: fetchName(question.unit_id),
//     description: question.description,
//     marks: question.marks || 1,
//     option_a: question.option_a,
//     option_b: question.option_b,
//     option_c: question.option_c,
//     option_d: question.option_d,
//     correct_option: question.correct_option
//   }
//   modals.edit = true
//    console.log("Editing question  dd:", question)
// }

const openEditModal = async (question) => {
  console.log("Editing question:", question)

  const name = await fetchName(question.unit_id)   // ← await here

  forms.edit = {
    id:           question.id,
    unit_name:    name,                            // real string
    description:  question.description,
    marks:        question.marks || 1,
    option_a:     question.option_a,
    option_b:     question.option_b,
    option_c:     question.option_c,
    option_d:     question.option_d,
    correct_option: question.correct_option
  }
  modals.edit = true
}


const updateQuestion = async () => {
  if (!isEditFormValid.value) return
  
  ui.loading = true
  
  try {
    await axios.put(`${API_BASE_URL}/question/${forms.edit.id}`, {
      unit_name: forms.edit.unit_name,
      description: forms.edit.description,
      marks: parseInt(forms.edit.marks),
      option_a: forms.edit.option_a,
      option_b: forms.edit.option_b,
      option_c: forms.edit.option_c,
      option_d: forms.edit.option_d,
      correct_option: forms.edit.correct_option
    })
    
    // Update local state
    const index = quiz.questions.findIndex(q => q.id === forms.edit.id)
    if (index !== -1) {
      quiz.questions[index] = {
        ...quiz.questions[index],
        unit_name: forms.edit.unit_name,
        description: forms.edit.description,
        marks: parseInt(forms.edit.marks),
        option_a: forms.edit.option_a,
        option_b: forms.edit.option_b,
        option_c: forms.edit.option_c,
        option_d: forms.edit.option_d,
        correct_option: forms.edit.correct_option
      }
    }
    
    modals.edit = false
    showNotification('Question updated successfully!', 'success')
    
  } catch (error) {
    console.error('Error updating question:', error)
    showNotification(error.response?.data?.error || 'Error updating question', 'error')
  } finally {
    ui.loading = false
  }
}

// Helper functions
const getUnitName = (unitId) => {
  const unit = quiz.units.find(u => u.id === unitId)
  return unit ? unit.name : 'Unknown Unit'
}

const getDifficultyByMarks = (marks) => {
  if (marks <= 1) return 'easy'
  if (marks <= 3) return 'medium'
  return 'hard'
}

const getDifficultyColor = (marks) => {
  const difficulty = getDifficultyByMarks(marks)
  return difficulty === 'easy' ? 'success' : 
         difficulty === 'medium' ? 'warning' : 'danger'
}

const getCorrectOptionText = (question) => {
  const optionMap = {
    'a': question.option_a,
    'b': question.option_b,
    'c': question.option_c,
    'd': question.option_d
  }
  return optionMap[question.correct_option] || ''
}

// Initialize data
const initializeData = async () => {
  await fetchUnits()
  await fetchQuestions()
}

// Call initialization
initializeData()

// Options for correct answer mapping
const correctOptions = [
  { value: 'a', label: 'A' },
  { value: 'b', label: 'B' },
  { value: 'c', label: 'C' },
  { value: 'd', label: 'D' }
]
</script>

<template>
  <InteractiveLayout>
    <div class="d-flex">
      
      <!-- Notification Toast -->
      <Transition name="notification">
        <div 
        v-if="ui.notification.show" 
        :class="`notification notification-${ui.notification.type}`"
        >
        <i :class="`fas ${ui.notification.type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}`"></i>
        {{ ui.notification.message }}
      </div>
    </Transition>
    
    <div class="main-content">
      <div class="container-fluid">
        <!-- Header Section -->
        <div>
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h2 class="page-title">
                <i class="fas fa-question-circle me-2"></i>
                Quiz Management
              </h2>
              <p class="text-muted">Manage your quiz questions and track performance</p>
            </div>
            <button 
            class="btn btn-primary btn-lg add-btn"
            @click="modals.add = true"
            :disabled="ui.loading"
            >
            <i class="fas fa-plus me-2"></i>
            Add Question
            </button>
          </div>
          
          <!-- Stats Cards -->
          <div class="row mb-4">
            <div class="col-md-3">
              <div class="stats-card">
                <div class="stats-icon bg-primary">
                  <i class="fas fa-list"></i>
                </div>
                <div class="stats-content">
                  <h3>{{ totalQuestions }}</h3>
                  <p>Total Questions</p>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stats-card">
                <div class="stats-icon bg-success">
                  <i class="fas fa-smile"></i>
                </div>
                <div class="stats-content">
                  <h3>{{ questionsStats.easy }}</h3>
                  <p>Easy Questions (1 mark)</p>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stats-card">
                <div class="stats-icon bg-warning">
                  <i class="fas fa-meh"></i>
                </div>
                <div class="stats-content">
                  <h3>{{ questionsStats.medium }}</h3>
                  <p>Medium Questions (2-3 marks)</p>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stats-card">
                <div class="stats-icon bg-danger">
                  <i class="fas fa-frown"></i>
                </div>
                <div class="stats-content">
                  <h3>{{ questionsStats.hard }}</h3>
                  <p>Hard Questions (4+ marks)</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Filters Section -->
        <div class="filters-section mb-4">
          <div class="row">
            <div class="col-md-6">
              <div class="search-wrapper">
                <i class="fas fa-search search-icon"></i>
                <input
                v-model="quiz.filters.search"
                type="text"
                class="form-control search-input"
                placeholder="Search questions..."
                />
              </div>
            </div>
            <div class="col-md-3">
              <select v-model="quiz.filters.unit" class="form-select">
                <option value="all">All Units</option>
                <option v-for="unit in quiz.units" :key="unit.id" :value="unit.name">
                  {{ unit.name }}
                </option>
              </select>
              
            </div>
            <!-- <div class="col-md-3">
              <div class="d-flex gap-2">
                <button class="btn btn-outline-secondary btn-sm" @click="fetchQuestions()">
                  <i class="fas fa-refresh me-1"></i>Refresh
                </button>
                <button class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-download me-1"></i>Export
                </button>
              </div>
            </div> -->
          </div>
        </div>
        
        <div class="table-section">
          <CTable hover responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell scope="col" style="width: 5%">#</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 30%">Question</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 25%">Options</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 10%">Marks</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 15%">Course</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 10%">Correct</CTableHeaderCell>
                <CTableHeaderCell scope="col" style="width: 5%">Actions</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow v-for="(question, index) in filteredQuestions" 
              :key="question.id"
              :class="{ 'new-question': ui.animation.newQuestion && index === quiz.questions.length - 1 }">
              <CTableDataCell class="text-center">{{ index + 1 }}</CTableDataCell>
              <CTableDataCell>
                <div class="question-content">
                  <p class="question-text mb-1">{{ question.description }}</p>
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <div class="options-list">
                  <div class="option-item">A. {{ question.option_a }}</div>
              <div class="option-item">B. {{ question.option_b }}</div>
              <div class="option-item">C. {{ question.option_c }}</div>
              <div class="option-item">D. {{ question.option_d }}</div>
            </div>
          </CTableDataCell>
          <CTableDataCell>
            <CBadge :color="getDifficultyColor(question.marks)">
              {{ question.marks }} {{ question.marks === 1 ? 'mark' : 'marks' }}
            </CBadge>
          </CTableDataCell>
          <CTableDataCell>
            <!-- Display the fetched course name -->
            <CBadge color="secondary" :title="`Course ID: ${question.unit_id}`">
              {{ question.unit_name || `Course ${question.unit_id}` }}
            </CBadge>
          </CTableDataCell>
          <CTableDataCell>
            <div class="correct-answer">
              <strong>{{ question.correct_option.toUpperCase() }}.</strong>
              <small class="text-success d-block">{{ getCorrectOptionText(question) }}</small>
            </div>
          </CTableDataCell>
          <CTableDataCell>
            <div class="d-flex gap-2">
              <CButton color="primary" 
              size="sm" 
              @click="openEditModal(question)"
              :disabled="ui.loading">
              <i class="fas fa-edit"></i>
            </CButton>
              <CButton color="danger" 
                      size="sm" 
                      @click="deleteQuestion(question.id)"
                      :disabled="ui.loading">
                      <i class="fas fa-trash"></i>
                    </CButton>
                  </div>
          </CTableDataCell>
        </CTableRow>

        <!-- Loading state with course name fetching -->
        <CTableRow v-if="ui.loading">
          <CTableDataCell colspan="7" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted mt-2">Loading questions and course details...</p>
          </CTableDataCell>
        </CTableRow>
        
        <!-- Empty state -->
        <CTableRow v-if="filteredQuestions.length === 0 && !ui.loading">
          <CTableDataCell colspan="7" class="text-center py-5">
            <i class="fas fa-question-circle fa-3x text-muted mb-3"></i>
            <h4 class="text-muted">No questions found</h4>
            <p class="text-muted mb-4">
              {{ quiz.filters.search ? 'Try adjusting your search criteria' : 'Start by adding your first question' }}
            </p>
            <CButton v-if="!quiz.filters.search" 
            color="primary"
            @click="modals.add = true">
            <i class="fas fa-plus me-2"></i>Add Your First Question
          </CButton>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</div>
</div>

      <!-- Add Question Modal -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="modals.add" class="modal-overlay" @click.self="modals.add = false">
            <div class="modern-modal">
              <div class="modal-header">
                <h5 class="modal-title">
                  <i class="fas fa-plus-circle me-2"></i>
                  Add New Question
                </h5>
                <button class="btn-close" @click="modals.add = false"></button>
              </div>
              
              <div class="modal-body">
                <form @submit.prevent="addQuestion">
                  <div class="row mb-3">
                    <div class="col-md-8">
                      <label class="form-label">Unit *</label>
                      <select v-model="forms.add.unit_name" class="form-select" required>
                        <option value="">Select Unit</option>
                        <option v-for="unit in quiz.units" :key="unit.id" :value="unit.name">
                          {{ unit.name }}
                        </option>
                      </select>
                    </div>
                    
                    <div class="col-md-4">
                      <label class="form-label">Marks</label>
                      <input
                      v-model.number="forms.add.marks"
                      type="number"
                      class="form-control"
                      min="1"
                      max="10"
                      />
                    </div>
                  </div>
                  
                  <div class="form-group mb-3">
                    <label class="form-label">Question *</label>
                    <textarea
                    v-model="forms.add.description"
                    class="form-control"
                    rows="3"
                      placeholder="Enter your question here..."
                      required
                    ></textarea>
                  </div>
                  
                  <div class="form-group mb-3">
                    <label class="form-label">Options *</label>
                    <div class="options-input">
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">A</span>
                          <input
                          v-model="forms.add.option_a"
                            type="text"
                            class="form-control"
                            placeholder="Option A"
                            required
                            />
                          <div class="input-group-text">
                            <input
                              v-model="forms.add.correct_option"
                              type="radio"
                              value="a"
                              name="correct"
                              class="form-check-input mt-0"
                              />
                            </div>
                          </div>
                        </div>
                        
                        <div class="option-input-group mb-2">
                          <div class="input-group">
                            <span class="input-group-text">B</span>
                            <input
                            v-model="forms.add.option_b"
                            type="text"
                            class="form-control"
                            placeholder="Option B"
                            required
                            />
                          <div class="input-group-text">
                            <input
                            v-model="forms.add.correct_option"
                            type="radio"
                            value="b"
                            name="correct"
                            class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">C</span>
                          <input
                          v-model="forms.add.option_c"
                          type="text"
                          class="form-control"
                          placeholder="Option C"
                          required
                          />
                          <div class="input-group-text">
                            <input
                            v-model="forms.add.correct_option"
                            type="radio"
                            value="c"
                            name="correct"
                            class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">D</span>
                          <input
                          v-model="forms.add.option_d"
                          type="text"
                          class="form-control"
                          placeholder="Option D"
                          required
                          />
                          <div class="input-group-text">
                            <input
                            v-model="forms.add.correct_option"
                            type="radio"
                              value="d"
                              name="correct"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <small class="text-muted">Select the radio button for the correct answer</small>
                  </div>
                </form>
              </div>
              
              <div class="modal-footer">
                <button 
                type="button" 
                class="btn btn-secondary me-2"
                @click="modals.add = false"
                :disabled="ui.loading"
                >
                Cancel
              </button>
                <button 
                  type="button"
                  class="btn btn-primary"
                  @click="addQuestion"
                  :disabled="!isAddFormValid || ui.loading"
                >
                <span v-if="ui.loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-plus me-2"></i>
                  {{ ui.loading ? 'Adding...' : 'Add Question' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Edit Question Modal -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="modals.edit" class="modal-overlay" @click.self="modals.edit = false">
            <div class="modern-modal">
              <div class="modal-header">
                <h5 class="modal-title">
                  <i class="fas fa-edit me-2"></i>
                  Edit Question
                </h5>
                <button class="btn-close" @click="modals.edit = false"></button>
              </div>
              
              <div class="modal-body">
                <form @submit.prevent="updateQuestion">
                  <div class="row mb-3">
                    <div class="col-md-8">
                      <label class="form-label">Unit *</label>
                      <select v-model="forms.edit.unit_name" class="form-select" required>
                        <option value="">Select Unit</option>
                        <option v-for="unit in quiz.units" :key="unit.id" :value="unit.name">
                          {{ unit.name }}
                        </option>
                      </select>
                    </div>
                    
                    <div class="col-md-4">
                      <label class="form-label">Marks</label>
                      <input
                        v-model.number="forms.edit.marks"
                        type="number"
                        class="form-control"
                        min="1"
                        max="10"
                      />
                    </div>
                  </div>

                  <div class="form-group mb-3">
                    <label class="form-label">Question *</label>
                    <textarea
                      v-model="forms.edit.description"
                      class="form-control"
                      rows="3"
                      placeholder="Enter your question here..."
                      required
                      ></textarea>
                    </div>

                    <div class="form-group mb-3">
                      <label class="form-label">Options *</label>
                    <div class="options-input">
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">A</span>
                          <input
                            v-model="forms.edit.option_a"
                            type="text"
                            class="form-control"
                            placeholder="Option A"
                            required
                          />
                          <div class="input-group-text">
                            <input
                              v-model="forms.edit.correct_option"
                              type="radio"
                              value="a"
                              name="editCorrect"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">B</span>
                          <input
                            v-model="forms.edit.option_b"
                            type="text"
                            class="form-control"
                            placeholder="Option B"
                            required
                            />
                          <div class="input-group-text">
                            <input
                              v-model="forms.edit.correct_option"
                              type="radio"
                              value="b"
                              name="editCorrect"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">C</span>
                          <input
                            v-model="forms.edit.option_c"
                            type="text"
                            class="form-control"
                            placeholder="Option C"
                            required
                            />
                          <div class="input-group-text">
                            <input
                            v-model="forms.edit.correct_option"
                            type="radio"
                              value="c"
                              name="editCorrect"
                              class="form-check-input mt-0"
                              />
                          </div>
                        </div>
                      </div>
                      
                      <div class="option-input-group mb-2">
                        <div class="input-group">
                          <span class="input-group-text">D</span>
                          <input
                            v-model="forms.edit.option_d"
                            type="text"
                            class="form-control"
                            placeholder="Option D"
                            required
                            />
                            <div class="input-group-text">
                              <input
                              v-model="forms.edit.correct_option"
                              type="radio"
                              value="d"
                              name="editCorrect"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </form>
              </div>

              <div class="modal-footer">
                <button 
                  type="button" 
                  class="btn btn-secondary me-2"
                  @click="modals.edit = false"
                  :disabled="ui.loading"
                  >
                  Cancel
                </button>
                <button 
                type="button"
                  class="btn btn-primary"
                  @click="updateQuestion"
                  :disabled="!isEditFormValid || ui.loading"
                  >
                  <span v-if="ui.loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-save me-2"></i>
                  {{ ui.loading ? 'Updating...' : 'Update Question' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
  </InteractiveLayout>
</template>

<style scoped>
/* Main Layout */
.main-content {
  margin: 20px;
  border-radius: 5px;
  background-color: #ffffff3d;  
  padding: 0;
  height: calc(100vh - 250px);
}

.container-fluid {
  padding: 2rem;
  overflow-y: auto;
}

/* Header Section */
.page-title {
  color: #2d3748;
  font-weight: 700;
  margin: 0;
}

.add-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6);
}

/* Stats Cards */
.stats-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: white;
  font-size: 1.5rem;
}

.stats-content h3 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
}

.stats-content p {
  margin: 0;
  color: #718096;
  font-size: 0.9rem;
}

/* Filters Section */
.filters-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
  z-index: 10;
}

.search-input {
  padding-left: 45px;
  border: 2px solid #e2e8f0;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #4facfe;
  box-shadow: 0 0 0 0.2rem rgba(79, 172, 254, 0.25);
}

/* Table Section */
.table-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.question-content {
  max-width: 300px;
}

.question-text {
  font-weight: 500;
  color: #2d3748;
  line-height: 1.4;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.9rem;
}

.option-item {
  padding: 0.125rem 0;
}

.correct-answer {
  text-align: center;
}

.correct-answer strong {
  color: #38a169;
  font-size: 1.1rem;
}

.correct-answer small {
  font-size: 0.75rem;
  max-width: 100px;
  word-wrap: break-word;
}

/* Modern Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modern-modal {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  font-weight: 600;
  flex: 1;
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-close::before {
  content: '×';
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  background: #f7fafc;
}

/* Form Styles */
.form-label {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #4facfe;
  box-shadow: 0 0 0 0.2rem rgba(79, 172, 254, 0.25);
}

.option-input-group .input-group-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 600;
}

/* Notifications */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1060;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.notification-success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
}

.notification-info {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
}

.notification-error {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
}

/* Animations */
.notification-enter-active, .notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modern-modal,
.modal-leave-to .modern-modal {
  transform: scale(0.8) translateY(-50px);
}

.new-question {
  animation: highlightNew 2s ease-in-out;
}

@keyframes highlightNew {
  0%, 100% { 
    background-color: transparent; 
  }
  50% { 
    background-color: rgba(72, 187, 120, 0.1);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .container-fluid {
    padding: 1rem;
  }
  
  .stats-card {
    margin-bottom: 1rem;
  }
  
  .modern-modal {
    margin: 1rem;
    max-width: calc(100vw - 2rem);
  }
  
  .modal-body {
    padding: 1rem;
  }
}
</style>
