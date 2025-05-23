<template>
    <div id="navbar">
        <div class="mx-md-5">
            <div class="p-3 d-flex justify-content-between align-items-center">
                <!-- brand -->
                <div>
                    <h2 class="fw-bold brand-font">Parkly</h2>
                </div>

                <!-- auth links -->
                <div>
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
}
</script>
<style></style>