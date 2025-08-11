<template>
  <InteractiveLayout>
    <div class="unit-lectures">
      <!-- Main Header with Unit Title & Description -->
      <div class="main-content">
        <header class="profile-header">
          <div class="page-heading-box">
            <div class="page-heading">
              {{ loading ? 'Loading...' : error ? 'Error' : title }}
            </div>
            <div class="page-caption">
              {{ loading ? '' : error ? error : description }}
            </div>
          </div>
        </header>
      </div>

      <div class="learn-videos-container">
        <!-- Collapsible Sidebar -->
        <aside :class="['sidebar', { collapsed: isCollapsed }]">
          <button
            class="collapse-btn"
            :class="{ 'align-left': isCollapsed, 'align-right': !isCollapsed }"
            @click="toggleSidebar">
                {{ isCollapsed ? '▶' : '◀' }}
          </button>

          <h2 v-if="!isCollapsed" class="sidebar-heading">Lectures</h2>
          <div v-if="!isCollapsed" class="sidebar-divider"></div>
          <ul v-if="!loading && !error && !isCollapsed" class="lecture-list">
            <li
              v-for="lecture in lectures"
              :key="lecture.lecture_id"
              :class="['lecture-item', { active: lecture.lecture_id === activeLecture?.lecture_id }]"
              @click="selectLecture(lecture)"
            >
             {{ lecture.lecture_title }}
            </li>
          </ul>
          <div v-if="loading && !isCollapsed" class="loading">Loading lectures...</div>
          <div v-if="error && !isCollapsed" class="error">{{ error }}</div>
        </aside>

        <!-- Main Content Area -->
        <main class="content">
            <div v-if="activeLecture">
                <h1>{{ activeLecture.lecture_title }}</h1>
                <!-- <p>{{ activeLecture.lecture_description }}</p> -->
                <iframe
                v-if="activeLecture.lecture_link"
                :src="getEmbedUrl(activeLecture.lecture_link)"
                frameborder="0"
                allowfullscreen
                class="video-frame"
                ></iframe>

                <!-- Fallback Button -->
                <div class="youtube-fallback" v-if="!activeLecture.lecture_link">
                    <a v-if="activeLecture.lecture_link"
                       :href="activeLecture.lecture_link"
                       target="_blank"
                       rel="noopener noreferrer"
                       class="youtube-btn">
                         ▶ Watch on YouTube
                    </a>
                </div>

                <!-- Summary Section -->
                <div class="summary-section">
                    <div class="button-group">
                        <button @click="generateSummary" class="summary-btn">
                            Generate Summary
                        </button>

                        <button
                            @click="downloadSummary"
                            class="download-btn"
                            :disabled="loadingSummary">
                                Download Summary
                        </button>

                        <button
                            @click="handleNextOrFinish"
                            :class="['next-btn', !hasNextLecture ? 'finish' : '']"
                            :disabled="loading">
                                {{ hasNextLecture ? 'Next →' : 'Finish' }}
                        </button>
                    </div>
                <div v-if="loadingSummary" class="loading">Generating summary...</div>
                <textarea 
                    v-if="summary" 
                    class="summary-box" 
                    readonly
                    rows="8"
                >{{ summary }}</textarea>
                <div v-if="summaryError" class="error">{{ summaryError }}</div>
                </div>
            </div>

            <div v-else-if="!loading && !error" class="placeholder">
                <p>Select a lecture from the sidebar to begin</p>
            </div>
        </main>
      </div>
    </div>
  </InteractiveLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import InteractiveLayout from '../InteractiveLayout.vue';

const API_BASE = "/Finance_Tutor";
const route = useRoute();
const router = useRouter();
const unitId = route.params.unitId;

const title = ref('');
const description = ref('');
const lectures = ref([]);
const loading = ref(true);
const error = ref(null);
const activeLecture = ref(null);
const isCollapsed = ref(false);

const summary = ref('');
const loadingSummary = ref(false);
const summaryError = ref(null);

const generateSummary = async () => {
  if (!activeLecture.value) return;

  loadingSummary.value = true;
  summaryError.value = null;
  summary.value = '';

  try {
    // Call your Flask API for video summary
    const response = await axios.get(
      `${API_BASE}/video_summary/${activeLecture.value.lecture_id}`
    );

    // Backend sends { summary: "..." }
    if (response.data && response.data.summary) {
      summary.value = response.data.summary;
    } else {
      summaryError.value = 'No summary returned for this video.';
    }

  } catch (err) {
    console.error(err);
    summaryError.value = 'Failed to generate summary. Try again.';
  } finally {
    loadingSummary.value = false;
  }
};

