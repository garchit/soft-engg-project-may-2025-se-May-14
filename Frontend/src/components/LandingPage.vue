<template>
  <div id="app">
    <div class="navbar">
      <span class="brand-name">SAVVY</span>
      <div class="nav-links">
        <a href="#" class="nav-link" @click.prevent="handleNavClick('Home')">About Us</a>
      </div>
    </div>

    <div class="hero-section">
      <div class="hero-icon">
        <div class="icon-wrapper" :style="{ transform: `translateY(${floatingOffset}px)` }">🏦</div>
      </div>
      <h1>Welcome to SAVVY!</h1>
      <p>Join our fun financial literacy platform and start your money learning adventure today!</p>
      <button class="cta-button" @click="handleGetStarted" :style="{ transform: buttonTransform }">Get Started</button>
      <div class="sign-in-section">
        <span class="sign-in-text">Already have an account?</span>
        <a href="#" class="sign-in-link" @click.prevent="handleSignIn">Login</a>
      </div>
    </div>

    <div class="features-section">
      <div class="feature-card"
           v-for="feature in features"
           :key="feature.id"
           @mouseenter="handleFeatureHover(feature.id, true)"
           @mouseleave="handleFeatureHover(feature.id, false)"
           :style="getFeatureCardStyle(feature.id)">
        <div class="feature-icon" :style="getFeatureIconStyle(feature.id)">{{ feature.icon }}</div>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.description }}</p>
      </div>
    </div>

    <div class="popup-overlay" v-if="showPopup" @click="handleOverlayClick">
      <div class="popup-container">
        <div class="popup-header">
          <h2>Choose Your Account Type</h2>
          <button class="close-btn" @click="closeAccountTypePopup">&times;</button>
        </div>
        <div class="popup-content">
          <p>Select the type of account you'd like to create:</p>
          <div class="account-options">
            <div class="account-option"
                 @click="selectAccountType('student')"
                 @mouseenter="hoveredOption = 'student'"
                 @mouseleave="hoveredOption = null">
              <div class="option-icon">🎓</div>
              <h3>Student</h3>
              <p>Perfect for kids and teens learning about money</p>
            </div>
            <div class="account-option"
                 @click="selectAccountType('institute')"
                 @mouseenter="hoveredOption = 'institute'"
                 @mouseleave="hoveredOption = null">
              <div class="option-icon">🏫</div>
              <h3>Institute</h3>
              <p>For schools and educational organizations</p>
            </div>
          </div>
        </div>
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

    <footer class="footer">
      <div class="footer-content">
        <p>Made with ❤️ by Team Savvy</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const floatingOffset = ref(0);
const floatingDirection = ref(1);
const buttonTransform = ref('translateY(-3px)');
const showPopup = ref(false);
const hoveredOption = ref(null);
const hoveredFeatures = reactive({});
let floatingInterval;

const features = [
  { id: 1, icon: '🎮', title: 'Fun Games', description: 'Learn money skills through exciting games and challenges' },
  { id: 2, icon: '📚', title: 'Easy Lessons', description: 'Simple, colorful lessons that make learning about money fun' },
  { id: 3, icon: '🏆', title: 'Earn Rewards', description: 'Collect badges and rewards as you master financial concepts' }
];

const handleNavClick = (section) => {
  console.log('Navigating to:', section);
};

const startFloatingAnimation = () => {
  floatingInterval = setInterval(() => {
    floatingOffset.value += floatingDirection.value * 0.5;
    if (floatingOffset.value > 5 || floatingOffset.value < -5) {
      floatingDirection.value *= -1;
    }
  }, 100);
};

const handleGetStarted = () => {
  buttonTransform.value = 'scale(0.95)';
  setTimeout(() => {
    buttonTransform.value = 'translateY(-3px)';
    showPopup.value = true;
  }, 100);
};

const closeAccountTypePopup = () => {
  showPopup.value = false;
};

const handleOverlayClick = (event) => {
  if (event.target.classList.contains('popup-overlay')) {
    closeAccountTypePopup();
  }
};

const handleSignIn = () => {
  alert('👋 Sign in feature coming soon!');
};

const handleFeatureHover = (id, hover) => {
  hoveredFeatures[id] = hover;
};

const getFeatureCardStyle = (id) => {
  const isHovered = hoveredFeatures[id];
  return {
    background: isHovered ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    color: isHovered ? 'white' : '',
    transform: isHovered ? 'translateY(-5px)' : 'translateY(0)',
    boxShadow: isHovered ? '0 15px 40px rgba(0, 0, 0, 0.15)' : '0 10px 30px rgba(0, 0, 0, 0.1)'
  };
};

const getFeatureIconStyle = (id) => {
  const isHovered = hoveredFeatures[id];
  return {
    transform: isHovered ? 'scale(1.1) rotate(5deg)' : 'scale(1) rotate(0deg)'
  };
};

