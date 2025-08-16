<template>
  <div class="learn-container">
    <!-- Profile Header -->
    <header class="profile-header">
      <div class="page-heading-box">
        <div class="page-heading">Profile</div>
        <div class="page-caption">Keep your profile updated for better communication.</div>
      </div>
    </header>

    <!-- Profile Card -->
    <div v-if="!isLoading" class="profile-card">
      <div class="profile-container-horizontal">
        <!-- Left Side: Profile Picture -->
        <div class="profile-left">
          <div class="profile-picture-container">
            <img
              class="profile-picture"
              :src="profileImageUrl"
              @error="onImageError"
              alt="Profile Picture"
            />
            <button v-if="isEditing" @click="triggerFileUpload" class="upload-btn">
              CHANGE PROFILE
            </button>
            <p v-if="!isEditing" class="profile-label">PROFILE PICTURE</p>
            <input
              type="file"
              ref="fileInput"
              @change="uploadProfilePicture"
              accept="image/*"
              style="display: none"
            >
          </div>
        </div>

        <!-- Right Side: Form Details -->
        <div class="profile-right">
          <div v-for="field in fields" :key="field.key" class="form-group">
            <label :for="field.key">{{ field.label }}</label>
            <input
              :type="field.type"
              :id="field.key"
              v-model="profileData[field.key]"
              :disabled="!isEditing"
              class="form-input"
              :class="{ 'error': errors[field.key] }"
              @blur="validateField(field.key)"
            >
            <span v-if="errors[field.key]" class="error-message">{{ errors[field.key] }}</span>
          </div>

          <!-- Edit / Save Button -->
          <div class="btn-group">
            <button @click="toggleEdit" class="edit-btn">
              {{ isEditing ? 'SAVE PROFILE' : 'EDIT PROFILE' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>

    <!-- Success -->
    <div v-if="showSuccessMessage" class="success-message">
      Profile updated successfully!
    </div>

    <!-- Error Message -->
    <div v-if="apiError" class="error-message-popup">
      {{ apiError }}
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'InstituteProfile',
  setup() {
    const defaultProfileSvg = `https://randomuser.me/api/portraits/lego/2.jpg`;
    const router = useRouter();
    const route = useRoute();

    const instituteId = computed(() => route.params.institute_id);

    const API_BASE_URL = 'http://localhost:5000/Finance_Tutor'; // Update if needed

    const isEditing = ref(false);
    const isLoading = ref(false);
    const showSuccessMessage = ref(false);
    const fileInput = ref(null);
    const apiError = ref(null);

    const profileData = reactive({
      username: '',
      password: '',
      email: '',
      address: '',
      picture: '/default-profile.png'
    });

    const errors = reactive({
      username: '',
      password: '',
      email: '',
      address: ''
    });

    const originalData = reactive({});

    const fields = [
      { key: 'username', label: 'INSTITUTE NAME', type: 'text' },
      { key: 'address', label: 'ADDRESS', type: 'text' },
      { key: 'email', label: 'INSTITUTE EMAIL', type: 'email' },
      { key: 'password', label: 'PASSWORD', type: 'password' }
    ];

    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const FILE_SIZE_LIMIT = 5 * 1024 * 1024;

    const profileImageUrl = computed(() => profileData.picture || defaultProfileSvg);

    const onImageError = () => {
      profileData.picture = defaultProfileSvg;
    };

    const validators = {
      username: val => !val.trim() ? 'Institute name is required'
        : val.length < 3 ? 'Institute name must be at least 3 characters' : '',
      password: val => !val ? 'Password is required'
        : val.length < 6 ? 'Password must be at least 6 characters' : '',
      email: val => !val ? 'Email is required'
        : !EMAIL_REGEX.test(val) ? 'Please enter a valid email address' : '',
      address: val => !val.trim() ? 'Address is required' : ''
    };

    const validateField = key => {
      errors[key] = validators[key](profileData[key]);
    };

    const validateForm = () => {
      Object.keys(validators).forEach(validateField);
      return Object.values(errors).every(e => !e) &&
             Object.values(profileData).every(v => v);
    };

    const fetchInstituteProfile = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/institute/${instituteId.value}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.error) {
          throw new Error(data.error);
        }
        return data;
      } catch (error) {
        apiError.value = error.message;
        throw error;
      }
    };

    const updateInstituteProfile = async (profileUpdateData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/institute/${instituteId.value}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: profileUpdateData.username,
            address: profileUpdateData.address,
            email: profileUpdateData.email,
            password: profileUpdateData.password
          })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.error) {
          throw new Error(data.error);
        }
        return data;
      } catch (error) {
        apiError.value = error.message;
        throw error;
      }
    };

    const loadProfile = async () => {
      isLoading.value = true;
      apiError.value = null;
      try {
        const data = await fetchInstituteProfile();
        Object.assign(profileData, {
          username: data.Name || '',
          password: 'password', // never show password
          email: data.email || '',
          address: data.Address || '',
          picture: '/default-profile.png'
        });
        Object.assign(originalData, {...profileData});
      } catch (error) {
        // error already handled
      } finally {
        isLoading.value = false;
      }
    };

    const saveProfile = async () => {
      if (!validateForm()) return false;

      isLoading.value = true;
      apiError.value = null;
      try {
        await updateInstituteProfile(profileData);
        Object.assign(originalData, {...profileData});
        showSuccessMessage.value = true;
        setTimeout(() => showSuccessMessage.value = false, 3000);
        return true;
      } catch (error) {
        return false;
      } finally {
        isLoading.value = false;
      }
    };

    const toggleEdit = async () => {
      if (isEditing.value) {
        const success = await saveProfile();
        if (success) isEditing.value = false;
      } else {
        isEditing.value = true;
        await nextTick();
        document.getElementById('username')?.focus();
      }
    };

    const cancelEdit = () => {
      Object.assign(profileData, originalData);
      Object.keys(errors).forEach(k => errors[k] = '');
      isEditing.value = false;
      apiError.value = null;
    };

    const uploadProfilePicture = e => {
      const file = e.target.files[0];
      if (!file) return;
      if (file.size > FILE_SIZE_LIMIT) return alert('File size must be less than 5MB');
      const reader = new FileReader();
      reader.onload = ev => { profileData.picture = ev.target.result };
      reader.readAsDataURL(file);
    };

    const triggerFileUpload = () => fileInput.value?.click();

    const handleLogout = () => router.push('/login');

    onMounted(() => {
      if (instituteId.value) {
        loadProfile();
      } else {
        apiError.value = 'Invalid institute ID';
      }
    });

    return {
      isEditing,
      isLoading,
      showSuccessMessage,
      profileData,
      errors,
      fileInput,
      fields,
      toggleEdit,
      cancelEdit,
      uploadProfilePicture,
      triggerFileUpload,
      handleLogout,
      validateField,
      defaultProfileSvg,
      instituteId,
      profileImageUrl,
      onImageError,
      apiError
    };
  }
}
</script>

