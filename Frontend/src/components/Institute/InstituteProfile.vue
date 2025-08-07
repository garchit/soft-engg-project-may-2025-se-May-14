<template>
  <div class="profile-app">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <!-- <img src="/logo.png" alt="Logo" class="logo-img"> -->
      </div>
      <button class="logout-btn" @click="handleLogout">Logout</button>
    </header>

    <div class="main-container">
      <!-- Sidebar Navigation -->
      

      <!-- Main Content -->
      <main class="content">
        <h1 class="page-title">PROFILE</h1>
        
        <div class="profile-card" v-if="!isLoading">
          <div class="profile-left">
            <div class="profile-picture-container">
              <img :src="profileData.picture" alt="Profile Picture" class="profile-picture">
              <p class="profile-label">PROFILE PICTURE</p>
              <input 
                type="file" 
                ref="fileInput" 
                @change="uploadProfilePicture" 
                accept="image/*" 
                style="display: none"
              >
              <button 
                v-if="isEditing" 
                @click="triggerFileUpload" 
                class="upload-btn"
              >
                Change Picture
              </button>
            </div>
            <button @click="toggleEdit" class="edit-btn">
              {{ isEditing ? 'SAVE PROFILE' : 'EDIT PROFILE' }}
            </button>
          </div>
          
          <div class="profile-right">
            <div class="form-group">
              <label for="username">USERNAME</label>
              <input 
                type="text" 
                id="username" 
                v-model="profileData.username" 
                :disabled="!isEditing"
                class="form-input"
                :class="{ 'error': errors.username }"
              >
              <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
            </div>
            
            <div class="form-group">
              <label for="password">PASSWORD</label>
              <input 
                type="password" 
                id="password" 
                v-model="profileData.password" 
                :disabled="!isEditing"
                class="form-input"
                :class="{ 'error': errors.password }"
              >
              <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            </div>
            
            <div class="form-group">
              <label for="email">INSTITUTE EMAIL</label>
              <input 
                type="email" 
                id="email" 
                v-model="profileData.email" 
                :disabled="!isEditing"
                class="form-input"
                :class="{ 'error': errors.email }"
              >
              <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Loading profile...</p>
        </div>

        <!-- Success Message -->
        <div v-if="showSuccessMessage" class="success-message">
          Profile updated successfully!
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'InstituteProfile',
  setup() {
    const router = useRouter()
    
    // Reactive state
    const isEditing = ref(false)
    const isLoading = ref(false)
    const showSuccessMessage = ref(false)
    const fileInput = ref(null)
    
    // Reactive profile data
    const profileData = reactive({
      username: '',
      password: '',
      email: '',
      picture: '/default-profile.png'
    })
    
    // Form errors
    const errors = reactive({
      username: '',
      password: '',
      email: ''
    })
    
    // Original data for reset functionality
    const originalData = reactive({})
    
    // Computed properties
    const isFormValid = computed(() => {
      return !errors.username && !errors.password && !errors.email &&
             profileData.username && profileData.password && profileData.email
    })
    
    // Validation functions
    const validateUsername = () => {
      if (!profileData.username.trim()) {
        errors.username = 'Username is required'
      } else if (profileData.username.length < 3) {
        errors.username = 'Username must be at least 3 characters'
      } else {
        errors.username = ''
      }
    }
    
    const validatePassword = () => {
      if (!profileData.password) {
        errors.password = 'Password is required'
      } else if (profileData.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
      } else {
        errors.password = ''
      }
    }
    
    const validateEmail = () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!profileData.email) {
        errors.email = 'Email is required'
      } else if (!emailRegex.test(profileData.email)) {
        errors.email = 'Please enter a valid email address'
      } else {
        errors.email = ''
      }
    }
    
    const validateForm = () => {
      validateUsername()
      validatePassword()
      validateEmail()
      return isFormValid.value
    }
    
    // Methods
    const loadProfile = async () => {
      isLoading.value = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock data - replace with actual API call
        Object.assign(profileData, {
          username: 'institute_admin',
          password: '********',
          email: 'admin@institute.edu',
          picture: '/default-profile.png'
        })
        
        // Store original data for reset
        Object.assign(originalData, { ...profileData })
      } catch (error) {
        console.error('Error loading profile:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const saveProfile = async () => {
      if (!validateForm()) {
        return false
      }
      
      isLoading.value = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        console.log('Saving profile:', profileData)
        // Add actual API call here
        // await profileAPI.save(profileData)
        
        // Update original data
        Object.assign(originalData, { ...profileData })
        
        // Show success message
        showSuccessMessage.value = true
        setTimeout(() => {
          showSuccessMessage.value = false
        }, 3000)
        
        return true
      } catch (error) {
        console.error('Error saving profile:', error)
        return false
      } finally {
        isLoading.value = false
      }
    }
    
    const toggleEdit = async () => {
      if (isEditing.value) {
        // Save changes
        const success = await saveProfile()
        if (success) {
          isEditing.value = false
        }
      } else {
        // Enter edit mode
        isEditing.value = true
        // Focus on first input
        await nextTick()
        document.getElementById('username')?.focus()
      }
    }
    
    const cancelEdit = () => {
      // Reset to original data
      Object.assign(profileData, originalData)
      // Clear errors
      Object.keys(errors).forEach(key => errors[key] = '')
      isEditing.value = false
    }
    
    const uploadProfilePicture = (event) => {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) { // 5MB limit
          alert('File size must be less than 5MB')
          return
        }
        
        const reader = new FileReader()
        reader.onload = (e) => {
          profileData.picture = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const triggerFileUpload = () => {
      fileInput.value?.click()
    }
    
    const handleLogout = () => {
      // Add logout logic
      router.push('/login')
    }
    
    // Lifecycle
    onMounted(() => {
      loadProfile()
    })
    
    // Return reactive properties and methods
    return {
      // State
      isEditing,
      isLoading,
      showSuccessMessage,
      profileData,
      errors,
      fileInput,
      
      // Computed
      isFormValid,
      
      // Methods
      toggleEdit,
      cancelEdit,
      uploadProfilePicture,
      triggerFileUpload,
      handleLogout,
      validateUsername,
      validatePassword,
      validateEmail
    }
  }
}
</script>

