<template>
    <NavBar />
    <div id="notFound">
        <div class="vh-100 d-flex justify-content-center align-items-center">
            <div class=" text-center">
                <h1>
                    Unauthorized
                </h1>
                <p>Access denied !</p>
                <button @click="$router.push({ name: 'Home' })" class="btn btn-dark">Home</button>
            </div>
        </div>
    </div>
    <Footer></Footer>
</template>
<script>
import NavBar from "./NavBar.vue";
import Footer from "./Footer.vue";


export default {
    name: "Unauthorized",
    components: {
        NavBar,
        Footer
    }
}
</script>
<style scoped></style>