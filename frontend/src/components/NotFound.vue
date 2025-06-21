<template>
    <NavBar/>
    <div id="notFound">
        <div class="vh-100 d-flex justify-content-center align-items-center">
            <h1>
                Page Not Found
            </h1>
        </div>
    </div>
    <Footer></Footer>
</template>
<script>
import NavBar from "./NavBar.vue";
import Footer from "./Footer.vue";


export default {
    name: "NotFound", 
    components: {
        NavBar,
        Footer
    }
}
</script>
<style scoped>
    
</style>