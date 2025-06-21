<template>
    <div id="navbar">
        <div class="mx-md-5">
            <div class="p-3 d-flex justify-content-between align-items-center">
                <!-- brand -->
                <div>
                    <h2 class="fw-bold brand-font"><router-link to="/" class=" text-decoration-none text-black" >Parkly</router-link></h2>
                </div>

                <!-- auth links -->
                <div v-if="$store.getters.isAuthenticated">
                    <button @click="logout" class="btn btn-dark rounded-pill mx-1">
                        Logout
                    </button>
                </div>
                <div v-else>
                    <button @click="$router.push('/auth/login')" class="btn btn-outline-dark rounded-pill mx-1">
                        Login
                    </button>
                    <button @click="$router.push('/auth/signup')" class="btn btn-primary rounded-pill mx-1">
                        Signup
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "NavBar",
    inject: ['notify'],
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