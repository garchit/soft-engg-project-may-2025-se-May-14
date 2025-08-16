<template>
    <nav class="navbar">
      <div class="navbar-content">
        <img src="@/assets/logo.png" alt="Savvy Logo" class="logo" />
        <button class="logout-button" @click="logout">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
            <path d="M6 2a.5.5 0 0 1 .5.5v1A.5.5 0 0 1 6 4H2v8h4a.5.5 0 0 1 0 1H1.5a.5.5 0 0 1-.5-.5v-9A.5.5 0 0 1 1.5 2H6zm5.354 1.646a.5.5 0 0 1 0 .708L10.207 6H14.5a.5.5 0 0 1 0 1H10.207l1.147 1.646a.5.5 0 1 1-.708.708l-2-2a.5.5 0 0 1 0-.708l2-2a.5.5 0 0 1 .708 0z"/>
          </svg>
        </button>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useToast } from 'vue-toast-notification';

  const toast = useToast();

  const logout = async() => {
    localStorage.clear();
    window.location.href = '/';
    toast.success('Logged out successfully!')
  };

  </script>
  
  <style scoped>
 @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
  .navbar {
    width: 100%;
    padding: 15px 0px 30px 100px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .navbar-content {
    display: flex;
    align-items: center;
    justify-content: space-between; 
    width: 100%; 
    padding: 0px 10px 0px 10px;
  }

  .logo {
    width: 150px;
    height: 40px;
    border-radius: 5px;
    transition: transform 0.3s ease;
  }

  .logout-button {
    width: 45px;
    height: 35px;
    margin-left: auto;
    background-color: #e54c91;
    border: none;
    padding: 0.5em 0.6em 0.2em 0.3em;
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  .logout-button:hover {
    background-color: #c13e79;
  }

  .logout-button svg {
  transform: scaleX(-1);
  width: 1.5rem;
  height: 1.3rem;
  fill: white;
}
  .logout-button:hover svg {
    fill: #f7ebee;
  }
  </style>