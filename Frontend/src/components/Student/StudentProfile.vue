<template>
  <InteractiveLayout>
  <div class="profile-layout">
    <div class="main-content">
      <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">All About You!</div>
          <div class="page-caption">
            This is your space to tweak your details and admire your achievements.
          </div>
        </div>
      </header>
      <div class="profile-grid">
        <section class="profile-card-section">
          <div class="profile-card">
            <img class="profile-avatar" :src="defaultAvatar" alt="Profile Picture" />
            <div class="profile-fields">
              <label>USERNAME
                <input type="text" v-model="user.username" />
              </label>
              <label>PARENT'S EMAIL
                <input type="email" v-model="user.parentEmail" />
              </label>
              <label>PASSWORD
                <input type="password" v-model="user.password" />
              </label>
            </div>
            <button class="edit-btn" @click="editProfile">EDIT PROFILE</button>
          </div>
        </section>

        <section class="badges-section">
          <div class="badges-card">
            <h2 style="margin-bottom:0;">Badge Collection</h2>
            <hr class="badge-divider" style="margin-top:0;" />
            <div class="badges-list-vertical">
              <div v-for="badge in badges" :key="badge.label" class="badge-vertical">
                <img :src="badge.icon" :alt="badge.label" class="badge-img" />
                <div class="badge-info">
                  <div class="badge-label">{{ badge.label }}</div>
                  <div class="badge-desc">{{ badge.description }}</div>
                  <div class="badge-points">Points: {{ badge.points }}</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
  </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import InteractiveLayout from '../InteractiveLayout.vue'
import axios from 'axios'

const API_BASE = '/Finance_Tutor'

// Default avatar if no user avatar is found
const defaultAvatar = 'https://randomuser.me/api/portraits/lego/2.jpg'

// Reactive user data
const user = ref({
  avatar: defaultAvatar,
  username: '',
  password: '',
  parentEmail: ''
})

// Reactive badges array
const badges = ref([])

async function fetchUserProfile() {
  try {
    const currentUserid = localStorage.getItem('user_id') || '1'
    const res = await axios.get(`${API_BASE}/User/${currentUserid}`)
    console.log("User profile API Response:", res.data)

    user.value.username = res.data.username || ''
    user.value.avatar = res.data.avatar || defaultAvatar
    user.value.password = res.data.password || ''
    user.value.parentEmail = res.data.parents_email || ''
  } catch (err) {
    console.error('Failed to fetch user profile:', err)
  }
}

// Fetch badges from API
async function fetchBadges() {
  try {
    const res = await axios.get(`${API_BASE}/badge`)
    badges.value = res.data.badges || []

    // Check if the badges array is empty. If so, add a default badge.
    if (badges.value.length === 0) {
      console.log('No badges found, adding a default "First Login" badge.')
      badges.value.push({
        label: 'First Login',
        description: 'You have logged in for the first time!',
        icon: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSIjRkZCNzAwIj4KICAgIDxwYXRoIGQ9Ik0xMiAyTDE1LjA5IDguMjZMMjIgOS4yN0wxNyAxNC4xNEwxOC4xOCAyMS4wMkwxMiAxNy43N0w1Ljg2IDIxLjAzTDcgMTQuMTRM MiA5LjI3TDguOTEgOC4yNkwxMiAyWiIvPgo8L3N2Zz4=', // Placeholder icon
        points: 5
      })
    }
  } catch (err) {
    console.error('Failed to fetch badges:', err)
    // Optional: Add the default badge even if the API call fails
    if (badges.value.length === 0) {
      console.log('API call failed, adding a default "First Login" badge.')
      badges.value.push({
        label: 'First Login',
        description: 'You have logged in for the first time!',
        icon: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI0ZGRDc0MjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHBhdGggZD0iTTEyIDJMMTUuMDkgOC4yNkwyMiA5LjI3TDE3IDE0LjE0TDE4LjE4IDIxLjAyTDEyIDE3Ljc3TDUuODIgMjEuMDJMNyAxNC4xNEwyIDkuMjdMOC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjRkZENzAwIiBzdHJva2U9IiNGRkQ3MDAiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=',
        points: 5
      })
    }
  }
}

// Edit profile handler
async function editProfile() {
  try {
    const currentUserid = localStorage.getItem('user_id') || '1';
    
    // Construct the payload with the updated user data
    const updatedUser = {
      username: user.value.username,
      parents_email: user.value.parentEmail,
      password: user.value.password
    };
    
    // Send a PUT request to update the user profile
    const res = await axios.put(`${API_BASE}/User/${currentUserid}`, updatedUser);
    
    console.log("Profile updated successfully:", res.data);
    alert('Profile updated!');
  } catch (err) {
    console.error('Failed to update user profile:', err);
    alert('Failed to update profile. Please try again.');
  }
}

// Load data on mount
onMounted(() => {
  fetchUserProfile()
  fetchBadges()
})
</script>

<style scoped>
.profile-layout {
  display: flex;
  min-height: 100vh;
  height: 100vh;
  font-family: 'Poppins', sans-serif;
  padding-bottom: 100px;
}

.main-content {
  flex: 1;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.page-heading-box {
  width: 90%;
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

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 22px;
  margin-bottom: 18px;
  background: none;
  border: none;
  box-shadow: none;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  width: 100%;
  height: 100%;
  align-items: stretch;
}

.profile-card,
.badges-card {
  background: #ffffff4b;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
  min-width: 0;
  max-width: none;
}

.profile-card-section,
.badges-section {
  display: flex;
  justify-content: center;
  align-items: stretch;
  width: 100%;
  height: 100%;
  margin-bottom: 20px;
}

.profile-avatar {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 3px solid #ffddc8;
  margin-bottom: 12px;
  margin-top: 18px;
}

.profile-fields {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
  margin-bottom: 18px;
}
.profile-fields label {
  color: #ffffffe4;
  font-size: 0.95rem;
  font-weight: 600;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.profile-fields input {
  border: none;
  border-radius: 8px;
  padding: 7px 12px;
  font-size: 1rem;
  background: #ffddc8;
  margin-top: 2px;
}
.edit-btn {
  background: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 10px 22px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.5s;
}
.edit-btn:hover {
  background: #7fb069;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5)
}

.badges-card {
  background: #ffffff4b;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 32px 42px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}
.badges-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}
.badges-section h2 {
  color: #ffffffe4;
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 0px;
  letter-spacing: 1px;
}
.badge-divider {
  border: none;
  border-top: 2.5px solid #ffffffe4;
  margin: 0 0 18px 0;
  width: 75%;
  align-self: center;
  opacity: 0.8;
}
.badges-list-vertical {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-height: 390px;
  width: 100%;
  overflow-y: auto;
  padding-right: 8px;
}
.badge-vertical {
  display: flex;
  align-items: center;
  background: #ffddc8;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(79, 140, 255, 0.07);
  padding: 16px 18px;
  gap: 18px;
}
.badge-img {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 12px;
  background: #fbd8c2;
}
.badge-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}
.badge-label {
  font-size: 1.1rem;
  font-weight: bold;
  color: #e54c91;
}
.badge-desc {
  font-size: 0.95rem;
  color: #333;
}
.badge-points {
  font-size: 0.95rem;
  color: #00b3fa;
  font-weight: 600;
}
@media (max-width: 600px) {
  .profile-layout {
    padding-top: 24px;
    padding-bottom: 32px;
  }
}
</style>
