<template>
  <InteractiveLayout>
        <div class="main-container">
        <header class="profile-header">
        <div class="page-heading-box">
          <div class="page-heading">Your Practice Roadmap</div>
            <div class="page-caption">
              Practice smart, earn XP, level up, and race your way to leaderboard glory!
            </div>
          </div>
        <div class="mascot-container">
            <div class="mascot-box">
                <div class="speech-bubble">REVISIT<br/> COURSES!</div>
                <div class="mascot" @click.prevent="trynowfeature">
                  <img src="/src/assets/ReviseAvatar.png" alt="Savvy Mascot" class="mascot-face" />
                </div>
            </div>
        </div>
      </header>

          <!-- Main Content -->
          <div class="content" ref="contentContainer">
            <div class="roadmap-container" :style="{ height: roadmapContainerHeight, transform: `translateY(${scrollOffset}px)` }">
            
              <!-- Road Path -->
              <svg class="road-path" :viewBox="svgViewBox" :height="svgHeight" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="road-fade-mask" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="white" stop-opacity="0" />
                    <stop offset="5%" stop-color="white" stop-opacity="1" />
                    <stop offset="95%" stop-color="white" stop-opacity="1" />
                    <stop offset="100%" stop-color="white" stop-opacity="0" />
                  </linearGradient>

                  <mask id="fade-mask">
                    <rect x="0" y="0" width="100%" height="100%" fill="url(#road-fade-mask)" />
                  </mask>
                </defs>
                <!-- Black Road with Mask -->
                <path
                  :d="svgPath"
                  stroke="black"
                  stroke-width="80"
                  fill="none"
                  stroke-linecap="round"
                  mask="url(#fade-mask)"
                />
                <!-- Dashed Divider with same mask -->
                <path
                  :d="svgPath"
                  stroke="white"
                  stroke-width="6"
                  stroke-dasharray="30 20"
                  fill="none"
                  stroke-linecap="round"
                  mask="url(#fade-mask)"
                />
              </svg>

              <!-- Units -->
              <div class="units-container">
                <!-- Unit Bubbles -->
                <div
                    v-for="unit in units"
                    :key="unit.id"
                    class="unit absolute cursor-pointer transition-all duration-300 hover:scale-110"
                    :style="{ bottom: unit.position.bottom, left: unit.position.left }"
                    @click="$router.push(`/student-unit-practice/${unit.id}`)"
                >
                   <div
                    :class="[
                        'unit-circle',
                        unit.color,
                        selectedUnit === unit.id ? 'ring-4 ring-white ring-opacity-50 scale-105' : ''
                    ]"
                    >
                    <div class="unit-title whitespace-pre-line">{{ unit.title }}</div>
                    </div>
                </div>
                <div
                  v-if="numUnits === 0 || numUnits === 15 || (numUnits > 0 && numUnits < 15)"
                  class="coming-soon-section unit absolute"
                  :style="{ bottom: nextBubblePosition.bottom, left: nextBubblePosition.left, zIndex: 5 }"
                >
                  <div class="coming-soon-text">
                    <template v-if="numUnits === 0">
                      Learn a topic to unlock exciting practice sessions!
                    </template>
                    <template v-else>
                      Congrats! You have unlocked all practices.
                    </template>
                  </div>
                </div>
                </div>

              </div>
            

            <!-- Scroll Controls -->
            <div class="scroll-controls">
            <button @click="scrollToTop" class="scroll-btn">↑</button>
            <button @click="scrollToBottom" class="scroll-btn">↓</button>
            </div>
           </div> 
        </div>
  </InteractiveLayout>
</template>


<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';
import InteractiveLayout from '../InteractiveLayout.vue';
import axios from 'axios';

const API_BASE = '/Finance_Tutor';

// Reactive state for the courses fetched from the API
const courses = ref([]);

// Road segments: each segment extends the previous, so the path for n units is the first n segments joined
const roadSegments = [
  'M 0 110 Q 229 128 379 144',
  'Q 1278 233 322 482',
  'Q -179 615 493 743',
  'Q 1278 900 401 1029',
  'Q -371 1137 531 1403',
  'Q 1232 1595 540 1656',
  'Q -111 1749 531 1908',
  'Q 1141 2072 540 2206',
  'Q -84 2298 540 2437',
  'Q 1298 2639 531 2703',
  'Q -234 2770 543 2970',
  'Q 1247 3138 549 3271',
  'Q -262 3363 558 3479',
  'Q 1312 3643 558 3822',
  'Q -133 3913 739 4092',
  'Q 1367 4204 1220 4166'
];

