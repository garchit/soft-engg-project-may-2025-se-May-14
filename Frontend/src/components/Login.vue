<template>
    <div class="login-wrapper">
        <h1>SAVVY</h1>
        <br><br>
        <img src="../assets/credit-card.png" class="credit-image"/>
        <img src="../assets/hands.png" class="hands-image"/>
        <img src="../assets/bag.png" class="bag-image"/>
        <img src="../assets/piggy.png" class="piggy-image"/>
        <div class="login-card">
            <div class="login-left">
                <img src="../assets/char1.png" class="char1 char-image"/>
                <img src="../assets/char2.png" class="char2 char-image"/>
                <img src="../assets/char3.png" class="char3 char-image"/>
                <img src="../assets/char4.png" class="char4 char-image"/>
            </div>
            <div class="login-right">
                <h3>Welcome back to <span id="savvy">SAVVY</span></h3>
                <br><br>
                <form @submit.prevent="handleSubmit">
                    <input v-model="email" class="input-border" placeholder="Email" type="text"/>

                    <div class="password-wrapper">
                        <input v-model="password" :type="showPassword ? 'text' : 'password'" class="input-border" placeholder="Password" />
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'" class="toggle-password" @click="togglePassword"></i>
                    </div> 
                    <br>

                    <button type="submit" class="submit-btn input-border">Login</button>
                    <p>Don't have account sign up, <a href="#" @click.prevent="goToLandingPage">here</a></p>

                </form>
            </div>
        </div>
    </div>
</template>



<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();

let email = ref('');
let password = ref('');
const showPassword = ref(false);


const togglePassword = () => {
  showPassword.value = !showPassword.value;
}

//Go to landing page if no account
const goToLandingPage = () => {
    router.push('/');
}

//Handle form submission
const handleSubmit = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/Finance_Tutor/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }

    alert(data.message);
    console.log('User:', data.user);
    console.log('Role', data.user.role);

    // Store login info in localStorage
    localStorage.setItem('username', data.user.username || '');
    localStorage.setItem('email', data.user.email || '');
    localStorage.setItem('role', data.user.role || '');
    localStorage.setItem('user_id', data.user.id || '');

    if(data.user.role == "admin"){
        router.push('/admin-home')
    } else if(data.user.role == "institute"){
        router.push(`/${data.id}/institute-home`)
    } else{
        router.push(`/student-home`)
    }

  } catch (error) {
    alert(error.message);
  }
};

</script>



<style scoped>
body{
    font-family: 'Arial', sans-serif;
}

h1{
    font-weight: 800;
    font-size: 54px;
    line-height: 100%;
    letter-spacing: 3.5%;
    color: rgb(209, 70, 132);
}

.login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 100vh;
    background: linear-gradient(109.62deg, #EFBD7D -1.73%, rgba(244, 123, 123, 0.72) 49.09%, #D99239 91.15%);
    font-family: 'Arial', sans-serif; 

    position: relative; /*For absolute positioning of the image*/
    overflow: hidden;
}

.credit-image{
    position: absolute;
    z-index: 0;
    width: 35%;
    top: -130px;
    left: 90px;
    border-radius: 180px;
}

.hands-image{
    position: absolute;
    width: 22%;
    bottom: -10px;
    right: -60px;
    transform: rotate(-30deg);
    z-index: 3;
}

.piggy-image{
    position: absolute;
    width: 15%;
    right: 20px;
    bottom: 300px;
    transform: scaleX(-1) rotate(-20deg); 
}

.bag-image{
    position: absolute;
    width: 15%;
    left: 50px;
    transform: rotate(-30deg);
}
.login-card {
    width: 800px;
    height: 500px;
    border: 8px solid white;
    border-radius: 20px;
    box-shadow: 0px 4px 75px -20px black;
    display: flex;
    overflow: hidden;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);

    position: relative;
    z-index: 2;
}

.login-left{
    width: 40%;
    background: linear-gradient(180deg, rgba(229, 76, 145, 0.78) 0%, #E8AE32 49.6%, #F7AD50 100%);

    border-radius: 0px 20px 20px 0px;
    box-shadow: 4px 4px 20px -4px black;
    position: relative;
    overflow: hidden;
}

/*Charater images in the login card*/
.char-image{
    position: absolute;
    height: 210px;
}

.char1{
    transform: rotate(110deg);
    top: -20px;
    left: -15px;
}
.char2{
    transform: rotate(-90deg);
    top: 90px;
    right: -10px;
}
.char3{
    transform: rotate(70deg);
    bottom: 90px;
    left: -35px;
}
.char4{
    transform: rotate(-20deg);
    bottom: -25px;
    right: 0px;
}

.login-right{
    width: 60%;
    padding: 5px 10px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

#savvy{
    color: rgba(244, 80, 154, 1);
}

form{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.toggle-password {
  position: absolute;
  top: 30%;
  right: 0.75rem;
  transform: translateY(-50%);
  cursor: pointer;
  color: #6c757d;
  font-size: 1.2rem;
}

.input-border{
    width: 300px;
    height: 2.8rem;
    font-size: 16px;
    border: 2.5px solid black;
    border-radius: 5px;
    /*box-shadow: 2px 6px 1px 5px rgba(0, 0, 0, 1);*/
    color: black;
    margin-bottom: 30px;
    padding-left: 10px; 
    background-color: inherit;
    align-items: left;
}
input::placeholder{
    color: black;
    letter-spacing: 3.5px;
    font-weight: bold;
    font-size: 16px;
}

.password-wrapper {
  position: relative;
  width: 100%; /* or a specific width */
}

p{
    color: gray;
    font-weight: 300;
}

a{
    color: rgba(244, 80, 154, 1);
    text-decoration: none;
}

.submit-btn{
    width: 150px;
    letter-spacing: 3.5px;
    text-align: center;
    font-weight: bold;
}
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
}
.submit-btn:active {
    transform: translateY(2px);
    box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.2);
}
</style>