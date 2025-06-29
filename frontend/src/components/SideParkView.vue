<template>
    <div id="sideParkView">
        <div class="my-3  bg-primary text-light rounded-4 p-4">
            <h4>
                {{ place }}
            </h4>
            <address class=" text-light">
                {{ address }}
            </address>
            <button class="btn btn-light w-100 rounded-pill">Explore More</button>
        </div>

        <div class=" border border-2 rounded-4">
            <div class="border-bottom border-2 p-4 rounded-4">
                <small class="text-muted">Nearby</small>
                <div class=" d-flex justify-content-between align-items-start">
                    <h4>
                        Parking Lots
                    </h4>
                    <h4 class=" text-primary">
                        <i class="bi bi-p-circle-fill"></i>
                    </h4>
                </div>
                <div class=" col-md">
                    <div class="p-1 row">
                        <div class="col">
                            <div class=" bg-success rounded-circle" style="height: 15px; width: 15px;">
                            </div>
                            <div class="text-muted mt-2">
                                Available
                            </div>


                        </div>
                        <div class="col">
                            <div class=" bg-primary rounded-circle" style="height: 15px; width: 15px;">
                            </div>
                            <div class="text-muted mt-2">
                                Pick Ready
                            </div>
                        </div>
                    </div>
                    <div class="row p-1">
                        <div class="col">
                            <div class="mt-4">
                                <small class="text-muted">Nearby (in Km)</small>
                                <div class="">
                                    <button @click="inDist--" style="font-size: 24px;"
                                        class="btn p-0 me-1 text-primary"><i
                                            class="bi bi-dash-circle-fill"></i></button>
                                    <input v-model="inDist" type="number" style="width: 40px;"
                                        class=" text-center border-0 border-bottom border-dark text-decoration-none ">
                                    <button @click="inDist++" style="font-size: 24px;"
                                        class="btn p-0 ms-1 text-primary"><i
                                            class="bi bi-plus-circle-fill"></i></button>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="mt-4 ">
                                <small class="text-muted">Nearby (in Min)</small>
                                <div class="">
                                    <button @click="inTime--" style="font-size: 24px;"
                                        class="btn p-0 me-1 text-primary"><i
                                            class="bi bi-dash-circle-fill"></i></button>
                                    <input v-model="inTime" type="number" style="width: 40px;"
                                        class=" text-center border-0 border-bottom border-dark text-decoration-none ">
                                    <button @click="inTime++" style="font-size: 24px;"
                                        class="btn p-0 ms-1 text-primary"><i
                                            class="bi bi-plus-circle-fill"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg overflow-auto" style="height: 360px;">
                <ParkingCard v-for="parking in parkings" :key="parking.id" :parking="parking" />
            </div>

        </div>
    </div>
</template>
<script>
import ParkingCard from './ParkingCard.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
    name: "SideParkView",
    data() {
        return {
            place: "A unknown Place",
            address: "ABC, dummy city, state, country, 00000",
            loc: {
                lat: 0.00000000,
                long: 0.00000000,
            },
            inDist: 15,
            inTime: 20,
        }
    },

    computed: {
        ...mapGetters("parking", ['page', 'total', 'parkings'])
    },

    methods: {
        ...mapActions("parking", ['fetchParkings'])
    },
    
    mounted() {
        this.fetchParkings();
    }, 

    components: {
        ParkingCard,
    }

}
</script>
<style scoped></style>