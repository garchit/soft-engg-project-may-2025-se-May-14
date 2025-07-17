<script setup>
import {

  CAccordion, CAccordionItem, CAccordionHeader, CAccordionBody,
  CButton, CModal, CModalHeader, CModalTitle, CModalBody, CModalFooter,
  CForm, CFormInput, CFormTextarea
} from '@coreui/vue'
import Sidebar from './Sidebar.vue'
// import SIdebarArchit from './SIdebarArchit.vue'
import { ref, onMounted } from 'vue'
import deleteIcon from '@/assets/delete.png'
import playButton from '@/assets/play-button.png'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'

// import VideoPlay from 'Frontend/node_modules/vue3-video-play'
// import VideoPlay from 'vue3-video-play'
// Frontend\node_modules\vue3-video-play
// C:\Users\Archit Garg\Desktop\Project - SE\Frontend\node_modules\vue3-video-play
// import 'vue3-video-play/dist/style.css'
// import delete from '@/assets/delete.png'
// Sidebar navigation state
const activeTab = ref('lectures')

const toast = useToast()
// API base URL
const API_BASE_URL = 'http://127.0.0.1:5000/Finance_Tutor'

// Lectures state
const Courses = ref([])
const visible = ref(false)
const newTitle = ref('')
const newDescription = ref('')
const selectedCourseIndex = ref(null)
const newLectureTitle = ref('')
const newLectureVideoUrl = ref('')
const newLectureDescription = ref('')
const lectureModalVisible = ref(false)
const selectedCourseId = ref(null)
const showVideoModal = ref(false)
const currentVideoUrl = ref('')

// Fetch courses from API
const fetchCourses = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/course`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const data = await response.json()
    console.log('Fetched courses:', data)
    Courses.value = data.course_detail || []
  } catch (e) {
    Courses.value = []
  }
}

// Add course
// const addCourse = () => {
//   if (newTitle.value.trim() && newDescription.value.trim()) {
//     Courses.value.push({
//       course_title: newTitle.value,
//       course_description: newDescription.value,
//       lectures: []
//     })
//     newTitle.value = ''
//     newDescription.value = ''
//     visible.value = false
//   }
// }

// ...existing code...

const addCourse = async () => {
  if (newTitle.value.trim() && newDescription.value.trim()) {
    // Prepare the payload
    const payload = {
      title: newTitle.value,
      description: newDescription.value,
    }

    try {
      const response = await fetch(`${API_BASE_URL}/course`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      console.log(response)
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      console.log('Course added successfully:', data);
      // Optionally, add the new course to Courses or refetch
      Courses.value.push({
        course_title: newTitle.value,
        course_description: newDescription.value,
        lectures: []
      });

      // Clear form and close modal
      newTitle.value = '';
      newDescription.value = '';
      visible.value = false;
      toast.success('Course added successfully!')
      // Optionally, refetch courses from server:
      // await fetchCourses();

    } catch (error) {
      console.error('Failed to add course:', error);
      toast.error('Failed to add course!')
      // Optionally show an error message to the user
    }
  }
}

// Add lecture
// const addLectureToCourse = () => {
//   if (newLectureTitle.value.trim() && newLectureVideoUrl.value.trim()) {
//     Courses.value[selectedCourseIndex.value].lectures.push({
//       lecture_title: newLectureTitle.value,
//       lecture_description: newLectureDescription.value,
//       lecture_link: newLectureVideoUrl.value
//     })
//     newLectureTitle.value = ''
//     newLectureVideoUrl.value = ''
//     newLectureDescription.value = ''
//     lectureModalVisible.value = false
//   }
// }

const addLectureToCourse = async () => {
  if (newLectureTitle.value.trim() && newLectureVideoUrl.value.trim()) {
    const payload = {
      unit_id: selectedCourseId.value,
      title: newLectureTitle.value,
      description: newLectureDescription.value,
      link: newLectureVideoUrl.value
    }

    try {
      const response = await fetch(`${API_BASE_URL}/lecture`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();

      // Optionally, add the new lecture to the UI or refetch lectures
      Courses.value[selectedCourseIndex.value].lectures.push({
        lecture_title: newLectureTitle.value,
        lecture_description: newLectureDescription.value,
        lecture_link: newLectureVideoUrl.value
      });
      // Clear form and close modal
      newLectureTitle.value = '';
      newLectureVideoUrl.value = '';
      newLectureDescription.value = '';
      lectureModalVisible.value = false;
      toast.success('Lecture added successfully!')
      // Optionally, refetch courses from server:
      // await fetchCourses();

    } catch (error) {
      console.error('Failed to add lecture:', error);
      toast.error('Failed to add lecture!')
      // Optionally show an error message to the user
    }
  }
}

const openLectureModal = (courseIndex, course_id) => {
  console.log('Opening lecture modal for course:', course_id)
  selectedCourseId.value = course_id
  selectedCourseIndex.value = courseIndex
  lectureModalVisible.value = true

}

// Add this function to convert YouTube URLs to embed format
const getYouTubeEmbedUrl = (url) => {
  let videoId = ''

  // Handle different YouTube URL formats
  if (url.includes('youtube.com/watch?v=')) {
    videoId = url.split('v=')[1]?.split('&')[0]
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0]
  } else if (url.includes('youtube.com/embed/')) {
    return url // Already in embed format
  }

  return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0` : ''
}

