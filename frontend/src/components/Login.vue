<template>
    <div class="p-4 bg-transparent border border-2 rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">
                <h3 class=" text-center mb-3">Login</h3>
                <p v-if="errorMsg" class="text-center text-danger fw-bold">
                    {{ errorMsg }}
                </p>
                <form @submit.prevent="handleLogin">
                    <div>
                        <div class="form-floating mb-3">
                            <input type="email" required class="form-control" id="email" name="email" v-model="email" />
                            <label for="email"><span><i class="bi bi-envelope-at-fill"></i></span> Email</label>
                        </div>

                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" v-model="password" id="" name="password"
                                required minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                                title="Password must contain at least one number, one uppercase and lowercase letter, and be at least 8 characters long" />
                            <label for="password"><span><i class="bi bi-unlock-fill"></i></span> Password</label>
                        </div>
                    </div>
                    <div>

                    </div>
                    <button type="submit" class="btn text-dark  lime-green w-100 rounded-3">
                        Login
                    </button>
                    <p class="mt-3 mx-4">
                        Don't have an account <router-link class=" text-decoration-none text-dark fw-bold"
                            to="/auth/signup">Signup</router-link>.
                    </p>
                </form>
            </div>
            <div class="d-flex justify-content-center">
                <div class="lime-green rounded-top-pill" style="height: 10px; width: 100px;">
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapActions } from 'vuex';


export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            isLoading: false,
            errorMsg: "",
        }
    },
    inject: ['notify'],
    methods: {
        ...mapActions('user', ['fetchCurrentUser']),

        async handleLogin() {
            try {

                this.isLoading = true;

                if (!this.email & !this.password) {
                    this.notify({
                        message: 'First fill all required fields',
                        title: 'Warning',
                        icon: 'https://cdn-icons-png.flaticon.com/512/4201/4201973.png',
                        duration: 5000
                    })
                }

                const baseUrl = import.meta.env.VITE_BASE_URL;
                const response = await fetch(`${baseUrl}/api_v1/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                    })
                });
                if (!response.ok) {
                    const data = await response.json();
                    this.notify({
                        message: data.message || "Unable to Login!",
                        title: 'Warning',
                        icon: 'https://cdn-icons-png.flaticon.com/512/1680/1680012.png',
                        duration: 5000
                    })
                    throw new Error(data.message || "Failed to login!");

                }

                const data = await response.json();

                this.$store.dispatch("login", {
                    role: data.role,
                    token: data.token,
                    refreshToken: data.refresh_token
                });

                this.notify({
                    message: 'You are successfully logged in as user!',
                    title: 'Login Success',
                    icon: 'https://cdn-icons-png.flaticon.com/512/190/190411.png',
                    duration: 5000
                })

                this.$router.push({ name: "User" });

                this.fetchCurrentUser();


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