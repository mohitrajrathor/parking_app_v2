<template>
    <div id="sideParkView" class="container-fluid">
        <!-- Location Card -->
        <div class="my-3 bg-white text-dark rounded-4 shadow-sm p-4">
            <p class="mb-2 text-muted">Your Location</p>
            <address class="mb-3 fs-5 text-dark small">{{ address }}</address>
            <button class="btn btn-primary w-100 rounded-pill">Explore More</button>
        </div>

        <!-- Parking Info Card -->
        <div class="bg-white border border-2 rounded-4 shadow-sm mb-3">
            <div class="border-bottom border-2 p-4 rounded-top-4">
                <small class="text-muted">Nearby</small>
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h4 class="fw-bold mb-0">Parking Lots</h4>
                    <span class="fs-3 text-primary"><i class="bi bi-p-circle-fill"></i></span>
                </div>
                <div class="row mb-3">
                    <div class="col text-center">
                        <div class="bg-success rounded-circle mx-auto" style="height: 15px; width: 15px;"></div>
                        <div class="text-muted mt-2 small">Available</div>
                    </div>
                    <div class="col text-center">
                        <div class="bg-primary rounded-circle mx-auto" style="height: 15px; width: 15px;"></div>
                        <div class="text-muted mt-2 small">Pick Ready</div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col">
                        <div class="mt-2">
                            <small class="text-muted">Nearby (in Km)</small>
                            <div class="d-flex align-items-center justify-content-center gap-2 mt-1">
                                <button @click="inDist = Math.max(0, inDist-1)" class="btn btn-outline-primary btn-sm rounded-circle"><i class="bi bi-dash-circle-fill"></i></button>
                                <input v-model="inDist" type="number" min="0" style="width: 40px;" class="form-control text-center border-0 border-bottom border-primary p-0" />
                                <button @click="inDist++" class="btn btn-outline-primary btn-sm rounded-circle"><i class="bi bi-plus-circle-fill"></i></button>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="mt-2">
                            <small class="text-muted">Nearby (in Min)</small>
                            <div class="d-flex align-items-center justify-content-center gap-2 mt-1">
                                <button @click="inTime = Math.max(0, inTime-1)" class="btn btn-outline-primary btn-sm rounded-circle"><i class="bi bi-dash-circle-fill"></i></button>
                                <input v-model="inTime" type="number" min="0" style="width: 40px;" class="form-control text-center border-0 border-bottom border-primary p-0" />
                                <button @click="inTime++" class="btn btn-outline-primary btn-sm rounded-circle"><i class="bi bi-plus-circle-fill"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="overflow-auto px-3 pb-3" style="max-height: 360px;">
                <ParkingCard v-for="parking in parkings" :key="parking.id"
                    :id="parking.id"
                    :name="parking.name"
                    :bookingFee="parking.booking_fee"
                    :hourlyFee="parking.hourly_fee"
                    :availableSlots="parking.slots_num - (parking.booked || 0)"
                    @view="handleViewParking" />
            </div>
        </div>
    </div>
</template>
<script>
import ParkingCard from './user/ParkingCard.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
    name: "SideParkView",
    data() {
        return {
            address: "ABC, Dummy City, State, Country, 00000",
            inDist: 15,
            inTime: 20,
        }
    },
    computed: {
        ...mapGetters(['position']),
        ...mapGetters("parking", ['page', 'total', 'parkings']),
    },
    methods: {
        ...mapActions("parking", ['fetchParkings']),
        handleViewParking(id) {
            this.$router.push(`/parking/${id}`)
        },

        async getAddressFromCoordinates(lat, long) {
            // Use backend proxy to avoid CORS
            try {
                const response = await fetch(`http://localhost:1234/api_v1/analytics/reverse_geocode?lat=${lat}&lon=${long}`);
                const data = await response.json();
                if (data && data.address) {
                    this.address = data.address;
                } else {
                    this.address = "Unknown address";
                }
            } catch (err) {
                this.address = "Unknown address";
            }
        }
    },
    watch: {
        position: {
            handler(newVal) {
                if (newVal && newVal.lat && newVal.long) {
                    this.getAddressFromCoordinates(newVal.lat, newVal.long);
                }
            },
            immediate: true,
            deep: true
        }
    },
    created() {
        this.fetchParkings();
    },
    components: {
        ParkingCard,
    }
}
</script>
<style scoped>
#sideParkView .card, #sideParkView .bg-white {
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.rounded-4 {
    border-radius: 1.25rem !important;
}
.rounded-top-4 {
    border-top-left-radius: 1.25rem !important;
    border-top-right-radius: 1.25rem !important;
}
.form-control:focus {
    box-shadow: none;
    border-color: #0d6efd;
}
</style>