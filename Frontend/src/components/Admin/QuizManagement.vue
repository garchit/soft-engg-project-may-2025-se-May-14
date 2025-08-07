<script setup>
import { ref, computed, reactive, watch, nextTick } from 'vue'
// import { useQuizStore } from './stores/quizStore' // We'll create this
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
// Store (you can implement Pinia later)
const quiz = reactive({
  questions: [],
  filters: {
    search: '',
    difficulty: 'all'
  }
})

// Form states
const forms = reactive({
  add: {
    question: '',
    options: ['', '', '', ''],
    correct: 0,
    difficulty: 'medium',
    category: 'general',
    explanation: ''
  },
  edit: {
    index: null,
    question: '',
    options: ['', '', '', ''],
    correct: 0,
    difficulty: 'medium',
    category: 'general',
    explanation: ''
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
    const matchesSearch = q.question.toLowerCase().includes(quiz.filters.search.toLowerCase())
    const matchesDifficulty = quiz.filters.difficulty === 'all' || q.difficulty === quiz.filters.difficulty
    return matchesSearch && matchesDifficulty
  })
})

const totalQuestions = computed(() => quiz.questions.length)

const questionsStats = computed(() => {
  const stats = { easy: 0, medium: 0, hard: 0 }
  quiz.questions.forEach(q => stats[q.difficulty]++)
  return stats
})

// Validation
const isAddFormValid = computed(() => {
  return forms.add.question.trim() &&
         forms.add.options.every(opt => opt.trim()) &&
         forms.add.correct >= 0 && forms.add.correct < 4
})

const isEditFormValid = computed(() => {
  return forms.edit.question.trim() &&
         forms.edit.options.every(opt => opt.trim()) &&
         forms.edit.correct >= 0 && forms.edit.correct < 4
})

// Methods
const resetAddForm = () => {
  Object.assign(forms.add, {
    question: '',
    options: ['', '', '', ''],
    correct: 0,
    difficulty: 'medium',
    category: 'general',
    explanation: ''
  })
}

const showNotification = (message, type = 'success') => {
  ui.notification = { show: true, message, type }
  setTimeout(() => {
    ui.notification.show = false
  }, 3000)
}

const addQuestion = async () => {
  if (!isAddFormValid.value) return
  
  ui.loading = true
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500))
  
  const newQuestion = {
    id: Date.now(),
    question: forms.add.question,
    options: [...forms.add.options],
    correct: forms.add.correct,
    difficulty: forms.add.difficulty,
    category: forms.add.category,
    explanation: forms.add.explanation,
    createdAt: new Date().toISOString()
  }
  
  quiz.questions.push(newQuestion)
  
  // Trigger animation
  ui.animation.newQuestion = true
  await nextTick()
  
  setTimeout(() => {
    ui.animation.newQuestion = false
  }, 600)
  
  resetAddForm()
  modals.add = false
  ui.loading = false
  
  showNotification('Question added successfully!', 'success')
}

const deleteQuestion = async (index) => {
  ui.loading = true
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 300))
  
  quiz.questions.splice(index, 1)
  modals.delete = false
  ui.loading = false
  
  showNotification('Question deleted successfully!', 'info')
}

const openEditModal = (index) => {
  const question = quiz.questions[index]
  forms.edit = {
    index,
    question: question.question,
    options: [...question.options],
    correct: question.correct,
    difficulty: question.difficulty,
    category: question.category,
    explanation: question.explanation || ''
  }
  modals.edit = true
}

const updateQuestion = async () => {
  if (!isEditFormValid.value) return
  
  ui.loading = true
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500))
  
  const updatedQuestion = {
    ...quiz.questions[forms.edit.index],
    question: forms.edit.question,
    options: [...forms.edit.options],
    correct: forms.edit.correct,
    difficulty: forms.edit.difficulty,
    category: forms.edit.category,
    explanation: forms.edit.explanation,
    updatedAt: new Date().toISOString()
  }
  
  quiz.questions[forms.edit.index] = updatedQuestion
  
  modals.edit = false
  ui.loading = false
  
  showNotification('Question updated successfully!', 'success')
}

// Watchers
// watch(() => quiz.filters.search, (newVal) => {
//   // Debounce search
//   clearTimeout(window.searchTimeout)
//   window.searchTimeout = setTimeout(() => {
//     console.log('Searching for:', newVal)
//   }, 300)
// })

