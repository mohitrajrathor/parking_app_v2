<template>
    <div id="adminDashboard" class=" bg-secondary-subtle">
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar (visible on lg and up) -->
                <nav class="col-lg-2 d-none d-lg-flex flex-column vh-100 pt-2 px-2">
                    <div class="mt-1 mx-2 d-lg-flex flex-column vh-100 side-bg-custom rounded-top-5 p-3">
                        <h4 class="text-center text-light fw-bold my-3">Admin Dashboard</h4>
                        <ul class="nav nav-pills flex-column text-center">
                            <li class="nav-item">
                                <router-link to="/admin/dashboard" class="nav-link text-light fw-bold fs-6" href="#">
                                    <span class="nav-icon"><i class="bi bi-speedometer2"></i></span>
                                    Dashboard
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/admin/user" class="nav-link text-light fw-bold fs-6" href="#">
                                    <span class="nav-icon"><i class="bi bi-people-fill"></i></span>
                                    User
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/admin/parkings" class="nav-link text-light fw-bold fs-6" href="#">
                                    <span class="nav-icon"><i class="bi bi-car-front-fill"></i></span>
                                    Parkings
                                </router-link>
                            </li>
                        </ul>
                    </div>
                </nav>

                <!-- Main content -->
                <main class="col-lg-10 overflow-auto vh-100">
                    <NavBar />
                    <div class="container">
                        <router-view></router-view>
                    </div>
                </main>
            </div>
        </div>

        <!-- Bottom nav (visible only on mobile and tablet) -->
        <nav class="d-lg-none fixed-bottom bg-light border-top rounded-top-3">
            <div class="d-flex justify-content-around text-center py-1">
                <router-link to="/admin/dashboard" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-speedometer2"></i></div>
                    <small>Dashboard</small>
                </router-link>
                <router-link to="/admin/user" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-people-fill"></i></div>
                    <small>User</small>
                </router-link>
                <router-link to="/admin/parkings" class="nav-link">
                    <div class="nav-icon"><i class="bi bi-car-front-fill"></i></div>
                    <small>Parkings</small>
                </router-link>
            </div>
        </nav>

    </div>
</template>
<script>
import NavBar from '../components/NavBar.vue';

export default {
    name: "Admin",
    components: {
        NavBar,
    },

}
</script>

<style scoped>
.side-bg-custom {
    background-image: linear-gradient(to bottom, #ff9000, #ffa600, #febc00, #f9d200, #f2e700);
}
</style>