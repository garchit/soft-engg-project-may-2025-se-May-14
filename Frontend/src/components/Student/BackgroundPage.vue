<template>
    <div class="background-container">
      <!-- Floating Emojis -->
      <div class="floating-emojis">
        <span class="float-icon">💰</span>
        <span class="float-icon">💸</span>
        <span class="float-icon">⭐️</span>
        <span class="float-icon">💵</span>
        <span class="float-icon">💲</span>
        <span class="float-icon">₹</span>
        <span class="float-icon">💳</span>
        <span class="float-icon">📈</span>
        <span class="float-icon">📉</span>
        <span class="float-icon">💰</span>
      </div>
    </div>
  </template>
  
  <style scoped>
  .background-container {
    position: relative;
    width: 100%;
    height: 100vh;
    background-color: white;
    overflow: hidden;
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
  
  /* Random placements explicitly avoiding overlapping */
  .float-icon:nth-child(1) { top: 10%; left: 20%; animation-delay: 2s; }
  .float-icon:nth-child(2) { top: 20%; left: 80%; animation-delay: 2s; }
  .float-icon:nth-child(3) { top: 50%; left: 20%; animation-delay: 2s; }
  .float-icon:nth-child(4) { top: 85%; left: 75%; animation-delay: 2s; }
  .float-icon:nth-child(5) { top: 60%; left: 90%; animation-delay: 2s; }
  .float-icon:nth-child(6) { top: 90%; left: 5%; animation-delay: 2s; }
  .float-icon:nth-child(7) { top: 10%; left: 50%; animation-delay: 2s; }
  .float-icon:nth-child(8) { top: 40%; left: 30%; animation-delay: 2s; }
  .float-icon:nth-child(9) { top: 50%; left: 70%; animation-delay: 2s; }
  .float-icon:nth-child(10) { top: 80%; left: 40%; animation-delay: 2s; }
  .float-icon:nth-child(11) { top: 20%; left: 60%; animation-delay: 2s; }
  
  @keyframes floatEmoji {
    0% { transform: translate(0, 0) scale(1) rotate(0deg); }
    25% { transform: translate(-20px, -60px) scale(1.1) rotate(10deg); }
    50% { transform: translate(40px, -90px) scale(1.2) rotate(-10deg); }
    75% { transform: translate(-30px, -60px) scale(1.1) rotate(10deg); }
    100% { transform: translate(0, 0) scale(1) rotate(0deg); }
  }
  </style>