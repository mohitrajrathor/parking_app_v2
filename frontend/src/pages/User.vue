<template>
    <div id="adminDashboard" class=" bg-secondary-subtle">
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar (visible on lg and up) -->
                <nav class="col-lg-2 d-none d-lg-block bg-primary bg-gradient vh-100 p-0">
                    <div class="d-flex flex-column h-100 p-3">
                        <h4 class="text-center text-light fw-bold my-3">Dashboard</h4>
                        <ul class="nav nav-pills flex-column mb-4">
                            <li class="nav-item mb-2">
                                <router-link to="/user/dashboard" class="nav-link text-light fw-bold fs-6 px-3 py-2">
                                    <span class="nav-icon me-2"><i class="bi bi-speedometer2"></i></span>
                                    Dashboard
                                </router-link>
                            </li>
                            <li class="nav-item mb-2">
                                <router-link to="/user/profile" class="nav-link text-light fw-bold fs-6 px-3 py-2">
                                    <span class="nav-icon me-2"><i class="bi bi-person-fill"></i></span>
                                    Profile
                                </router-link>
                            </li>
                            <li class="nav-item mb-2">
                                <router-link to="/user/support" class="nav-link text-light fw-bold fs-6 px-3 py-2">
                                    <span class="nav-icon me-2"><i class="bi bi-headset"></i></span>
                                    Support
                                </router-link>
                            </li>
                        </ul>
                    </div>
                </nav>

                <!-- Main content -->
                <main class="col-lg-10 overflow-auto vh-100">
                    <NavBar />
                    <div class="container" style="margin-bottom: 75px;">
                        <router-view></router-view>
                    </div>
                </main>
            </div>
        </div>

        <!-- Bottom nav (visible only on mobile and tablet) -->
        <nav class="d-lg-none fixed-bottom bg-light border-top rounded-top-3">
            <div class="d-flex justify-content-around text-center py-1">
                <router-link to="/user/dashboard" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-speedometer2"></i></div>
                    <small>Dashboard</small>
                </router-link>
                <router-link to="/user/profile" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-person-fill"></i></div>
                    <small>Profile</small>
                </router-link>
                <router-link to="/user/support" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-headset"></i></div>
                    <small>Support</small>
                </router-link>
            </div>
        </nav>

    </div>
</template>
<script>
import NavBar from '../components/NavBar.vue';

export default {
    name: "User",
    components: {
        NavBar,
    },

}
</script>

<style scoped>
</style>