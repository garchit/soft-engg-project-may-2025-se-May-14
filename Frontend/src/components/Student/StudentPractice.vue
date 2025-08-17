<template>
  <InteractiveLayout>
    <div class="main-content">
      <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">{{ unitName || 'Loading...' }}</div>
          <div class="page-caption">
            Practice questions to enhance your skills and knowledge.
          </div>
        </div>
      </header>

        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">Loading questions...</p>
        </div>
        <div v-else-if="error" class="error-container">
          <p class="error-text">{{ error }}</p>
          <button class="retry-button" @click="loadQuestions">Retry</button>
        </div>

        <div v-else-if="isGameOver" class="completion-container">
          <div class="completion-card">
            <h2 class="completion-title">Game Over!</h2>
            <p class="game-over-text">You've lost all your lives!</p>
            <div class="score-display">
              <span class="score-text">Your Score:</span>
              <span class="score-value">{{ score }}/{{ currentQuestionIndex + 1 }}</span>
            </div>
            <div class="percentage-display">
              {{ Math.round((score / (currentQuestionIndex + 1)) * 100) }}%
            </div>
            <button class="restart-button" @click="resetQuiz">Try Again</button>
          </div>
        </div>

        <div v-else-if="isCompleted" class="completion-container">
          <div class="completion-card">
            <h2 class="completion-title">Quiz Complete!</h2>
            
            <div class="score-display">
              <span class="score-text">Your Score:</span>
              <span class="score-value">{{ score }}/{{ questions.length }}</span>
            </div>
            
            <div class="percentage-display">
              <span class="percentage-text"></span>
              <span class="percentage-value">{{ Math.round((score / questions.length) * 100) }}%</span>
            </div>
            
            <button class="restart-button" @click="resetQuiz">Try Again</button>
          </div>
        </div>

        <div v-else-if="currentQuestion" class="question-card">
          <div class="timer-hearts-container">
            <div class="timer-container">
              <div
                class="timer-progress"
                :style="{
                  width: `${progress}%`,
                  backgroundColor: progressColor,
                  transition: 'width 1s linear, background-color 0.3s ease'
                }"
              ></div>
              <div class="timer-text">{{ formatTime(timeRemaining) }}</div>
            </div>
            
            <div class="lives-container">
              <div class="hearts-wrapper">
                <svg
                  v-for="(life, index) in lives"
                  :key="index"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  :class="[
                    'heart-icon',
                    life ? 'heart-alive' : 'heart-broken'
                  ]"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12.001 4.529c2.349-2.532 6.148-2.532 8.497 0 2.191 2.364 2.191 6.187 0 8.551l-7.083 7.645a1 1 0 0 1-1.428 0L3.906 13.08c-2.191-2.364-2.191-6.187 0-8.551 2.349-2.532 6.148-2.532 8.497 0l.001.001.001-.001z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div class="question-content">
            <h3 class="question-text">
              <span style="display: inline-flex; align-items: center; gap: 8px;">
              {{ currentQuestion.text }}
              <button 
                @click="toggleSpeech" 
                class="speaker-btn"
                aria-label="Read question aloud"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  class="icon"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" 
                    d="M11 5L6 9H3v6h3l5 4V5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" 
                    d="M15.54 8.46a5 5 0 010 7.07m2.83-9.9a9 9 0 010 12.73" />
                </svg>
              </button>
              </span>
            </h3>
            <div class="options-grid">
              <div
                v-for="(option, index) in currentQuestion.options"
                :key="index"
                class="option-item"
                :class="{
                  selected: selectedOption === index,
                  correct: showResults && index === currentQuestion.correctAnswer,
                  incorrect: showResults && selectedOption === index && index !== currentQuestion.correctAnswer,
                  disabled: showResults || isProcessing
                }"
                @click="handleOptionSelect(index)"
              >
                <div class="option-number">{{ String.fromCharCode(65 + index) }}</div>
                <div class="option-text">{{ option }}</div>
              </div>
            </div>

            <button
              class="continue-button"
              :disabled="selectedOption === null || isProcessing"
              @click="handleContinue"
            >
              {{ isLastQuestion ? 'Finish Quiz' : 'Continue' }}
            </button>
          </div>
        </div>
        <audio ref="breakSoundRef" preload="auto">
          <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT" type="audio/wav">
        </audio>
      </div>
  
  </InteractiveLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import InteractiveLayout from '../InteractiveLayout.vue';
