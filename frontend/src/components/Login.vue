<template>
    <div class="p-4 bg-transparent border border-2 rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">
                <h3 class=" text-center mb-3">Login</h3>
                <form @submit.prevent="">
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
export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
        }
    },
}
</script>
<style></style>