const downloadSummary = async () => {
  if (!activeLecture.value) return;

  if (!summary.value) {
    // If no summary yet, generate first
    await generateSummary();
  }

  if (summary.value) {
    const timestamp = new Date().toLocaleString();
    const lectureTitle = activeLecture.value.lecture_title.replace(/[^a-z0-9]/gi, '_'); // Clean file name
    const fileName = `${lectureTitle}_Summary.txt`;
    const fileContent = `Lecture: ${activeLecture.value.lecture_title}\nGenerated At: ${timestamp}\n\nSummary:\n${summary.value}`;

    const blob = new Blob([fileContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
};

const hasNextLecture = computed(() => {
  if (!lectures.value.length || !activeLecture.value) return false;
  const currentIndex = lectures.value.findIndex(
    (lec) => lec.lecture_id === activeLecture.value.lecture_id
  );
  return currentIndex < lectures.value.length - 1;
});

const goToNextLecture = () => {
  const currentIndex = lectures.value.findIndex(
    (lec) => lec.lecture_id === activeLecture.value.lecture_id
  );
  const nextLecture = lectures.value[currentIndex + 1];
  selectLecture(nextLecture);
  summary.value = ''; // Clear summary
};

const handleNextOrFinish = () => {
  if (hasNextLecture.value) {
    goToNextLecture();
  } else {
    router.push('/student-learn'); // Redirect to learn page
  }
};

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

const selectLecture = (lecture) => {
  activeLecture.value = lecture;
  window.scrollTo({ top: 0, behavior: 'smooth' }); // optional scroll to top
};

const getEmbedUrl = (url) => {
  return url.replace("watch?v=", "embed/");
};

onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE}/course/${unitId}`);
    const data = response.data.course_details;
    title.value = data.course_title;
    description.value = data.course_description;
    lectures.value = data.lectures;
    activeLecture.value = data.lectures[0] || null;
  } catch (err) {
    console.error(err);
    error.value = 'Failed to load unit details.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>

.main-content {
  flex: 1;
  display: flex;
  padding: 0 32px;
  align-items: center;
  width: 100%;
}

.profile-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2px;
  margin-bottom: 18px;
  background: none;
  border: none;
  box-shadow: none;
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

.unit-lectures {
  padding: 20px;
  max-height: 100vh; /* Limit height to viewport */
  overflow-y: auto;  /* Enable vertical scroll */
}

.learn-videos-container {
  display: flex;
  max-height: 550px;
}

.sidebar {
  width: 300px;
  background: #ffffff4d;
  border-right: 5px solid #ffddc8;
  overflow-y: auto;
  transition: width 0.3s ease;
  position: relative;
  border-radius: 6px;
}

.sidebar.collapsed {
  width: 35px;
}

.collapse-btn {
  position: absolute;
  top: 10px;
  right: -10px;
  width: 35px;
  height: 50px;
  background: #ffddc8;
  border: 1px solid #ffddc8;
  border-radius: 5px;
  cursor: pointer;
  z-index: 10;
  font-family: Arial, sans-serif;
  font-size: 20px;
  line-height: 50px; /* Center vertically */
  display: flex;
  justify-content: center; /* Center by default */
  align-items: center;
  color: #fff;
  text-shadow: #999999a9 0px 2px 0px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, background 0.3s ease;
  padding: 0 5px;
}

.collapse-btn.align-left {
  justify-content: flex-start; /* Arrow sticks left */
}

.collapse-btn.align-right {
  justify-content: flex-end; /* Arrow sticks right */
}

.sidebar-heading {
  font-size: 1.4rem;
  font-weight: 700;
  margin: 0.5rem;
  text-align: center;
  color: #ffffff;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2); 
}
.sidebar-divider {
  height: 2px;
  width: 100%;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.1));
  margin: 2px 0 15px 0;
  border: none;
}

.lecture-list {
  list-style: none;
  padding: 0;
  margin-top: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #00000099;
  text-shadow: 1px 1px 4px rgba(255, 255, 255, 0.2);
  margin-bottom: 20px;
}

.lecture-item {
  padding: 0.8rem;
  cursor: pointer;
  transition: background 0.3s;
}

.lecture-item:hover {
  background: #ffddc87c;
}

.lecture-item.active {
  background: #ffddc8;
  font-weight: bold;
}

.content {
  flex: 1;
  padding: 1rem 2rem;
  overflow-y: auto;
  background-color: #ffffff4d;
  margin-left: 1%;
  border-radius: 10px;
}

.content h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  text-shadow: 1px 1px 4px rgba(255, 255, 255, 0.2);
  text-align: center;
}

.video-frame {
  width: 100%;
  height: 390px;
  border-radius: 10px;
  margin-top: 0.5rem;
  background: #ffddc8;
}

.placeholder {
  text-align: center;
  color: #999;
  font-size: 1.2rem;
  margin-top: 2rem;
}

.button-group button {
  color: #fff;
  padding: 5px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.3);
  margin: 0 5px 0 5px; /* Remove margin to avoid height differences */
  height: 40px; /* Fixed height for both */
  font-size: 16px; /* Same font size */
  line-height: 1.2;
}

.summary-btn {
  background-color: #e54c91;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
  margin-bottom: 10px; /* Add space below button */
}

.summary-btn:hover {
  background-color: #a03165;
}

.download-btn{
  background-color: rgba(233, 117, 15, 0.8); 
  border: none;
  color: #333;
}

.download-btn:hover {
  background-color: rgb(228, 107, 1); 
}

.next-btn {
  border: none;
  background-color: #4a90e2;
}

.next-btn:hover {
  background-color: #2c6db7;
}

.next-btn:disabled {
  background-color: #bcdff5;
  cursor: not-allowed;
}

.next-btn.finish {
  background-color: #4caf50; /* Green for finish */
}

.next-btn.finish:hover {
  background-color: #388e3c; /* Darker green on hover */
}

.summary-section {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Center children horizontally */
  justify-content: center; /* Optional: center vertically if needed */
  text-align: center;
}
.summary-box {
  width: 100%; /* Slightly narrower so it's visually centered */
  margin-top: 10px;
  padding: 10px;
  border: 2px solid #ffddc89b;
  border-radius: 8px;
  background: #ffddc85d;
  color: #333;
  resize: vertical;
}

.loading {
  margin-top: 10px;
  color: #888;
}

.error {
  margin-top: 10px;
  color: rgb(255, 51, 85);
}

</style>
