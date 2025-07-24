<template>
    <div id="sideParkView" class="container-fluid">
        <!-- Location Card -->
        <div class="my-3 bg-white text-dark rounded-4 shadow-sm p-4">
            <p class="mb-2 text-muted">Your Location</p>
            <div class="mb-3">
                <div v-if="addressLoading" class="d-flex justify-content-center align-items-center" style="height: 2.5em;">
                    <div class="spinner-border text-primary" role="status" style="width: 1.5em; height: 1.5em;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <address v-else class="fs-5 text-dark small mb-0">{{ address }}</address>
            </div>
            <button class="btn btn-primary w-100 rounded-pill mt-2">Explore More</button>
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
            address: "Unable to load address at the moment",
            inDist: 15,
            inTime: 20,
            addressLoading: false,
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
                this.addressLoading = true;
                const baseUrl = import.meta.env.VITE_BASE_URL;
                const response = await fetch(`${baseUrl}/api_v1/analytics/reverse_geocode?lat=${lat}&lon=${long}`);
                const data = await response.json();
                this.address = data.address;
            } catch (err) {
                console.error(err)
            } finally {
                this.addressLoading = false;
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

</style>