const selectAccountType = (type) => {
  closeAccountTypePopup();
 if (type === 'student') {
    router.push('/student');
    //   alert('🎉 Welcome student! Your financial adventure begins!');
      // You can add navigation for student here if needed
    } else {
      // Navigate to the institute signup page
      router.push('/institute');
    }
};


const handleKeydown = (e) => {
  if (e.key === 'Escape' && showPopup.value) {
    closeAccountTypePopup();
  }
};

onMounted(() => {
  startFloatingAnimation();
  document.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  clearInterval(floatingInterval);
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>

/* Paste all your CSS from styles.css here 
@import './styles.css';*/

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
    background: transparent;
    min-height: 100vh;
    overflow-x: hidden;
}

#app {
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);
    min-height: 100vh;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}


/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.logo-icon {
    font-size: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.brand-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.3);
    cursor: pointer;
}

.nav-link:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Main Content */
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    flex: 1;
}

/* Hero Section */
.hero-section {
    text-align: center;
    max-width: 600px;
    margin: 2rem auto;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    padding: 3rem 2rem; 
    border-radius: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 3px solid rgba(255, 255, 255, 0.3);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
}


.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.hero-icon {
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
}

.icon-wrapper {
    display: inline-block;
    font-size: 4rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    animation: bounce 2s infinite;
    transition: transform 0.1s ease;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

.hero-section h1 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    position: relative;
    z-index: 1;
}

.hero-section p {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 2rem;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    position: relative;
    z-index: 1;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

.cta-button:active {
    transform: translateY(-1px);
}

.sign-in-section {
    margin-top: 1.5rem;
    position: relative;
    z-index: 1;
}

.sign-in-text {
    color: #666;
    margin-right: 0.5rem;
}

.sign-in-link {
    color: #667eea;
    text-decoration: none;
    font-weight: bold;
    transition: all 0.3s ease;
    cursor: pointer;
}

.sign-in-link:hover {
    color: #5a67d8;
    text-decoration: underline;
}

/* Features Section */
.features-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 3rem auto;
    padding: 0 1rem;
    max-width: 900px;
    width: 100%;
}


.feature-card {
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.feature-card:hover::before {
    opacity: 1;
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 50%;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.feature-card h3 {
    font-size: 1.3rem;
    color: #333;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.feature-card p {
    color: #555;
    line-height: 1.5;
}

.feature-card:hover h3 {
    color: rgb(238, 237, 237);
}
.feature-card:hover p {
  color: rgb(213, 213, 213);
}

/* Popup Styles */
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    transition: opacity 0.3s ease;
}

.popup-container {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 25px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.3);
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    transform: scale(0.8);
    transition: transform 0.3s ease;
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.popup-header h2 {
    color: #333;
    font-size: 1.5rem;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
}

.close-btn {
    background: none;
    border: none;
    font-size: 2rem;
    color: #666;
    cursor: pointer;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    color: #333;
    transform: rotate(90deg);
}

.popup-content {
    padding: 2rem;
}

.popup-content p {
    color: #555;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    text-align: center;
}

.account-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.account-option {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 2rem 1.5rem;
    border-radius: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.account-option::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.2));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.account-option:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.account-option:hover::before {
    opacity: 1;
}

.option-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 50%;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.account-option:hover .option-icon {
    transform: scale(1.1) rotate(5deg);
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.account-option h3 {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.account-option p {
    font-size: 0.9rem;
    line-height: 1.4;
    margin: 0;
    position: relative;
    z-index: 1;
}

.account-option:hover h3 {
    color: rgb(238, 237, 237);
}
.account-option:hover p {
  color: rgb(213, 213, 213);
}

/* Footer */
.footer {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem 2rem;
  width: 100%;

}

.footer-content {
    text-align: center;
    color: #333;
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }

    .nav-links {
        gap: 1rem;
    }

    .hero-title {
        font-size: 2rem;
    }

    .hero-description {
        font-size: 1rem;
    }
    
    .features-section {
        grid-template-columns: 1fr;
        padding: 0 1rem;
    }

    .main-content {
        padding: 1rem;
    }

    .account-options {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .popup-container {
        width: 95%;
    }

    .popup-header {
        padding: 1rem 1.5rem;
    }

    .popup-content {
        padding: 1.5rem;
    }
}

@media (max-width: 480px) {
    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
    }

    .hero-section {
        padding: 2rem 1rem;
        margin: 1rem 0;
    }

    .hero-title {
        font-size: 1.8rem;
    }

    .icon-wrapper {
        width: 100px;
        height: 100px;
        font-size: 3rem;
    }

    .popup-header h2 {
        font-size: 1.3rem;
    }
    
    .account-options {
        grid-template-columns: 1fr; 
    }

    .account-option {
        padding: 1.5rem 1rem;
    }

    .option-icon {
        width: 60px;
        height: 60px;
        font-size: 2.5rem;
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
