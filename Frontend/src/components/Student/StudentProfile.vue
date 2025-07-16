<template>
  <InteractiveLayout>
  <div class="profile-layout">
    <!-- Main Content -->
    <div class="main-content">
      <header class="profile-header">
        <h1>PROFILE</h1>
      </header>

      <section class="profile-card-section">
        <div class="profile-card">
          <img class="profile-avatar" :src="user.avatar" alt="Profile Picture" />
          <div class="profile-fields">
            <label>USERNAME
              <input type="text" v-model="user.username" />
            </label>
            <label>PASSWORD
              <input type="password" v-model="user.password" />
            </label>
            <label>PARENT'S EMAIL
              <input type="email" v-model="user.parentEmail" />
            </label>
          </div>
          <button class="edit-btn" @click="editProfile">EDIT PROFILE</button>
        </div>
      </section>

      <section class="badges-section">
        <h2>BADGES EARNED</h2>
        <div class="badges-list">
          <div v-for="badge in badges" :key="badge.label" class="badge">
            <img :src="badge.icon" :alt="badge.label" />
          </div>
        </div>
      </section>
    </div>
  </div>
  </InteractiveLayout>
</template>

<script setup>
import { ref } from 'vue'
// import StudentSidebar_2 from './StudentSidebar_2.vue'
import StudentSidebar from './StudentSidebar.vue'
import Navbar from './Navbar.vue'
import InteractiveLayout from '../InteractiveLayout.vue'

// Sidebar navigation
const navItems = [
  { text: 'HOME', route: '/home' },
  { text: 'LEARN', route: '/learn' },
  { text: 'PRACTICE', route: '/practice' },
  { text: 'PROFILE', route: '/profile' },
  { text: 'LEADER BOARD', route: '/leaderboard' },
]

// User data (mock)
const user = ref({
  avatar: 'https://randomuser.me/api/portraits/lego/1.jpg',
  username: 'student123',
  password: 'password',
  parentEmail: 'parent@email.com'
})

// Badges (mock)
const badges = [
  { label: 'Wizard', icon: 'https://img.icons8.com/color/96/000000/wizard.png' },
  { label: 'Fire', icon: 'https://img.icons8.com/color/96/000000/fire-element.png' },
  { label: 'Scroll', icon: 'https://img.icons8.com/color/96/000000/scroll.png' }
]

function editProfile() {
  alert('Profile updated!')
}
</script>

<style scoped>
.profile-layout {
  display: flex;
  min-height: 100vh;
  font-family: 'Poppins', sans-serif;
}

  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: #ffffffac; /* Navbar background color */
    z-index: 1000;
    display: flex;
    padding: 0 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }

/*.sidebar {
  
  width: 230px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 18px;
  position: relative;
}*/

.sidebar-profile {
  margin-bottom: 20px;
}

.sidebar-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 3px solid #fff;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  margin-top: 30px;
}

.sidebar-link {
  color: #fff;
  font-weight: bold;
  text-decoration: none;
  padding: 8px 0 8px 32px;
  border-radius: 18px 0 0 18px;
  transition: background 0.2s;
  font-size: 1.1rem;
  letter-spacing: 1px;
}
.sidebar-link.active,
.sidebar-link.router-link-exact-active {
  background: #b8e0d2;
  color: #222;
}

.sidebar-footer {
  margin-top: auto;
  margin-bottom: 18px;
}
.sidebar-chat {
  width: 40px;
}

.main-content {
  flex: 1;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 22px;
  margin-bottom: 18px;
}
.profile-header h1 {
  color: #fff;
  font-size: 2.8rem;
  font-weight: bold;
  letter-spacing: 2px;
}
.logout-btn {
  background: #1cb1f6;
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 8px 22px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.logout-icon {
  margin-right: 6px;
}

.profile-card-section {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 32px;
}
.profile-card {
  background: #ffb800;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 340px;
  max-width: 420px;
}
.profile-avatar {
  width: 78px;
  height: 78px;
  border-radius: 50%;
  border: 3px solid #fff;
  margin-bottom: 12px;
}
.profile-fields {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
  margin-bottom: 18px;
}
.profile-fields label {
  color: #333;
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
  background: #fff;
  margin-top: 2px;
}
.edit-btn {
  background: #1cb1f6;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 10px 22px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s;
}
.edit-btn:hover {
  background: #e54c91;
}

.badges-section {
  width: 100%;
  text-align: center;
}
.badges-section h2 {
  color: #fff;
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 16px;
  letter-spacing: 1px;
}
.badges-list {
  display: flex;
  justify-content: center;
  gap: 32px;
}
.badge {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(79, 140, 255, 0.07);
  padding: 16px 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.badge img {
  width: 56px;
  height: 56px;
  object-fit: contain;
}
</style>
