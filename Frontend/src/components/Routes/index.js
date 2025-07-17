import { createRouter , createWebHistory } from "vue-router";
import LandingPage from "../LandingPage.vue";
import SignUpArchit from "../Institute/SignUp-Archit.vue";
import SignUp from "../Student/SignUp-Tanuja.vue";
import AdminHome from "../Admin/AdminDashboard.vue";
import StudentHome from "../Student/StudentHome.vue";
import PracticeContent from "../Student/PracticeContent.vue";
import StudentProfile from "../Student/StudentProfile.vue";
import VideosUploadPage from "../Admin/VideosUploadPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/" , component: LandingPage},
    {path: "/institute" , component: SignUpArchit},
    {path: "/student" , component:SignUp},
    {path: "/admin-home" , component: AdminHome},
    {path: "/student-home" , component: StudentHome},
    {path: "/student-practice" , component: StudentPractice},

    {path : "/studentprofile" , component: StudentProfile},

    {path : "/videos-upload" , component : VideosUploadPage},


    {path: "/student-practice-content" , component: PracticeContent},
    {path: "/student-profile" , component: StudentProfile}
  ]
})

export default router;