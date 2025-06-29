<template>
    <div id="navbar">
        <div class="mx-md-5">
            <div class="p-3 d-flex justify-content-between align-items-center">
                <!-- brand -->
                <div>
                    <h4 class="fw-bold brand-font"><router-link to="/" class=" text-decoration-none text-black" >Parkly</router-link></h4>
                </div>

                <!-- auth links -->
                <div v-if="isAuthenticated">
                    <button @click="role === 'user' ? $router.push('/user') : $router.push('/admin')" class="btn btn-outline-primary rounded-pill btn-sm mx-1">
                        Dashboard
                    </button>
                    <button @click="logout" class="btn btn-dark rounded-pill btn-sm mx-1">
                        Logout
                    </button>
                </div>
                <div v-else>
                    <button @click="$router.push('/auth/login')" class="btn btn-outline-dark rounded-pill btn-sm mx-1">
                        Login
                    </button>
                    <button @click="$router.push('/auth/signup')" class="btn btn-primary rounded-pill btn-sm mx-1">
                        Signup
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex/dist/vuex.cjs.js';


export default {
    name: "NavBar",
    inject: ['notify'],
    computed: {
        ...mapGetters(["isAuthenticated", "role"])
    },
    methods: {
        logout() {
            this.$store.dispatch("logout");

            this.notify(
                {
                    message: "Logging out, please login again!",
                    title: "Logout",
                    icon: null,
                    duration: 5000
                }
            );

            this.$router.push('/');
        }
    }
}
</script>
<style></style>