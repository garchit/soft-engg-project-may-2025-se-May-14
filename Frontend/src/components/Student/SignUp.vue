<script setup lang="ts">
import { ref } from 'vue'

const formData = ref({
  parentEmail: '',
  password: '',
  confirmPassword: '',
  institute: '',
  className: '',
  dateOfBirth: '',
  username: ''
})

const institutes = [
  'Select Institute',
  'KV School',
  'HUS School',
  'ABC Academy',
]

const classes = [
  'Select Class',
  'Grade 1',
  'Grade 2',
  'Grade 3',
  'Grade 4',
  'Grade 5',
  'Grade 6',
  'Grade 7',
  'Grade 8',
  'Grade 9',
  'Grade 10',
  'Grade 11',
  'Grade 12'
]

const handleSubmit = () => {
  console.log('Form submitted:', formData.value)
  // Form submission logic will go here
}

const goToLogin = () => {
  console.log('Navigate to login')
  // Navigation logic will go here
}
</script>

<template>
    <div class="app-container">
  <div class="signup-container">
    <div class="signup-card">
      <div class="card-header">
        <h2 class="signup-title">Student Sign Up</h2>
        <p class="signup-subtitle">Create your account to get started with SAVVY</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="signup-form">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="parentEmail" class="form-label">Parent's Email</label>
            <input
              type="email"
              class="form-control custom-input"
              id="parentEmail"
              v-model="formData.parentEmail"
              required
              placeholder="Enter parent's email"
            />
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              class="form-control custom-input"
              id="username"
              v-model="formData.username"
              required
              placeholder="Enter username"
            />
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control custom-input"
              id="password"
              v-model="formData.password"
              required
              placeholder="Enter password"
            />
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input
              type="password"
              class="form-control custom-input"
              id="confirmPassword"
              v-model="formData.confirmPassword"
              required
              placeholder="Confirm password"
            />
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="institute" class="form-label">Institute Name</label>
            <select
              class="form-select custom-input"
              id="institute"
              v-model="formData.institute"
              required
            >
              <option v-for="institute in institutes" :key="institute" :value="institute === 'Select Institute' ? '' : institute">
                {{ institute }}
              </option>
            </select>
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="className" class="form-label">Class</label>
            <select
              class="form-select custom-input"
              id="className"
              v-model="formData.className"
              required
            >
              <option v-for="className in classes" :key="className" :value="className === 'Select Class' ? '' : className">
                {{ className }}
              </option>
            </select>
          </div>
        </div>

        <div class="mb-4">
          <label for="dateOfBirth" class="form-label">Date of Birth</label>
          <input
            type="date"
            class="form-control custom-input"
            id="dateOfBirth"
            v-model="formData.dateOfBirth"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary custom-btn mb-3">
          Sign Up
        </button>
        
        <div class="text-center">
          <a href="#" @click.prevent="goToLogin" class="login-link">
            ← Back to Login
          </a>
        </div>
      </form>
    </div>
  </div>
  </div>
</template>

<style scoped>
.row{
    display: flex;
    padding :20px;
    justify-content: space-between;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.signup-container {
  width: 100%;
  max-width: 600px;
}

.signup-card {
  background: white;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.card-header {
  text-align: center;
  margin-bottom: 30px;
}

.signup-title {
  color: #E54C91;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.signup-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 0;
}

.form-label {
  color: #333;
  font-weight: 600;
  margin-bottom: 8px;
}

.custom-input {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 12px 15px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.custom-input:focus {
  border-color: #1CB0F6;
  box-shadow: 0 0 0 0.2rem rgba(28, 176, 246, 0.25);
  outline: none;
}

.custom-btn {
  background: linear-gradient(45deg, #E54C91, #1CB0F6);
  border: none;
  border-radius: 10px;
  padding: 12px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
  color: white;
  margin-top: 20px;
  margin-bottom: 20px;
}

.custom-btn:hover {
  background: linear-gradient(45deg, #d63384, #0ea5e9);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(229, 76, 145, 0.4);
}

.login-link {
  color: #58CC02;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #46a302;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .signup-card {
    padding: 30px 20px;
  }
  
  .signup-title {
    font-size: 2rem;
  }
}
</style>