<style scoped>
.learn-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 100vh;
  overflow-y: auto
}
.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 23px 0 18px;
}
.page-heading-box {
  width: 85%;
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
.profile-card {
  background: #ffffff3d;
  min-height: 400px;
  margin: 10px 32px 0 32px;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  padding: 15px 40px;
}
.profile-container-horizontal {
  display: grid;
  grid-template-columns: 1fr 2fr;
  height: calc(100vh - 310px);
  gap: 32px;
}
.profile-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}
.profile-picture-container {
  text-align: center;
}
.profile-picture {
  width: 200px;
  height: 200px;
  border-radius: 20px;
  border: 3px solid #ffddc8;
  margin: 75px 12px 10px 12px;
}
.profile-label {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #ffffffc8;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}
.upload-btn {
  background: #4caf50cc;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}
.edit-btn {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  width: 70%;
  background: #00bbd4ee;
  border: none;
  margin: 2rem -10rem;
  padding: 0.75rem 2rem;
  border-radius: 15px;
  cursor: pointer;
  transition: background 0.3s;
}
.edit-btn:hover {
  background: #0097a7;
}
.profile-right {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 50px 30px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  color: #ffffffe4;
  font-size: 0.95rem;
  font-weight: 600;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.form-input {
  border: none;
  border-radius: 8px;
  padding: 7px 12px;
  font-size: 1rem;
  background: #ffddc8;
  margin-top: 2px;
  color: #000000cc;
}
.form-input:disabled {
  border: none;
  border-radius: 8px;
  padding: 7px 12px;
  font-size: 1rem;
  background: #ffddc8;
  margin-top: 2px;
  cursor: not-allowed;
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
.error-message-popup {
  position: fixed;
  top: 70px;
  right: 20px;
  background: #f44336;
  color: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  animation: slideIn 0.3s ease-out;
  z-index: 1000;
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
