import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Auth from "../pages/Auth.vue";
import Login from "../components/Login.vue";
import Signup from "../components/Signup.vue"
import AdminLogin from "../components/AdminLogin.vue"


const routes = [
    {
        path: '/',
        name: "Home",
        component: Home,
    },
    {
        path: '/auth',
        name: "Auth",
        redirect: "Login",
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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


// router.beforeEach()     // TODO: update after create store and api setup.


export default router