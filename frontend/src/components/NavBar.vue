<template>
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm rounded-bottom-4 px-2 px-md-5 py-2">
  <div class="container-fluid">
    <router-link to="/" class="navbar-brand fw-bold fs-3 text-dark brand-font">Parkly</router-link>
    <div class="d-flex align-items-center ms-auto">
      <template v-if="isAuthenticated">
        <button @click="role === 'user' ? $router.push('/user') : $router.push('/admin')" class="btn btn-outline-primary rounded-pill btn-sm mx-1">
          <i class="bi bi-speedometer2 me-1"></i> Dashboard
        </button>
        <button @click="logout" class="btn btn-dark rounded-pill btn-sm mx-1">
          <i class="bi bi-box-arrow-right me-1"></i> Logout
        </button>
      </template>
      <template v-else>
        <button @click="$router.push('/auth/login')" class="btn btn-outline-dark rounded-pill btn-sm mx-1">
          <i class="bi bi-box-arrow-in-right me-1"></i> Login
        </button>
        <button @click="$router.push('/auth/signup')" class="btn btn-primary rounded-pill btn-sm mx-1">
          <i class="bi bi-person-plus me-1"></i> Signup
        </button>
      </template>
    </div>
  </div>
</nav>
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
<style>
.brand-font {
  letter-spacing: 1px;
}
</style>