import axios from 'axios';

const route = useRoute();

const questions = ref([]);
const currentQuestionIndex = ref(0);
const selectedOption = ref(null);
const answers = ref([]);
const score = ref(0);
const timeRemaining = ref(60);
const isCompleted = ref(false);
const isLoading = ref(false);
const error = ref(null);
const showResults = ref(false);
const lives = ref([true, true, true]);
const isGameOver = ref(false);
const isProcessing = ref(false);
const breakSoundRef = ref(null);
const unitName = ref(null);
const userId = ref(localStorage.getItem('user_id') || ''); 

const totalTime = 60; 
let timerInterval = null;

const API_BASE = '/Finance_Tutor'; 

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value]);
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.value.length - 1);
const progress = computed(() => (timeRemaining.value / totalTime) * 100);
const progressColor = computed(() => {
  if (timeRemaining.value > totalTime * 0.5) return '#22c55e';
  if (timeRemaining.value > totalTime * 0.17) return '#eab308';
  return '#ef4444';
});

const letterToNumber = (letter) => {
  const letters = ['a', 'b', 'c', 'd'];
  return letters.indexOf(letter.toLowerCase());
};

const startTimer = () => {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value -= 1;
    } else {
      handleTimeUp();
    }
  }, 1000);
};

const resetTimer = () => {
  timeRemaining.value = totalTime;
  startTimer();
};

const handleTimeUp = () => {
  if (timerInterval) clearInterval(timerInterval);
  selectedOption.value = -1;
  handleContinue();
};

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

const loadQuestions = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const unitId = route.params.unitId;
    if (!unitId) {
        throw new Error("Unit ID not found in route parameters.");
    }

    const courseUrl = `${API_BASE}/course/${unitId}`;
    const courseResponse = await axios.get(courseUrl);
    
    if (courseResponse.status !== 200) {
      throw new Error(`Failed to fetch course details. Status: ${courseResponse.status}`);
    }

    unitName.value = courseResponse.data.course_details.course_title;

    const questionsUrl = `${API_BASE}/questions/unit/${unitId}`;
    const questionsResponse = await axios.get(questionsUrl);
    
    if (questionsResponse.status !== 200) {
      throw new Error(`Failed to fetch questions. Status: ${questionsResponse.status}`);
    }
    
    const data = questionsResponse.data;
    
    if (data.questions && data.questions.length > 0) {
      questions.value = data.questions.map(q => ({
        id: q.id,
        text: q.description,
        options: [q.option_a, q.option_b, q.option_c, q.option_d],
        correctAnswer: letterToNumber(q.correct_option),
        unit: q.unit_id
      }));
      resetTimer();
    } else {
      error.value = 'No questions found for this unit.';
      questions.value = [];
    }
  } catch (err) {
    console.error('Error loading questions:', err);
    error.value = `Failed to load questions: ${err.message}. Please try again.`;
  } finally {
    isLoading.value = false;
  }
};

let isSpeaking = false;
let utterance = null;

const toggleSpeech = () => {
  if (!window.speechSynthesis) {
    alert("Your browser does not support speech synthesis.");
    return;
  }

  if (isSpeaking) {
    window.speechSynthesis.cancel();
    isSpeaking = false;
    return;
  }

  const voices = window.speechSynthesis.getVoices();
  const preferredVoice =
    voices.find(v => v.name.includes("Google UK English Female")) ||
    voices.find(v => v.name.includes("Google US English")) ||
    voices.find(v => /female/i.test(v.name)) ||
    voices[0];

  const questionText = currentQuestion.value.text;
  const optionsText = currentQuestion.value.options
    .map((opt, idx) => `Option ${String.fromCharCode(65 + idx)}: ${opt}`)
    .join(". ");

  const fullText = `${questionText}. ${optionsText}`;

  utterance = new SpeechSynthesisUtterance(fullText);
  utterance.lang = "en-US";
  utterance.rate = 0.95;
  utterance.pitch = 1;
  if (preferredVoice) utterance.voice = preferredVoice;

  utterance.onend = () => {
    isSpeaking = false;
  };

  isSpeaking = true;
  window.speechSynthesis.speak(utterance);
};

