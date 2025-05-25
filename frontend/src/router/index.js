import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Auth from "../pages/Auth.vue";
import Login from "../components/Login.vue";
import Signup from "../components/Signup.vue"
import AdminLogin from "../components/AdminLogin.vue"
import Admin from "../pages/Admin.vue";
import ParkingManager from "../components/ParkingManager.vue"
import UserManager from "../components/UserManager.vue";
import AdminDashboard from "../components/AdminDashboard.vue"
import NotFound from "../components/NotFound.vue";


const routes = [
    {
        path: '/',
        name: "Home",
        component: Home,
    },
    {
        path: '/auth',
        name: "Auth",
        redirect: "/auth/login",
        component: Auth,
        children: [
            {
                path: 'login',
                name: "Login",
                component: Login,
            },
            {
                path: 'signup',
                name: "Signup",
                component: Signup,
            },
            {
                path: 'admin-login',
                name: "AdminLogin",
                component: AdminLogin,
            },
        ]
    },
    {
        path: '/admin',
        name: "Admin",
        component: Admin,
        redirect: "/admin/dashboard",
        children: [
            {
                path: 'dashboard',
                name: "AdminDashboard",
                component: AdminDashboard,
            },
            {
                path: 'user',
                name: "User",
                component: UserManager,
            },{
                path: 'parkings',
                name: "Parkings",
                component: ParkingManager,
            },
        ]
    },
    {
        path: '/:pathMatch(.*)*',
        name: "Notfound",
        component: NotFound,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


// router.beforeEach()     // TODO: update after create store and api setup.


export default router