const bubblePositions = [
  { bottom: '90px', left: '50%' },
  { bottom: '430px', left: '15%' },
  { bottom: '690px', left: '60%' },
  { bottom: '950px', left: '20%' },
  { bottom: '1280px', left: '40%' },
  { bottom: '1500px', left: '80%' },
  { bottom: '1680px', left: '15%' },
  { bottom: '1950px', left: '75%' },
  { bottom: '2210px', left: '18%' },
  { bottom: '2430px', left: '70%' },
  { bottom: '2640px', left: '35%' },
  { bottom: '2930px', left: '60%' },
  { bottom: '3210px', left: '30%' },
  { bottom: '3460px', left: '70%' },
  { bottom: '3750px', left: '45%' },
  { bottom: '4020px', left: '70%' }
];

const numUnits = computed(() => courses.value.length);

const nextBubblePosition = computed(() => {
  return bubblePositions[numUnits.value] || { bottom: '0px', left: '50%' };
});

// A computed property to format the courses for display
const units = computed(() => {
  return courses.value.map((course, i) => ({
    id: course.course_id,
    title: course.course_title,
    color: ['green', 'blue', 'pink', 'yellow'][i % 4],
    position: bubblePositions[i] || { bottom: '0px', left: '50%' }
  }));
});

// The SVG path now depends on the number of courses fetched
const svgPath = computed(() => {
  if (numUnits.value <= 1) {
    return roadSegments.slice(0, 3).join(' ');
  }
  return roadSegments.slice(0, numUnits.value + 3).join(' ');
});

const dynamicHeight = computed(() => {
  if (numUnits.value === 0) return 550;
  const unitHeight = 300 - (30 * Math.min(numUnits.value, 15) / 15);
  return Math.min(Math.max((numUnits.value + 1) * unitHeight, 650), 4200);
});

const roadmapContainerHeight = computed(() => `${dynamicHeight.value}px`);
const svgHeight = dynamicHeight;
const svgViewBox = computed(() => `0 0 1000 ${svgHeight.value}`);

const selectedUnit = ref(null);

const selectUnit = async (unitId) => {
  selectedUnit.value = unitId;
  try {
    const res = await axios.get(`${API_BASE}/course/${unitId}`);
    // Check if course_detail exists and is not empty before accessing
    if (res.data && res.data.course_detail && res.data.course_detail.length > 0) {
      const courseDetails = res.data.course_detail[0];
      console.log(`Starting Unit ${unitId}: ${courseDetails.course_title}`);
      console.log("Unit Details:", courseDetails);
    } else {
      console.log(`No details found for unit ${unitId}`);
    }
  } catch (err) {
    console.error(`Failed to fetch details for unit ${unitId}:`, err);
  }
};

const trynowfeature = () => {
  console.log('This feature is coming soon!');
};

// Scroll handling logic remains the same
const contentContainer = ref(null);
const scrollOffset = ref(0);

const scrollToTop = () => {
  if (contentContainer.value) {
    contentContainer.value.scrollTop = 0;
    scrollOffset.value = 300;
  }
};

const scrollToBottom = () => {
  if (contentContainer.value) {
    const maxScroll = contentContainer.value.scrollHeight - contentContainer.value.clientHeight;
    contentContainer.value.scrollTop = maxScroll;
    scrollOffset.value = 0;
  }
};

const handleScroll = () => {
  if (contentContainer.value) {
    const scrollTop = contentContainer.value.scrollTop;
    const maxScroll = contentContainer.value.scrollHeight - contentContainer.value.clientHeight;
    const scrollPercent = scrollTop / maxScroll;
    scrollOffset.value = (1 - scrollPercent) * 10;
  }
};

// New function to fetch all courses from the API
const fetchCourses = async () => {
  try {
    const res = await axios.get(`${API_BASE}/course`);
    // Correctly access the course_detail array from the response object
    if (res.data && res.data.course_detail) {
      courses.value = res.data.course_detail;
      console.log("Fetched courses:", courses.value);
    } else {
      console.log("No courses found in the response.");
    }
  } catch (err) {
    console.error('Failed to fetch courses:', err);
  }
};