if (typeof window !== "undefined") {
  window.speechSynthesis.onvoiceschanged = () => {
    console.log("Voices loaded:", window.speechSynthesis.getVoices());
  };
}

const breakHeart = () => {
  const index = lives.value.lastIndexOf(true);
  if (index !== -1) {
    lives.value[index] = false;
    playBreakSound();
  }
};

const playBreakSound = () => {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.5);
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  } catch (error) {
    console.log('Audio not supported');
  }
};

const handleGameOver = () => {
  isGameOver.value = true;
  if (timerInterval) clearInterval(timerInterval);
  
  const percentage = Math.round((score.value / (currentQuestionIndex.value + 1)) * 100);
  submitScore(percentage);
};


const checkGameOver = () => {
  if (lives.value.filter(Boolean).length === 0) {
    handleGameOver();
    return true;
  }
  return false;
};

const handleOptionSelect = (index) => {
  if (showResults.value || isGameOver.value || isProcessing.value) return;
  selectedOption.value = index;
};

const handleContinue = async () => {
  if (isGameOver.value || isProcessing.value) return;
  
  isProcessing.value = true;
  showResults.value = true;
  
  if (selectedOption.value !== null && selectedOption.value !== -1) {
    answers.value.push(selectedOption.value);
    if (selectedOption.value === currentQuestion.value.correctAnswer) {
      score.value += 1;
    } else {
      breakHeart();
      if (checkGameOver()) {
        isProcessing.value = false;
        return;
      }
    }
  } else {
    breakHeart();
    if (checkGameOver()) {
      isProcessing.value = false;
      return;
    }
  }

  setTimeout(async () => {
    if (isLastQuestion.value) {
      finishQuiz();
    } else {
      currentQuestionIndex.value += 1;
      selectedOption.value = null;
      showResults.value = false;
      resetTimer();
    }
    isProcessing.value = false;
  }, 2000);
};

// --- THIS IS THE CORRECTED FUNCTION ---
const submitScore = async (percentage) => {
  try {
    const unitId = route.params.unitId;
    const url = `${API_BASE}/user_course_completed/${userId.value}`;
    const payload = {
      course_id: unitId,
      marks_scored: percentage
    };
    
    const response = await axios.post(url, payload);
    console.log('Score submitted successfully:', response.data);
  } catch (err) {
    console.error('Error submitting quiz results:', err);
  }
};

const finishQuiz = () => {
  if (timerInterval) clearInterval(timerInterval);
  isCompleted.value = true;

  const percentage = Math.round((score.value / questions.value.length) * 100);
  submitScore(percentage);
};

const resetQuiz = () => {
  currentQuestionIndex.value = 0;
  selectedOption.value = null;
  answers.value = [];
  score.value = 0;
  isCompleted.value = false;
  showResults.value = false;
  lives.value = [true, true, true];
  isGameOver.value = false;
  isProcessing.value = false;
  error.value = null;
  resetTimer();
};

onMounted(() => {
  loadQuestions();
});

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.main-content {
  display: grid;
  grid-template-rows: auto 1fr;
  height: 100vh;
  width: 100%; 
  overflow: hidden;
  padding: 0 12px;
  box-sizing: border-box;
}

.profile-header {
  width: 87%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 22px auto 15px auto;
  flex-wrap: wrap;
}

