<template>
  <div class="signup-wrapper">
    <div class="signup-card">

      <!-- <div class="signup-left">  
        <p class="side-text">Welcome to<br><span>Institute Sign Up</span></p>
      </div> -->


      <div class="signup-right">
        <h3 class="signup-title">Register Your Institute</h3>
        <form @submit.prevent="handleSubmit" class="signup-form">
          
          <div class="form-group">
            <label class="form-label">Institute Name</label>
            <input v-model="instituteName" type="text" class="form-input" placeholder="Enter Institute Name" required>
          </div>

          <div class="form-group">
            <label class="form-label">Institute Email</label>
            <input v-model="instituteEmail" type="email" class="form-input" placeholder="Enter Institute Email" required>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-input" placeholder="Enter Password" required minlength="6">
          </div>

          <div class="form-group">
            <label class="form-label">Confirm Password</label>
            <input v-model="confirmPassword" type="password" class="form-input" placeholder="Confirm Password" required minlength="6">
          </div>

          <div class="form-group">
            <label class="form-label">Address</label>
            <textarea v-model="address" class="form-input" placeholder="Enter Address" required></textarea>
          </div>

          <button type="submit" class="submit-btn">Sign Up</button>
        </form>
        <div class="login-link-wrap">
          <a href="#" @click.prevent="goToLogin" class="login-link">← Back to Login</a>
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

let instituteName = ref('')
let instituteEmail = ref('')
let password = ref('')
let confirmPassword = ref('');
let address = ref('')


const handleSubmit = async () => {
  
  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match!");
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/Finance_Tutor/institute/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: instituteName.value,
        email: instituteEmail.value,
        password: password.value,
        address: address.value
      })
    });

    if (!response.ok) {
      throw new Error('Failed to sign up');
    }

    const data = await response.json();
    alert('Sign Up Successful!');
    goToLogin();
    // Clear the form fields after successful submission
    instituteName.value = ''
    instituteEmail.value = ''
    password.value = ''
    address.value = ''

    // Optionally handle success (e.g., redirect or clear form)
  } catch (error) {
    alert('Sign Up Failed: ' + error.message);
  }
};

const goToLogin = () => {
  console.log("Navigating to login page");
  router.push('/'); 
};

</script>

<style scoped>
body{
  font-family: 'Arial', sans-serif;
}

.signup-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.signup-card {
  width: 100%;
  max-width: 420px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 15px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  padding: 40px 30px;
}

.signup-title {
  text-align: center;
  font-size: 26px;
  color: #333;
  margin-bottom: 25px;
}

.signup-form .form-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s;
  font-family: 'Arial', sans-serif;
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
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s ease;
  margin-top: 15px;
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

@media (max-width: 480px) {
  .signup-card {
    padding: 30px 20px;
  }

  .signup-title {
    font-size: 22px;
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
/* 
body{
  font-family: 'Arial', sans-serif;
}
.signup-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
  background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
  font-family: 'Arial', sans-serif;
  
}

.signup-card {
  width: 400px;
  height: 500px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 15px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.2);
  display: flex;
  overflow: hidden;
  padding-left : 100px; 
  background-color: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.signup-left {
  width: 50%;
  background: linear-gradient(135deg, #fc6076 0%, #ff9a44 100%);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.side-text {
  font-size: 44px;
  text-align: center;
   font-family: 'Arial', sans-serif;
}

.side-text span {
  font-size: 30px;
  font-weight: bold;
   font-family: 'Arial', sans-serif;
}

.signup-right {
  width: 100%;
  padding-left: 10px;
  padding-right: 40px;
 
  margin-left: -58px;
}

.signup-title {
  text-align: center;
  font-size: 26px;
  color: #333;
  margin-bottom: 20px;
}

.signup-form .form-group {
  margin-bottom: 15px;
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
  transition:  0.3s ease;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%);
} */
</style>