// Categories and difficulties
const categories = ['general', 'science', 'history', 'sports', 'technology']
const difficulties = ['easy', 'medium', 'hard']
</script>

<template>
  <div class="d-flex">
    <Sidebar />
    
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
                  <p>Easy Questions</p>
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
                  <p>Medium Questions</p>
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
                  <p>Hard Questions</p>
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
              <select v-model="quiz.filters.difficulty" class="form-select">
                <option value="all">All Difficulties</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <div class="col-md-3">
              <div class="d-flex gap-2">
                <button class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-download me-1"></i>Export
                </button>
                <button class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-upload me-1"></i>Import
                </button>
              </div>
            </div>
          </div>
        </div>


<div class="table-section">
  <CTable hover responsive>
    <CTableHead>
      <CTableRow>
        <CTableHeaderCell scope="col" style="width: 5%">#</CTableHeaderCell>
        <CTableHeaderCell scope="col" style="width: 30%">Question</CTableHeaderCell>
        <CTableHeaderCell scope="col" style="width: 30%">Options</CTableHeaderCell>
        <CTableHeaderCell scope="col" style="width: 15%">Difficulty</CTableHeaderCell>
        <CTableHeaderCell scope="col" style="width: 10%">Category</CTableHeaderCell>
        <CTableHeaderCell scope="col" style="width: 10%">Actions</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody>
      <CTableRow v-for="(question, index) in filteredQuestions" 
                 :key="question.id"
                 :class="{ 'new-question': ui.animation.newQuestion && index === quiz.questions.length - 1 }">
        <CTableDataCell class="text-center">{{ index + 1 }}</CTableDataCell>
        <CTableDataCell>
          <div class="question-content">
            <p class="question-text mb-1">{{ question.question }}</p>
            <small class="text-muted">
              Created: {{ new Date(question.createdAt).toLocaleDateString() }}
            </small>
          </div>
        </CTableDataCell>
        <CTableDataCell>
          <div class="options-list">
            <div v-for="(option, optIndex) in question.options" 
                 :key="optIndex"
                 :class="{ 'correct-option': optIndex === question.correct }"
                 class="option-item">
              {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
              <i v-if="question.correct === optIndex" 
                 class="fas fa-check-circle text-success ms-1"></i>
            </div>
          </div>
        </CTableDataCell>
        <CTableDataCell>
          <CBadge :color="question.difficulty === 'easy' ? 'success' : 
                         question.difficulty === 'medium' ? 'warning' : 'danger'">
            {{ question.difficulty.toUpperCase() }}
          </CBadge>
        </CTableDataCell>
        <CTableDataCell>
          <CBadge color="secondary">{{ question.category }}</CBadge>
        </CTableDataCell>
        <CTableDataCell>
          <div class="d-flex gap-2">
            <CButton color="primary" 
                    size="sm" 
                    @click="openEditModal(index)"
                    :disabled="ui.loading">
                    Edit
              <i class="fas fa-edit"></i>
            </CButton>
            <CButton color="danger" 
                    size="sm" 
                    @click="deleteQuestion(index)"
                    :disabled="ui.loading">
                    Delete
              <i class="fas fa-trash"></i>
            </CButton>
          </div>
        </CTableDataCell>
      </CTableRow>

      <!-- Empty state row -->
      <CTableRow v-if="filteredQuestions.length === 0">
        <CTableDataCell colspan="6" class="text-center py-5">
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
                  <div class="form-group mb-3">
                    <label class="form-label">Question *</label>
                    <textarea
                      v-model="forms.add.question"
                      class="form-control"
                      rows="3"
                      placeholder="Enter your question here..."
                      required
                    ></textarea>
                  </div>

                  <div class="form-group mb-3">
                    <label class="form-label">Options *</label>
                    <div class="options-input">
                      <div 
                        v-for="(option, index) in forms.add.options" 
                        :key="index"
                        class="option-input-group mb-2"
                      >
                        <div class="input-group">
                          <span class="input-group-text">{{ String.fromCharCode(65 + index) }}</span>
                          <input
                            v-model="forms.add.options[index]"
                            type="text"
                            class="form-control"
                            :placeholder="`Option ${String.fromCharCode(65 + index)}`"
                            required
                          />
                          <div class="input-group-text">
                            <input
                              v-model="forms.add.correct"
                              type="radio"
                              :value="index"
                              name="correct"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <small class="text-muted">Select the radio button for the correct answer</small>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Difficulty</label>
                      <select v-model="forms.add.difficulty" class="form-select">
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Category</label>
                      <select v-model="forms.add.category" class="form-select">
                        <option v-for="cat in categories" :key="cat" :value="cat">
                          {{ cat.charAt(0).toUpperCase() + cat.slice(1) }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="form-group mb-3">
                    <label class="form-label">Explanation (Optional)</label>
                    <textarea
                      v-model="forms.add.explanation"
                      class="form-control"
                      rows="2"
                      placeholder="Provide an explanation for the correct answer..."
                    ></textarea>
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
                  <div class="form-group mb-3">
                    <label class="form-label">Question *</label>
                    <textarea
                      v-model="forms.edit.question"
                      class="form-control"
                      rows="3"
                      placeholder="Enter your question here..."
                      required
                    ></textarea>
                  </div>

                  <div class="form-group mb-3">
                    <label class="form-label">Options *</label>
                    <div class="options-input">
                      <div 
                        v-for="(option, index) in forms.edit.options" 
                        :key="index"
                        class="option-input-group mb-2"
                      >
                        <div class="input-group">
                          <span class="input-group-text">{{ String.fromCharCode(65 + index) }}</span>
                          <input
                            v-model="forms.edit.options[index]"
                            type="text"
                            class="form-control"
                            :placeholder="`Option ${String.fromCharCode(65 + index)}`"
                            required
                          />
                          <div class="input-group-text">
                            <input
                              v-model="forms.edit.correct"
                              type="radio"
                              :value="index"
                              name="editCorrect"
                              class="form-check-input mt-0"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Difficulty</label>
                      <select v-model="forms.edit.difficulty" class="form-select">
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Category</label>
                      <select v-model="forms.edit.category" class="form-select">
                        <option v-for="cat in categories" :key="cat" :value="cat">
                          {{ cat.charAt(0).toUpperCase() + cat.slice(1) }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="form-group mb-3">
                    <label class="form-label">Explanation (Optional)</label>
                    <textarea
                      v-model="forms.edit.explanation"
                      class="form-control"
                      rows="2"
                      placeholder="Provide an explanation for the correct answer..."
                    ></textarea>
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
</template>

<style scoped>
/* Main Layout */
.main-content {
  margin-left: 250px;
  width: calc(100% - 250px);
  min-height: 100vh;
  background: #FDF9E2 ;
  padding: 0;
}

.container-fluid {
  padding: 2rem;
}

/* Header Section */
.header-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

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

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-item {
  padding: 0.25rem;
  border-radius: 4px;
}

.option-item.correct-option {
  background-color: rgba(56, 161, 105, 0.1);
  color: #38a169;
  font-weight: 500;
}




.questions-table {
  margin: 0;
}

.questions-table thead th {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 600;
  padding: 1rem;
  text-align: center;
}

.question-row {
  transition: all 0.3s ease;
  border: none;
}

.question-row:hover {
  background-color: #f7fafc;
  transform: scale(1.01);
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
  font-size: 0.9rem;
}

.option-item {
  padding: 0.25rem 0;
  display: flex;
  align-items: center;
}

.option-letter {
  font-weight: 600;
  margin-right: 0.5rem;
  color: #4a5568;
}

.correct-option {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 5px;
  font-weight: 500;
}

/* Difficulty Badges */
.difficulty-easy {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
}

.difficulty-medium {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
  color: white;
}

.difficulty-hard {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
  color: white;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.action-buttons .btn {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.action-buttons .btn:hover {
  transform: translateY(-2px);
}

/* Empty State */
.empty-state {
  padding: 4rem 2rem;
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
  justify-content: between;
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

.question-list-enter-active {
  transition: all 0.6s ease;
}

.question-list-enter-from {
  opacity: 0;
  transform: translateY(20px);
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
  
  .header-section {
    padding: 1.5rem;
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
  
  .table-responsive {
    font-size: 0.9rem;
  }
  
  .question-content {
    max-width: 200px;
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .add-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
  
  .stats-icon {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
  
  .stats-content h3 {
    font-size: 1.5rem;
  }
}
</style>
