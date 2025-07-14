<template>
  <div class="signup-wrapper">
    <div class="signup-card">
      <div class="signup-right">
        <h3 class="signup-title">Student Sign Up</h3>
        <form @submit.prevent="handleSubmit" class="signup-form">

          <!-- Row 1: Username -->
          <div class="form-row" style="justify-content: center; align-items: center;">
          <div class="form-group" style="width: 50%; max-width: 300px;">
            <label class="form-label" style="text-align: center;">Username</label>
            <input v-model="username" type="text" class="form-input" placeholder="Enter Username" required>
          </div>
        </div>

          <!-- Row 2: Parent's Email and Date of Birth -->
            <div class="form-row" style="align-items: center; justify-content: center;">
            <div class="form-group" style="flex: 1; text-align: center;">
              <label class="form-label" style="display: flex; justify-content: center; align-items: center; height: 100%;">Parent's Email</label>
              <input v-model="parentEmail" type="email" class="form-input" placeholder="Enter Parent's Email" required>
            </div>
            <div class="form-group" style="flex: 1; text-align: center;">
              <label class="form-label" style="display: flex; justify-content: center; align-items: center; height: 100%;">Date of Birth</label>
              <input v-model="dateOfBirth" type="date" class="form-input" required>
            </div>
            </div>


            <div class="form-row" style="justify-content: center; align-items: center;">
            <div class="form-group" style="text-align: center;">
              <label class="form-label form-label-thick" style="text-align: center;">Institute Name</label>
              <select v-model="institute" class="form-input" required>
              <option value="">Select Institute</option>
              <option v-for="inst in institutes" :key="inst" :value="inst">{{ inst }}</option>
              </select>
            </div>
            <div class="form-group" style="text-align: center;">
              <label class="form-label form-label-thick" style="text-align: center;">Class</label>
              <select v-model="className" class="form-input" required>
              <option value="">Select Class</option>
              <option v-for="cls in classes" :key="cls" :value="cls">{{ cls }}</option>
              </select>
            </div>
            </div>


            <div class="form-row" style="justify-content: center; align-items: center;">
            <div class="form-group" style="text-align: center;">
              <label class="form-label" style="text-align: center;">Password</label>
              <input v-model="password" type="password" class="form-input" placeholder="Enter Password" required minlength="6">
            </div>
            
            <div class="form-group" style="text-align: center;">
              <label class="form-label" style="text-align: center;">Confirm Password</label>
              <input v-model="confirmPassword" type="password" class="form-input" placeholder="Confirm Password" required minlength="6">
            </div>
            
            </div>

            <button type="submit" class="submit-btn" style="padding: 8px; font-size: 14px;">Sign Up</button>
        </form>
        <div class="login-link-wrap">
          <a href="#" @click.prevent="goToLogin" class="login-link">← Back to Login</a>
        </div>
      </div>
      <div class="floating-emojis">
        <span class="float-icon">💰</span>
        <span class="float-icon">💸</span>
        <span class="float-icon">⭐️</span>
        <span class="float-icon">💵</span>
        <span class="float-icon">💲</span>
        <span class="float-icon">₹</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { CFormSelect } from '@coreui/vue';

const router = useRouter();


let username = ref('');
let parentEmail = ref('');
let dateOfBirth = ref('');
let className = ref('');
let password = ref('');
let confirmPassword = ref('');
let institute = ref('');


let classes = ref(['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5',
  'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'Class 11', 'Class 12']);

let institutes = ref(['Institute A', 'Institute B', 'Institute C']);

// Handle form submission
const handleSubmit = () => {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match!');
    return;
  }

  console.log({
    username: username.value,
    parentEmail: parentEmail.value,
    dateOfBirth: dateOfBirth.value,
    className: className.value,
    password: password.value,
    institute: institute.value,
  });

  alert('Form submitted successfully!');
};


const goToLogin = () => {
  router.push('/'); 
};
</script>

<style scoped>
.signup-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
  font-family: 'Arial', sans-serif;
}

.signup-card {
  width: 700px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 15px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.2);
  display: flex;
  overflow: hidden;
}

.signup-right {
  width: 100%;
  padding: 40px 40px 20px 40px;
  box-sizing: border-box;
}

.signup-title {
  text-align: center;
  font-size: 26px;
  color: #333;
  margin-bottom: 20px;
}

.signup-form .form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.signup-form .form-group {
  flex: 1;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s;
  font-family: 'Arial', sans-serif;
  background: white;
}

.form-input:focus {
  border-color: #fc6076;
}

.submit-btn {
  width: 50%;
  padding: 12px;
  background: linear-gradient(135deg, #fc6076 0%, #ff9a44 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s ease;
  margin-top: 10px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%);
}

.login-link-wrap {
  text-align: center;
  margin-top: 18px;
}

.login-link {
  color: #fc6076;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #fc6076;
  text-decoration: underline;
}

@media (max-width: 500px) {
  .signup-card {
    width: 100%;
    min-width: 0;
    border-radius: 0;
    box-shadow: none;
  }
  .signup-right {
    padding: 24px 10px 10px 10px;
  }
  .signup-form .form-row {
    flex-direction: column;
  }
}

.floating-emojis {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0; 
  overflow: hidden;
}

.float-icon {
  position: absolute;
  font-size: 2.5rem;
  opacity: 0.8;
  animation: floatEmoji 10s infinite linear;
}

/* Random placements */
.float-icon:nth-child(1) { top: 20%; left: 20%; animation-delay: 0s; }
.float-icon:nth-child(2) { top: 20%; left: 80%; animation-delay: 0s; }
.float-icon:nth-child(3) { top: 55%; left: 10%; animation-delay: 0s; }
.float-icon:nth-child(4) { top: 90%; left: 80%; animation-delay: 0s; }
.float-icon:nth-child(5) { top: 50%; left: 90%; animation-delay: 0s; }
.float-icon:nth-child(6) { top: 88%; left: 15%; animation-delay: 0s; }

@keyframes floatEmoji {
  0% {transform: translate(0, 0) scale(1) rotate(0deg);}
  25% {transform: translate(-10px, -60px) scale(1.1) rotate(10deg);}
  50% {transform: translate(10px, -90px) scale(1.2) rotate(-10deg);}
  75% {transform: translate(-5px, -60px) scale(1.1) rotate(10deg);}
  100% {transform: translate(0, 0) scale(1) rotate(0deg);}
}
</style>