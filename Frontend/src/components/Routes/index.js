import { createRouter , createWebHistory } from "vue-router";
import LandingPage from "../LandingPage.vue";
import SignUpArchit from "../Institute/SignUp-Archit.vue";
import SignUp from "../Student/SignUp-Tanuja.vue";
import AdminHome from "../Admin/AdminDashboard.vue";
import StudentHome from "../Student/StudentHome.vue";
<<<<<<< Updated upstream
import StudentPractice from "../Student/StudentPractice.vue";
import StudentProfile from "../Student/StudentProfile.vue";
=======
import StudentPracticeContent from "../Student/PracticeContent.vue";
>>>>>>> Stashed changes

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/" , component: LandingPage},
    {path: "/institute" , component: SignUpArchit},
    {path: "/student" , component:SignUp},
    {path: "/admin-home" , component: AdminHome},
    {path: "/student-home" , component: StudentHome},
<<<<<<< Updated upstream
    {path: "/student-practice" , component: StudentPractice},

    {path : "/studentprofile" , component: StudentProfile},
=======
    {path: "/student-practice-content" , component: StudentPracticeContent},
>>>>>>> Stashed changes
  ]
})

export default router;