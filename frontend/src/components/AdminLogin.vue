<template>
    <div class="p-4 bg-transparent border border-2 rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">
                <h3 class=" text-center mb-3">Admin</h3>
                <form @submit.prevent="">
                    <div>
                        <div class="form-floating mb-3">
                            <input type="text" required class="form-control" v-model="username" />
                            <label for="username"><span><i class="bi bi-person-fill-lock"></i></span> username</label>
                        </div>

                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" v-model="password"
                                required minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                                title="Password must contain at least one number, one uppercase and lowercase letter, and be at least 8 characters long" />
                            <label for="formId1"><span><i class="bi bi-unlock-fill"></i></span> Password</label>
                        </div>
                    </div>
                    <div>

                    </div>
                    <button type="submit" class="btn text-light btn-danger w-100 rounded-3">
                        Login
                    </button>
                    <p class="mt-3 mx-4">
                        Don't have Admin access <a class="text-decoration-none text-dark fw-bold" href="mailto:developer@parkly.com?subject=give%20me%20admin%20access">ask
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
export default {
    name: "AdminLogin",
    data() {
        return { 
            username: "",
            password: ""
        }
    }
}
</script>
<style></style>