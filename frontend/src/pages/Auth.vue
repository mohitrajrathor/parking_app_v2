<template>
    <div id="auth" class="bg-custom">
        <div class="d-flex vh-100 justify-content-center align-items-center">
            <div id="authForm" class="">
                <div class="mb-5">
                    <h1 class="fw-bold brand-font text-center text-light">
                        <router-link to="/" class="text-decoration-none text-light">Parkly</router-link>
                    </h1>
                </div>
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "Auth",
}
</script>
<style scoped>
.bg-custom {
    background-image: linear-gradient(to right, #00167e, #005bcc, #0092d5, #00c296, #00eb15);
}
</style>