.page-heading-box {
  flex: 4;
  width: 83%;
  padding: 1rem 0 2rem 0;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.page-heading {
  font-size: 3rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

.page-caption {
  font-size: 0.8rem;
  font-weight: 500;
  color: #ffffffcc;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  margin-top: -0.5rem;
}

.practice-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.practice-title {
  color: white;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  margin: 0;
  font-family: 'Poppins', sans-serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.unit-container {
  background: linear-gradient(135deg, #e91e63 0%, #e81258 100%);
  border: 3px solid #c2185b;
  border-radius: 15px;
  padding: 15px 25px;
  color: white;
  font-weight: bold;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  z-index: 2;
  position: relative;
}

.unit-text {
  margin: 0;
  font-size: 16px;
  text-align: center;
  font-family: 'Poppins', sans-serif;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  color: white;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
  font-family: 'Poppins', sans-serif;
}

.error-container {
  text-align: center;
  color: white;
}

.error-text {
  font-size: 18px;
  margin-bottom: 20px;
  color: #fca5a5;
  font-family: 'Poppins', sans-serif;
}

.retry-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #9f66ea 0%, #e2c93d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: #cccccde7;
  transform: translateY(-2px);
}

.completion-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  z-index: 2;
  position: relative;
}

.completion-card {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.completion-card:hover {
  transform: scale(1.05);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

.completion-title {
  color: #000000;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  font-family: 'Poppins', sans-serif;
}

.game-over-text {
  color: #ff6b6b;
  font-size: 16px;
  margin-bottom: 20px;
  font-family: 'Poppins', sans-serif;
}

.score-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.score-text {
  font-size: 18px;
  color: #000000;
  font-family: 'Poppins', sans-serif;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
  font-family: 'Poppins', sans-serif;
  color: #000000;
}

.percentage-display {
  font-size: 36px;
  font-weight: bold;
  color: #000000;
  margin-bottom: 30px;
  font-family: 'Poppins', sans-serif;
}

.restart-button {
  padding: 15px 30px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.restart-button:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

.question-card {
  flex: unset;
  overflow-y: auto;
  overflow-x: hidden;
  height: unset;
  border-radius: 25px;
  background: #ffffff5d;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  margin: 10px 50px 100px 50px;
  padding: 40px 50px 30px 50px;
  position: relative;
}

.timer-hearts-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.timer-container {
  position: relative;
  flex: 1;
  height: 25px;
  background-color: #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timer-progress {
  height: 100%;
  border-radius: 12px;
  position: relative;
}

.timer-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #374151;
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  font-size: 12px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.lives-container {
  display: flex;
  align-items: center;
}

.hearts-wrapper {
  display: flex;
  gap: 8px;
}

.heart-icon {
  width: 32px;
  height: 32px;
  transition: all 0.3s ease;
}

.heart-alive {
  color: #ef4444;
  fill: #ef4444;
  filter: drop-shadow(0 2px 4px rgba(239, 68, 68, 0.3));
}

.heart-broken {
  color: #6b7280;
  fill: #6b7280;
  opacity: 0.4;
  animation: heartBreak 0.6s ease-in-out;
}

@keyframes heartBreak {
  0% { transform: scale(1); opacity: 1; }
  25% { transform: scale(1.3) rotate(-10deg); opacity: 0.8; }
  50% { transform: scale(0.8) rotate(10deg); opacity: 0.6; }
  75% { transform: scale(1.1) rotate(-5deg); opacity: 0.5; }
  100% { transform: scale(1); opacity: 0.4; }
}

.question-content {
  color: #ffffff;
  text-shadow: #0000004e 0px 2px 4px;
}

.question-text {
  font-size: 25px;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: center;
  line-height: 1.4;
  font-family: 'Poppins', sans-serif;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

.option-item {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #ff9b44 0%, #fc6075 100%);
  border-radius: 12px;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
}

.option-item:hover:not(.disabled) {
  background: linear-gradient(135deg, #ff8419ab 0%, #f42d48ab 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.option-item.selected {
  background: linear-gradient(135deg, #ff8419 0%, #f42d48 100%);;
  border: 2px solid #ffffff;
}

.option-item.correct {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
}

.option-item.incorrect {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.option-item.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.option-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
}

.continue-button {
  display: block;
  margin: 0 auto;
  padding: 15px 30px;
  background: #20ba59;
  border: white;
  border-radius: 12px;
  color: white;
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.continue-button:hover:not(:disabled) {
  background: linear-gradient(135deg,rgb(254, 202, 156)4 0%, #e756e2 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.continue-button:disabled {
  background: #6b728092;
  cursor: not-allowed;
  transform: none;
}

.speaker-btn {
  background-color: #f5f5f5;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.speaker-btn:hover {
  background-color: #e0e0e0;
  transform: scale(1.05);
}

.speaker-btn:active {
  transform: scale(0.95);
}

.icon {
  width: 20px;
  height: 20px;
  color: #444;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 10px;
  }
  
  .practice-content {
    margin-top: 80px;
    padding: 10px;
  }
  
  .practice-title {
    font-size: 24px;
  }
  
  .question-card {
    padding: 20px;
  }
  
  .timer-hearts-container {
    flex-direction: column;
    gap: 15px;
  }
  
  .options-grid {
    gap: 10px;
  }
  
  .option-item {
    padding: 12px 15px;
  }
}
</style>