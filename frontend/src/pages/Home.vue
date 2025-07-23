<template>
    <div id="home">
        <NavBar />

        <div class=" container-xxl ">
            <!-- layout -->
            <div class="row p-2 rounded-4 m-1">
                <div class=" col-lg-9 p-0">
                    <div class="p-2">

                        <!-- upper div -->
                        <div class="row">
                            <div class=" col-lg-4">
                                <p class="m-0 text-center fs-5 text-muted fw-bold kaushan"><span class="text-primary"><i
                                            class="bi bi-check-circle-fill"></i></span> Quick, Relieble & Hassele free
                                </p>
                                <div class="p-2 light-gray rounded-3">
                                    <h1 class="brand-font fw-bold text-center">Parkly</h1>
                                </div>

                                <div class="row p-2">
                                    <div class="col bg-primary p-2 m-1 rounded-3 text-light fw-bold">
                                        <div class="text-center">
                                            <small class=" text-center" style="font-size: 12px;"><i
                                                    class="bi bi-person-fill"></i> User</small>
                                            <br>
                                            <strong>800k+</strong>
                                        </div>
                                    </div>
                                    <div class="col lime-green p-2 m-1 rounded-3 text-dark fw-bold">
                                        <div class="text-center">
                                            <small style="font-size: 12px;"><i class="bi bi-p-circle"></i>
                                                Parking</small>
                                            <br>
                                            <strong>3K+</strong>
                                        </div>
                                    </div>
                                    <div class="col light-gray p-2 m-1 rounded-3 text-dark fw-bold">
                                        <div class="text-center">
                                            <small style="font-size: 12px;"><i class="bi bi-car-front-fill"></i>
                                                Lots</small>
                                            <br>
                                            <strong>150K+</strong>
                                        </div>
                                    </div>
                                </div>

                                <div class="p-1">
                                    <h1 class="brand-font">
                                        Urban parking made easy
                                    </h1>
                                </div>


                                <Feedback />


                            </div>

                            <!-- map section -->
                            <div class=" col-lg-8">
                                <LeafletMap />
                            </div>
                        </div>
                    </div>

                    <!-- perks section -->
                    <Perks />
                </div>

                <div class=" col-lg-3 p-2">
                    <SideParkView />
                </div>
            </div>
        </div>

        <Footer></Footer>
    </div>
</template>
<script>
import Feedback from '../components/Feedback.vue';
import LeafletMap from '../components/LeafletMap.vue';
import NavBar from '../components/NavBar.vue';
import Perks from '../components/Perks.vue';
import SideParkView from '../components/SideParkView.vue';
import Footer from '../components/Footer.vue';

export default {
    name: "Home",
    components: {
        NavBar,
        Feedback,
        Perks,
        LeafletMap,
        SideParkView,
        Footer,
    }, 
}
</script>
<style></style>