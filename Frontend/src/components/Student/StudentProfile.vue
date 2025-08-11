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
              <img class="profile-avatar" :src="user.avatar || defaultAvatar" alt="Profile Picture" />
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
                <div v-for="badge in displayedBadges" :key="badge.id || badge.name" class="badge-vertical">
                  <img 
                    :src="`https://api.iconify.design/${getIconName(badge.name)}.svg`" 
                    :alt="badge.name" 
                    class="badge-img"
                  />
                  <div class="badge-info">
                    <div class="badge-label">{{ badge.name }}</div>
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
import { ref, computed, onMounted } from 'vue'
import InteractiveLayout from '../InteractiveLayout.vue'
import axios from 'axios'

const API_BASE = '/Finance_Tutor'

const defaultAvatar = 'https://randomuser.me/api/portraits/lego/2.jpg'

const user = ref({
  avatar: defaultAvatar,
  username: '',
  password: '',
  parentEmail: ''
})

const allBadges = ref([])      // all badges from /badges
const userBadges = ref([])     // user earned badges from /user_badges/:id

// Map badge names to icon names for Iconify API
const getIconName = (badgeName) => {
  const iconMap = {
    'First Login': 'fluent-emoji:grinning-face', // A happy face for first login
    'Week Warrior': 'twemoji:fire', // A colorful fire emoji
    'Month Master': 'twemoji:calendar', // A calendar icon
    'Rising Star': 'twemoji:shooting-star', // A bright star
    'Pro Player': 'twemoji:trophy', // A shiny trophy
    'Bronze Champion': 'twemoji:sparkles', // A bronze medal
    'Silver Champion': 'twemoji:star', // A silver medal
    'Gold Champion': 'twemoji:trophy', // A gold medal
    'Centurion': 'twemoji:shield', // A colorful shield
    'Halfway Hero': 'fluent-emoji:party-popper', // A half moon for halfway
    'Reward Legend': 'twemoji:star-struck', // A star-struck emoji
    'Quick Learner': 'twemoji:light-bulb', // A colorful book
    'Consistent Learner': 'twemoji:open-book', // An open book
    'Knowledge Collector': 'twemoji:scroll', // A scroll icon
  }
  return iconMap[badgeName] || 'twemoji:question';  // Fallback to a question mark emoji
}

async function fetchUserProfile() {
  try {
    const currentUserid = localStorage.getItem('user_id') || '1'
    const res = await axios.get(`${API_BASE}/User/${currentUserid}`)
    user.value.username = res.data.username || ''
    user.value.avatar = res.data.avatar || defaultAvatar
    user.value.password = res.data.password || ''
    user.value.parentEmail = res.data.parents_email || ''
  } catch (err) {
    console.error('Failed to fetch user profile:', err)
  }
}

// Fetch all badges (definitions)
async function fetchAllBadges() {
  try {
    const res = await axios.get(`${API_BASE}/badge`)
    allBadges.value = res.data.list_badges || []
  } catch (err) {
    console.error('Failed to fetch all badges:', err)
    // Fallback to a minimal hardcoded list if API fails
    allBadges.value = [
      { id: 14, name: 'First Login', description: "Let's start!", points: 5 }
    ]
  }
}

// Fetch badges earned by user
async function fetchUserBadges() {
  try {
    const currentUserid = localStorage.getItem('user_id') || '1'
    const res = await axios.get(`${API_BASE}/user_badges/${currentUserid}`)
    userBadges.value = res.data.badges || []
  } catch (err) {
    console.error('Failed to fetch user badges:', err)
    userBadges.value = []
  }
}

// Combine user badges with all badge definitions
const displayedBadges = computed(() => {
  return userBadges.value.map(ub => {
    // Match badge by id or name to get full info (description, points)
    let badgeDef = allBadges.value.find(b => b.id === ub.id || b.name === ub.name)
    if (!badgeDef) {
      // fallback: use user badge data only
      badgeDef = ub
    }
    return badgeDef
  })
})

// Edit profile handler
async function editProfile() {
  try {
    const currentUserid = localStorage.getItem('user_id') || '1'
    const updatedUser = {
      username: user.value.username,
      parents_email: user.value.parentEmail,
      password: user.value.password
    }
    const res = await axios.put(`${API_BASE}/User/${currentUserid}`, updatedUser)
    alert('Profile updated!')
  } catch (err) {
    console.error('Failed to update user profile:', err)
    alert('Failed to update profile. Please try again.')
  }
}

onMounted(async () => {
  await fetchUserProfile()
  await fetchAllBadges()
  await fetchUserBadges()
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
