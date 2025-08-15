<template>
    <div class="chatbot-container">
      <div class="chatbot-header">
        <h3>Savvy Bot</h3>
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
        <input
          v-model="newMessage"
          type="text"
          placeholder="Ask me anything..."
          :disabled="isLoading"
        />
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
  background: white;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  border: 1px solid #ddd;
}
  
    .chatbot-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 20px;
      background: linear-gradient(90deg, #E54C91, #f58a5d);
      color: white;
      flex-shrink: 0; 
    }
  
    .chatbot-header h3 { margin: 0; font-weight: 600; }
    .close-btn { background: none; border: none; color: white; font-size: 2rem; font-weight: 300; cursor: pointer; }
    .messages-window { flex-grow: 1; padding: 20px; overflow-y: auto; background-color: #f9f9f9; }
    .message { margin-bottom: 15px; display: flex; }
    .message p { padding: 10px 15px; border-radius: 18px; max-width: 80%; margin: 0; word-wrap: break-word; }
    .message.user { justify-content: flex-end; }
    .message.user p { background-color: #E54C91; color: white; border-bottom-right-radius: 4px; }
    .message.bot p { background-color: #e9e9eb; color: #333; border-bottom-left-radius: 4px; }
    

    .message-form {
      display: flex;
      padding: 10px;
      border-top: 1px solid #ccc;
      background-color: #fff;
      flex-shrink: 0; /* Prevents form from shrinking */
    }
    .message-form input {
      flex-grow: 1;
      border: 1px solid #ddd;
      padding: 8px 15px; 
      border-radius: 20px;
      margin-right: 8px; 
      font-family: 'Poppins', sans-serif;
      min-width: 0; /* Allows input to shrink properly in flex container */
    }
    .message-form button {
      background-color: #E54C91;
      color: white;
      border: none;
      padding: 8px 15px; 
      border-radius: 20px;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .message-form button:hover { background-color: #d13a7b; }
    .message-form button:disabled { background-color: #a0a0a0; }
  </style>