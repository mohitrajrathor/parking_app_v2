<template>
    <div class="container d-flex flex-column justify-content-center align-items-center min-vh-100">
        <div class="w-100" style="max-width: 400px;">
            <div v-if="isLoading" class="d-flex flex-column align-items-center justify-content-center py-5">
                <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="fw-bold text-primary">Verifying your email...</div>
            </div>
            <div v-else>
                <div v-if="isTokenValid" class="alert alert-success rounded-4 text-center py-4">
                    <i class="bi bi-check-circle-fill fs-2 text-success mb-2"></i>
                    <h4 class="fw-bold">Email Verified!</h4>
                    <p class="mb-3">Your email has been successfully verified. You can now access all services.</p>
                    <button class="btn btn-primary rounded-pill px-4 fw-bold" @click="$router.push({ name: 'UserDashboard' })">
                        Go to Dashboard
                    </button>
                </div>
                <div v-else class="alert alert-danger rounded-4 text-center py-4">
                    <i class="bi bi-x-circle-fill fs-2 text-danger mb-2"></i>
                    <h4 class="fw-bold">Invalid or Expired Token</h4>
                    <p class="mb-3">The verification link is invalid or has expired. Please request a new verification email or contact support.</p>
                    <button class="btn btn-outline-primary rounded-pill px-4 fw-bold" @click="$router.push({ name: 'Signup' })">
                        Go to Signup
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { onMounted } from 'vue';
export default {
    name: "VerifyMail",
    data() {
        return {
            isLoading: false,
            isTokenValid: false,
        }
    },
    computed: {
        token() {
            return this.$route.query.token;
        }
    },
    methods: {
        async confirmMail() {
            try {
                this.isLoading = true;
                const baseUrl = import.meta.env.VITE_BASE_URL;
                const response = await fetch(`${baseUrl}/api_v1/auth/confirm-mail?token=${this.token}`);
                if (!response.ok) {
                    this.isTokenValid = false;
                    return;
                }
                const data = await response.json();
                this.$store.dispatch("login", {
                    role: data.role,
                    token: data.token,
                    refreshToken: data.refresh_token,
                });
                this.isTokenValid = true;
            } catch (err) {
                console.error(err);
                this.isTokenValid = false;
            } finally {
                this.isLoading = false;
            }
        }
    },
    mounted() {
        this.confirmMail();
    }
}
</script>
<style>
    
</style>