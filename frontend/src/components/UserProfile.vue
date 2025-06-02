<template>
    <div id="userProfile">
        <div class=" container">
            <div class="p-4 text-light bg-primary border border-5 border-dark bg-gradient rounded-5 col-md-6">
                <div class="d-flex justify-content-center">
                    <div>
                        <img src="../assets/vue.svg" class="img-fluid rounded-circle border border-5 border-light"
                            width="150px" alt="">
                        <h2 class=" text-center mt-3">User</h2>
                    </div>
                </div>

                <div class="d-flex mt-3 justify-content-around">
                    <div class="fs-5">
                        +91 94624 43361
                    </div>
                    <div class="fs-5">
                        <a class=" text-decoration-none text-light"
                            :href="'mailto:' + 'test@gmail.com'">test@parkly.com</a>
                    </div>
                </div>
                <address class="d-flex text-center justify-content-center mt-3 fs-5">
                    XYZ, dummy colony, <br>
                    District, state, india, 326001
                </address>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "UserProfile",
}
</script>
<style scoped></style>