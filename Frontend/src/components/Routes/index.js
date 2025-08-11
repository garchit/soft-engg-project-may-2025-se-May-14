import { createRouter , createWebHistory } from "vue-router";
import LandingPage from "../LandingPage.vue";
import Login from "../Login.vue";
import SignUpArchit from "../Institute/SignUp-Archit.vue";
import SignUp from "../Student/SignUp-Tanuja.vue";
import AdminHome from "../Admin/AdminDashboard.vue";
import VideosUploadPage from "../Admin/VideosUploadPage.vue";
import InstituteHome from "../Institute/InstituteHome.vue";
import TeacherProgress from "../Institute/TeacherProgress.vue";
import VerifyStudents from "../Institute/VerifyStudents.vue";
import QuizManagement from "../Admin/QuizManagement.vue";
import InstituteProfile from "../Institute/InstituteProfile.vue";

import StudentHome from "../Student/StudentHome.vue";
import PracticeContent from "../Student/PracticeContent.vue";
import LeaderBoard from "../Student/LeaderBoard.vue";
import StudentProfile from "../Student/StudentProfile.vue";
import Learn from "../Student/Learn.vue";
import LearnVideos from "../Student/LearnVideos.vue";
import StudentPractice from "../Student/StudentPractice.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/" , component: LandingPage},
    {path: "/institute" , component: SignUpArchit},
    {path: "/student" , component:SignUp},
    {path: "/login", component: Login},
    {path: "/admin-home" , component: AdminHome},
    
    {path: "/student-home" , component: StudentHome},
    {path: "/student-practice-content" , component: PracticeContent},
    {path: "/student-leaderboard" , component: LeaderBoard},
    {path: "/student-profile" , component: StudentProfile},
    {path: "/student-learn" , component: Learn},
    {path: "/student-learn/:unitId", component: LearnVideos},
    {path: '/student-unit-practice/:unitId', component: StudentPractice},

    {path : "/videos-upload" , component : VideosUploadPage},
    {path: "/:institute_id/institute-home", component: InstituteHome},
    {path: "/:institute_id/teacher-progress/:teacher_id", component: TeacherProgress},
    {path: "/:institute_id/verify-students", component: VerifyStudents},
    {path: "/quiz-manage" , component : QuizManagement},

    {path: "/InstituteProfile" , component : InstituteProfile}
  ]
})

export default router;