<template>
    <nav class="navbar">
      <div class="navbar-content">
        <div class="logo-container">
          <h1 class="logo">💸</h1>
        </div>
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </nav>
  </template>
  
  <script setup>
  const logout = () => {
    alert('Logging out...');
    window.location.href = '/'; 
  };
  </script>
  
  <style scoped>
  .navbar {
    width: 100%;
    background-color: #ffffff;
    color: rgb(72, 162, 204);
    padding: 15px 30px;
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
  }
  
  .logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50px; 
    height: 50px; 
    background-color: #E54C91; 
    border-radius: 50%; 
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
  }
  
  .logo {
    margin: 0;
    font-size: 2.5em; 
    font-weight: 600;
    animation: fly 1.5s infinite ease-in-out;
  }
  
  @keyframes fly {
    0%, 100% {
      transform: translateY(0); 
    }
    50% {
      transform: translateY(-10px); 
    }
  }
  
  .logout-button {
    margin-left: auto;
    background-color: #e54c91;
    border: none;
    padding: 10px 20px;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  .logout-button:hover {
    background-color: #c13e79;
  }
  </style>