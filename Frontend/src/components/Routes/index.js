import { createRouter , createWebHistory } from "vue-router";
import LandingPage from "../LandingPage.vue";
import SignUpArchit from "../Institute/SignUp-Archit.vue";
import SignUp from "../Student/SignUp-Tanuja.vue";
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/" , component: LandingPage},
    {path: "/institute" , component: SignUpArchit},
    {path: "/student" , component:SignUp}
  ]
})

export default router;