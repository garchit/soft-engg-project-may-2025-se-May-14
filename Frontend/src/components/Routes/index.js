import { createRouter , createWebHistory } from "vue-router";
import LandingPage from "../LandingPage.vue";
import Login from "../Login.vue";
import SignUpArchit from "../Institute/SignUp-Archit.vue";
import SignUp from "../Student/SignUp-Tanuja.vue";
import AdminHome from "../Admin/AdminDashboard.vue";
import StudentHome from "../Student/StudentHome.vue";
import PracticeContent from "../Student/PracticeContent.vue";
import StudentProfile from "../Student/StudentProfile.vue";
import VideosUploadPage from "../Admin/VideosUploadPage.vue";
import StudentPractice from "../Student/StudentPractice.vue";
import InstituteHome from "../Institute/InstituteHome.vue";
import TeacherProgress from "../Institute/TeacherProgress.vue";
import VerifyStudents from "../Institute/VerifyStudents.vue";
import QuizManagement from "../Admin/QuizManagement.vue";
import InstituteProfile from "../Institute/InstituteProfile.vue";
import AdminLayout from "../Institute/InstituteLayout.vue";


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/" , component: LandingPage},
    {path: "/institute" , component: SignUpArchit},
    {path: "/student" , component:SignUp},
    {path: "/login", component: Login},
    {path: "/admin-home" , component: AdminHome},
    {path: "/:student_id/student-home" , component: StudentHome},
    // {path: "/student-practice" , component: StudentPractice},

    // {path : "/studentprofile" , component: StudentProfile},

    {path : "/videos-upload" , component : VideosUploadPage},


    {path: "/student-practice-content" , component: PracticeContent},
    {path: "/student-profile" , component: StudentProfile},

    // Institute routes
    {
      path: '/:institute_id',
      component: AdminLayout,
      children: [
        {path: "institute-home", component: InstituteHome},
        {path: "teacher-progress/:teacher_id", component: TeacherProgress},
        {path: "verify-students", component: VerifyStudents},
        {path: "institute-profile" , component : InstituteProfile}
      ]

    },
    {path: "/quiz-manage" , component : QuizManagement},

  ]
})

export default router;