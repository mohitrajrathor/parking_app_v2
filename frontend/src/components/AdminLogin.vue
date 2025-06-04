<template>
    <div class="p-4 bg-transparent border border-2 rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">
                <h3 class=" text-center mb-3">Admin</h3>
                <p class=" text-center text-danger fw-bold">
                    {{ errorMsg }}
                </p>
                <form @submit.prevent="handleAdminLogin">
                    <div>
                        <div class="form-floating mb-3">
                            <input type="text" required class="form-control" v-model="username" />
                            <label for="username"><span><i class="bi bi-person-fill-lock"></i></span> username</label>
                        </div>

                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" v-model="password" required minlength="8"
                                pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                                title="Password must contain at least one number, one uppercase and lowercase letter, and be at least 8 characters long" />
                            <label for="formId1"><span><i class="bi bi-unlock-fill"></i></span> Password</label>
                        </div>
                    </div>
                    <div>

                    </div>
                    <button type="submit" :disabled="isLoading"
                        class="btn text-light btn-danger w-100 rounded-3 d-flex justify-content-center align-items-center">
                        <span v-if="!isLoading">Login</span>
                        <div v-else class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </button>

                    <p class="mt-3 mx-4">
                        Don't have Admin access <a class="text-decoration-none text-dark fw-bold"
                            href="mailto:developer@parkly.com?subject=give%20me%20admin%20access">ask
                            developer</a>.
                    </p>
                </form>
            </div>
            <div class="d-flex justify-content-center">
                <div class="bg-danger rounded-top-pill" style="height: 10px; width: 100px;">
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { inject } from 'vue';

export default {
    name: "AdminLogin",
    data() {
        return {
            username: "",
            password: "",
            isLoading: false,
            errorMsg: "",
        }
    },

    inject: ['notify'],

    methods: {
        async handleAdminLogin() {
            try {

                this.isLoading = true;

                if (!this.username & !this.password) {
                    this.notify({
                        message: 'First fill all required fields',
                        title: 'Warning',
                        icon: 'https://cdn-icons-png.flaticon.com/512/4201/4201973.png',
                        duration: 5000
                    })
                }

                const response = await fetch(`http://127.0.0.1:1234/api_v1/auth/admin-login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                    })
                });
                if (!response.ok) throw new Error("failed to login!");

                const data = await response.json();

                this.$store.dispatch("login", {
                    role: data.role,
                    token: data.token,
                    refreshToken: data.refresh_token
                });

                this.notify({
                    message: 'You are successfully logged in as admin!',
                    title: 'Login Success',
                    icon: 'https://cdn-icons-png.flaticon.com/512/190/190411.png',
                    duration: 5000
                })

                this.$router.push({ name: "Admin" });

            } catch (e) {
                console.error(e.message)
                this.errorMsg = e.message;

            } finally {
                this.isLoading = false;
            }
        },
    }
}
</script>
<style></style>