<style scoped>
/* Same styles as before, plus additional styles for new features */

.profile-app {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a56, #ff6b9d);
  font-family: 'Arial', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
}

.logo-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  padding: 8px;
}

.logout-btn {
  background: #00bcd4;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #0097a7;
}

.main-container {
  display: flex;
  height: calc(100vh - 100px);
}

.sidebar {
  width: 250px;
  background: #ff9a56;
  padding: 2rem 0;
  position: relative;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-link {
  display: block;
  padding: 1rem 2rem;
  color: white;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1rem;
  transition: background 0.3s;
}

.nav-item.active .nav-link {
  background: #4caf50;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.chat-icon {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  width: 60px;
  height: 60px;
  background: #ff6b9d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.chat-bubble::before {
  content: '💬';
  font-size: 24px;
}

.content {
  flex: 1;
  padding: 2rem;
  position: relative;
}

.page-title {
  font-size: 3rem;
  color: white;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.profile-card {
  background: #ffa726;
  border-radius: 20px;
  padding: 2rem;
  display: flex;
  gap: 3rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid #ff8f00;
}

.profile-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-picture-container {
  text-align: center;
}

.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: white;
  padding: 10px;
  margin-bottom: 0.5rem;
  object-fit: cover;
}

.profile-label {
  font-size: 0.8rem;
  font-weight: bold;
  margin: 0 0 0.5rem 0;
}

.upload-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.edit-btn {
  background: #00bcd4;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.edit-btn:hover {
  background: #0097a7;
}

.profile-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #333;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid transparent;
  border-radius: 10px;
  background: white;
  font-size: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s;
}

.form-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.form-input:focus {
  outline: none;
  border-color: #00bcd4;
  box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.3);
}

.form-input.error {
  border-color: #f44336;
}

.error-message {
  color: #f44336;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: white;
  min-height: 200px;
}

.spinner {
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

.success-message {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #4caf50;
  color: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
  }
  
  .nav-menu {
    display: flex;
    justify-content: space-around;
  }
  
  .profile-card {
    flex-direction: column;
    align-items: center;
  }
}
</style>