// Update your playLecture function
const playLecture = (url) => {
  console.log('Original YouTube URL:', url)
  const embedUrl = getYouTubeEmbedUrl(url)
  console.log('Embed URL:', embedUrl)

  if (!embedUrl) {
    toast.error('Invalid YouTube URL format')
    return
  }

  currentVideoUrl.value = embedUrl
  showVideoModal.value = true
}

// Add function to close video modal
const closeVideoModal = () => {
  showVideoModal.value = false
  currentVideoUrl.value = ''
}

// Delete lecture function
const deleteLecture = async (courseIndex, lectureIndex, lectureId) => {
  console.log('Deleting lecture with ID:', lectureId);
  if (confirm('Are you sure you want to delete this lecture?')) {
    try {
      const response = await fetch(`${API_BASE_URL}/lecture/${lectureId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      // Remove from local array
      Courses.value[courseIndex].lectures.splice(lectureIndex, 1);
      toast.success('Lecture deleted successfully!');

    } catch (error) {
      console.error('Failed to delete lecture:', error);
      toast.error('Failed to delete lecture!');
    }
  }
}

// Delete course function
const deleteCourse = async (courseIndex, courseId) => {
  console.log('Deleting course with ID:', courseId);
  if (confirm('Are you sure you want to delete this course? This action cannot be undone.')) {
    try {
      const response = await fetch(`${API_BASE_URL}/course/${courseId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
      // Remove from local array
      Courses.value.splice(courseIndex, 1);
      toast.success('Course deleted successfully!');
      
    } catch (error) {
      console.error('Failed to delete course:', error);
      toast.error('Failed to delete course!');
    }
  }
}


onMounted(fetchCourses)
</script>

<template>
  <div style="display: flex; min-height: 100vh;">
    <!-- Sidebar -->
    <Sidebar />
    <!-- Main Content -->
    <div style="flex: 1; background: linear-gradient(135deg, #E54C91 0%, #FFC800 100%);">
      <div v-if="activeTab === 'dashboard'" style="padding:2rem">
        <h2>Dashboard</h2>
        <p>Dashboard content here.</p>
      </div>
      <div v-else-if="activeTab === 'institute'" style="padding:2rem">
        <h2>Institute</h2>
        <p>Institute content here.</p>
      </div>
      <div v-else>
        <!-- Lectures Content -->
        <h1 class="heading">ADD YOUR CONTENT HERE</h1>
        <div class="accordion-container">
          <div style="text-align: right; margin-bottom: 1rem;">
            <CButton class="btn btn-warning" color="primary" @click="visible = true">+ New Course</CButton>
          </div>
          <CAccordion flush>
            <CAccordionItem v-for="(Course, index) in Courses" :key="Course.course_id || index">
              <CAccordionHeader>
                <div style="display: flex; justify-content: space-between; width: 100%; align-items: center;">
                  <span>{{ Course.course_title }}</span>
                  <CButton size="sm" color="info" @click.stop="openLectureModal(index, Course.course_id)">+ Add Lecture
                  </CButton>

                  <CButton @click.stop="deleteCourse(index, Course.course_id)"
                    style="display: flex; justify-content: space-between; align-items: center;"
                     title="Delete Course" color="danger">
                    <!-- <img :src="deleteIcon" alt="Delete" style="width: 20px; height: 20px;" /> -->
                     Delete Course
                  </CButton>

                </div>
              </CAccordionHeader>
              <CAccordionBody>
                <strong>Description:</strong> {{ Course.course_description }}
                <div v-if="Course.lectures && Course.lectures.length" style="margin-top: 1rem;">
                  <strong>Lectures:</strong>
                  <div class="lecture-list">
                    <div v-for="(lecture, i) in Course.lectures" :key="lecture.lecture_id || i" class="lecture-card">
                      <div class="lecture-header">
                        <span class="lecture-title">{{ lecture.lecture_title }}</span>
                        <!-- <a :href="lecture.lecture_link" target="_blank">
                          <img :src="playButton" alt="Play" style="width: 32px; height: 32px;" />
                        </a> -->

                        <!-- Inside your lecture-card -->
                        <!-- <button
                          style="background: none; border: none; padding: 0; cursor: pointer;">
                          <img :src="playButton" alt="Play" style="width: 32px; height: 32px;" />
                        </button> -->


                        <button @click="deleteLecture(index, i, lecture.lecture_id)" class="action-btn delete-btn"
                          title="Delete Lecture">
                          <img :src="deleteIcon" alt="Delete" style="width: 22px; height: 22px;" />
                        </button>


                        <!-- Replace your current play button with this -->
                        <button @click="playLecture(lecture.lecture_link)"
                          style="background: none; border: none; padding: 0; cursor: pointer;">
                          <img :src="playButton" alt="Play" style="width: 32px; height: 32px;" />
                        </button>




                      </div>
                      <div class="lecture-description">{{ lecture.lecture_description }}</div>
                    </div>
                  </div>
                </div>
              </CAccordionBody>
            </CAccordionItem>
          </CAccordion>
          <!-- Course Modal -->
          <CModal :visible="visible" @close="visible = false" alignment="center" size="lg">
            <CModalHeader>
              <CModalTitle>Add New Course</CModalTitle>
            </CModalHeader>
            <CModalBody>
              <CForm>
                <CFormInput v-model="newTitle" label="Course Title" placeholder="Enter course title" class="mb-3" />
                <CFormTextarea v-model="newDescription" label="Course Description" rows="4"
                  placeholder="Enter course description" />
              </CForm>
            </CModalBody>
            <CModalFooter>
              <CButton color="secondary" @click="visible = false">Cancel</CButton>
              <CButton color="success" @click="addCourse">Add</CButton>
            </CModalFooter>
          </CModal>
          <!-- Lecture Modal -->
          <CModal :visible="lectureModalVisible" @close="lectureModalVisible = false" alignment="center" size="lg">
            <CModalHeader>
              <CModalTitle>Add Lecture</CModalTitle>
            </CModalHeader>
            <CModalBody>
              <CForm>
                <CFormInput v-model="newLectureTitle" label="Lecture Title" placeholder="Enter lecture title"
                  class="mb-3" />
                <CFormInput v-model="newLectureDescription" label="Lecture Description"
                  placeholder="Enter lecture description" class="mb-3" />
                <CFormInput v-model="newLectureVideoUrl" label="Lecture Link" placeholder="Enter video link" />
              </CForm>
            </CModalBody>
            <CModalFooter>
              <CButton color="secondary" @click="lectureModalVisible = false">Cancel</CButton>
              <CButton color="success" @click.stop="addLectureToCourse">Add Lecture</CButton>
            </CModalFooter>
          </CModal>

          <!-- Video Modal -->
          <!-- YouTube Video Modal -->
          <CModal :visible="showVideoModal" @close="closeVideoModal" alignment="center" size="xl">
            <CModalHeader>
              <CModalTitle>Video Player</CModalTitle>
            </CModalHeader>
            <CModalBody>
              <div style="text-align: center;">
                <iframe v-if="currentVideoUrl" :src="currentVideoUrl" width="100%" height="450" frameborder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen style="border-radius: 8px;">
                </iframe>
              </div>
            </CModalBody>
            <CModalFooter>
              <CButton color="secondary" @click="closeVideoModal">Close</CButton>
            </CModalFooter>
          </CModal>



        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.accordion-container {
  margin-top: 4%;
  margin-left: 20%;
  margin-right: 10%;
  padding: 50px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 10px;
}

.heading {
  text-align: center;
  color: rgb(155, 50, 103);
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.lecture-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 10px;
}

.lecture-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(79, 140, 255, 0.07);
  padding: 18px 22px;
  transition: box-shadow 0.2s;
  border-left: 5px solid #81AB40;
}

.lecture-card:hover {
  box-shadow: 0 4px 16px rgba(79, 140, 255, 0.15);
  border-left: 5px solid #e54c91;
}

.lecture-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lecture-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #4f8cff;
  display: flex;
  align-items: center;
}

.lecture-icon {
  font-size: 1.5rem;
  color: #81AB40;
  margin-right: 8px;
}

.lecture-watch-btn {
  background: #81AB40;
  color: #fff;
  padding: 6px 18px;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s;
}

.lecture-watch-btn:hover {
  background: #e54c91;
  color: #fff;
}

.lecture-description {
  margin-top: 8px;
  color: #333;
  font-size: 0.98rem;
}
</style>
