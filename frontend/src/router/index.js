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
import User from "../pages/User.vue";
import UserDashboard from "../components/UserDashboard.vue";
import UserProfile from "../components/UserProfile.vue";
import UserSupport from "../components/UserSupport.vue";
import store from "../store";
import AddParking from "../components/AddParking.vue";
import Parking from "../pages/Parking.vue";


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
        meta: {
            authRequired: true,
            role: "admin",
        },
        children: [
            {
                path: 'dashboard',
                name: "AdminDashboard",
                component: AdminDashboard,
            },
            {
                path: 'user-manager',
                name: "UserManager",
                component: UserManager,
            },
            {
                path: 'parkings',
                name: "Parkings",
                component: ParkingManager,
            },

            {
                path: 'add-parking',
                name: "AddParking",
                component: AddParking,
            },

        ]
    },
    {
        path: "/user",
        name: "User",
        component: User,
        redirect: "/user/dashboard",
        meta: {
            authRequired: true,
            role: "user",
        },
        children: [
            {
                path: 'dashboard',
                name: "UserDashboard",
                component: UserDashboard,
            },
            {
                path: 'profile',
                name: "Profile",
                component: UserProfile,
            },
            {
                path: 'support',
                name: "UserSupport",
                component: UserSupport,
            },
        ]
    },
    {
        path: '/parking/:id',
        name: "Parking",
        component: Parking,
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


router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated;
    const userRole = store.getters.role;

    if (to.meta.authRequired) {
        if (!isAuthenticated) {
            if (to.meta.role == 'admin') {
                return next({ name: "AdminLogin" });
            }
            else return next({ name: "Login" });
        }

        if (to.meta.role && to.meta.role !== userRole) {
            return next({ name: "Home" });
        }

        return next();
    }


    return next();
});


export default router