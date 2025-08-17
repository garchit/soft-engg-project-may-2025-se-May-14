<template>
  <div class="chatbot-container">
    <div class="chatbot-header">
      <h3>Savvy Bot <span class="sparkles">✨</span></h3>
      <button @click="$emit('close')" class="close-btn">&times;</button>
    </div>
    <div class="messages-window">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
        <p>{{ msg.text }}</p>
      </div>
      <div v-if="isLoading" class="message bot">
        <p><i>Typing...</i></p>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="message-form">
      <div class="input-wrapper">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Ask me anything..."
          :disabled="isLoading"
        />
      </div>
      <button type="submit" :disabled="isLoading">Send</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['close']);

const messages = ref([
  { sender: 'bot', text: 'Hello! How can I help you with your finance questions today?' }
]);
const newMessage = ref('');
const isLoading = ref(false);
const apiUrl = '/Finance_Tutor/chatbot';

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  messages.value.push({ sender: 'user', text: newMessage.value });
  const userMessage = newMessage.value;
  newMessage.value = '';
  isLoading.value = true;

  try {
    const response = await axios.post(apiUrl, { question: userMessage });
    messages.value.push({ sender: 'bot', text: response.data.answer });
  } catch (error) {
    console.error("Error sending message:", error);
    messages.value.push({ sender: 'bot', text: 'Sorry, I ran into an error. Please try again.' });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
@keyframes subtle-glow {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}

.chatbot-container {
  position: fixed;
  bottom: 20px;
  left: 270px;
  width: 350px;
  height: 480px;
  z-index: 1000;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  font-family: 'Poppins', sans-serif;
  overflow: hidden;
  background: rgba(252, 228, 236, 0.4);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(252, 228, 236, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: linear-gradient(90deg, #f7797d, #fbd786);
  color: #fff;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.chatbot-header h3 { margin: 0; font-weight: 600; }
.sparkles { position: relative; }
@keyframes sparkle-animation {
  0% { opacity: 0; transform: scale(0.5) translate(5px, -5px); }
  50% { opacity: 1; transform: scale(1.2) translate(0, 0); }
  100% { opacity: 0; transform: scale(0.5) translate(-5px, 5px); }
}
.sparkles::before, .sparkles::after {
  content: '✨'; position: absolute; top: -5px; left: 100%;
  font-size: 12px; opacity: 0; animation: sparkle-animation 1s infinite;
}
.sparkles::after { animation-delay: 0.5s; }
.close-btn {
  background: none; border: none; color: #fff; font-size: 1.5rem;
  font-weight: 300; cursor: pointer; transition: opacity 0.2s ease;
}
.close-btn:hover { opacity: 0.8; }
.messages-window {
  flex-grow: 1; padding: 20px; overflow-y: auto; background-color: rgba(255, 255, 255, 0.1);
}
.message { margin-bottom: 15px; display: flex; }
.message p {
  padding: 10px 15px; border-radius: 18px; max-width: 80%;
  margin: 0; word-wrap: break-word; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}
.message.user { justify-content: flex-end; }
.message.user p { background-color: #f7797d; color: white; border-bottom-right-radius: 4px; }
.message.bot p {
  background-color: rgba(255, 255, 255, 0.7); color: #333;
  border: 1px solid rgba(252, 228, 236, 0.4); border-bottom-left-radius: 4px;
}
.message.bot i { color: #777; }

.message-form {
  display: flex;
  padding: 10px;
  border-top: 1px solid rgba(252, 228, 236, 0.4);
  background-color: rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.input-wrapper {
  position: relative;
  flex-grow: 1;
  margin-right: 8px;
  border-radius: 25px;
}

.input-wrapper::before {
  content: '';
  position: absolute;
  z-index: 0;
  inset: -5px;
  border-radius: 30px;
  background: linear-gradient(120deg, #f7797d, #fbd786, #a27cf3);
  background-size: 200% 200%;
  filter: blur(8px);
  animation: subtle-glow 6s ease-in-out infinite alternate;

  transform: translateZ(0);
}

.input-wrapper input {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  border: none;
  padding: 10px 15px;
  border-radius: 25px;
  font-family: 'Poppins', sans-serif;
  background-color: rgba(255, 255, 255, 0.8);
  color: #333;
  outline: none;
  box-sizing: border-box;
}

.input-wrapper input::placeholder { color: #777; }

.message-form button {
  background: linear-gradient(90deg, #f7797d, #fbd786);
  color: white; border: none; padding: 10px 15px; border-radius: 25px;
  cursor: pointer; transition: background-color 0.2s;
}

.message-form button:hover { background: linear-gradient(90deg, #e46a6e, #e9c678); }
.message-form button:disabled { background: #ccc; cursor: not-allowed; }
</style>