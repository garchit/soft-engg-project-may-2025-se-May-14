<template>
  <div class="signup-wrapper">
    <div class="signup-card">
      <div class="signup-right">
        <h3 class="signup-title">Student Sign Up</h3>
        <form @submit.prevent="handleSubmit" class="signup-form">

          <!-- Row 1: Username -->
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Username</label>
              <input v-model="username" type="text" class="form-input" placeholder="Enter Username" required>
            </div>
          </div>

          <!-- Row 2: Parent's Email and Date of Birth -->
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Parent's Email</label>
              <input v-model="parentEmail" type="email" class="form-input" placeholder="Enter Parent's Email" required>
            </div>
            <div class="form-group">
              <label class="form-label">Date of Birth</label>
              <input v-model="dateOfBirth" type="date" class="form-input" required>
            </div>
          </div>

          <!-- Row 3: Class and Password -->
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Class</label>
              <select v-model="className" class="form-input" required>
                <option value="">Select Class</option>
                <option v-for="cls in classes" :key="cls" :value="cls">{{ cls }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-input" placeholder="Enter Password" required minlength="6">
            </div>
          </div>

          <!-- Row 4: Confirm Password and Institute Name -->
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Confirm Password</label>
              <input v-model="confirmPassword" type="password" class="form-input" placeholder="Confirm Password" required minlength="6">
            </div>
            <div class="form-group">
              <label class="form-label">Institute Name</label>
              <select v-model="institute" class="form-input" required>
                <option value="">Select Institute</option>
                <option v-for="inst in institutes" :key="inst" :value="inst">{{ inst }}</option>
              </select>
            </div>
          </div>

          <button type="submit" class="submit-btn">Sign Up</button>
        </form>
        <div class="login-link-wrap">
          <a href="#" @click.prevent="goToLogin" class="login-link">← Back to Login</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

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
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #fc6076 0%, #ff9a44 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s ease;
  margin-top: 10px;
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
</style>