// On mount, fetch the courses and set up the scroll handler
onMounted(async () => {
  await fetchCourses();
  await nextTick();
  if (contentContainer.value) {
    contentContainer.value.addEventListener('scroll', handleScroll);
    scrollToBottom();
  }
});
</script>


<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.main-container {
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
.mascot-container {
  flex: 1; 
  max-width: 16%;
  flex-shrink: 0;
  position: static;
  z-index: 100;
  display: flex;
  flex-direction: column; /* stack speech-bubble + face vertically */
  align-items: self-end; /* center horizontally */
  justify-content: center; /* center vertically if needed */
  text-align: center; /* center text inside speech bubble */
}


.mascot-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.speech-bubble {
  background: #4a90e2;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: center;
  position: relative;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 75%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid #4a90e2;
}

.mascot {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* animation: bounce 2s infinite; */
}

.mascot-face {
  width: 150px;
  height: 150px;
  object-fit: contain;
  transition: transform 0.3s ease;
}
.mascot-face:hover {
  transform: scale(1.1);
}

.content {
  flex: unset;
  overflow-y: auto;
  overflow-x: hidden;
  height: unset;
  border-radius: 25px;
  background: #ffffff4d;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  margin: 5px 20px 80px 20px;
}

.roadmap-container {
  overflow-y: hidden;
  padding-bottom: 10px;
  margin-bottom: 10px;
  position: relative;
  width: 100%;
  height: 500px;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.road-path {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform: scaleY(-1);
  z-index: 1;
}

.units-container {
  position: relative;
  z-index: 2;
  height: 100%;
}

.unit {
  position: absolute;
  cursor: pointer;
  transition: all 0.4s ease;
}

.unit:hover {
  transform: scale(1.1);
}

.unit-circle {
  width: 170px;
  height: 170px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: 700;
  color: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  position: relative;
  transition: all 0.3s ease;
}

.unit-circle::before {
  content: '';
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.4), transparent);
  z-index: -1;
}

.yellow {
  background: linear-gradient(135deg, #fac229 0%, #e4a914 100%);
}

.pink {
  background: linear-gradient(135deg, #e84393 0%, #d73078 100%);
}

.green {
  background: linear-gradient(135deg, #7fb069 0%, #6a9454 100%);
}

.blue {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
}

.unit-number {
  font-size: 1.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
}

.unit-title {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.2;
}

.coming-soon-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.coming-soon-text {
  position: relative;
  text-align: center;
  color: #2c2c2c;
  background: rgba(255, 255, 255, 0.98);
  padding: 1rem 1.2rem;
  border-radius: 20px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.5);
  width: auto;
  max-width: 180px;
  font-size: 0.95rem;
  font-weight: 700;
  border: 10px solid transparent;
  background-clip: padding-box, border-box;
  background-origin: border-box;
  background-image: 
    linear-gradient(rgba(255,255,255,0.98), rgba(255,255,255,0.98)),
    linear-gradient(45deg, #ff9a9e, #fad0c4, #fad0c4);
}


@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.scroll-controls {
  position: fixed;
  top: 65%;
  right: 4rem;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  z-index: 10;
}

.scroll-btn {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.scroll-btn:hover {
  background: white;
  transform: scale(1.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }

  .page-heading-container {
    left: 50%;
    transform: translateX(-50%);
  }

  .page-heading-box {
    width: 80%;
    padding: 1rem 1.5rem;
  }

  .page-heading {
    font-size: 2.2rem;
  }

  .page-caption {
    font-size: 0.9rem;
  }

  .sidebar {
    width: 100%;
    height: auto;
    padding: 1rem;
  }
  
  .nav-menu {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .practice-title {
    font-size: 2rem;
  }
  
  .unit-circle {
    width: 120px;
    height: 120px;
  }
  
  .mascot-container {
    top: 4rem;
    right: 1rem;
  }
}

@media (max-width: 480px) {
  .page-heading {
    font-size: 1.2rem;
  }

  .page-caption {
    font-size: 0.5rem;
  }

  .page-heading-box {
    width: 50%;
    padding: 0.8rem 1rem;
  }
}

</style>