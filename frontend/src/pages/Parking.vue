<template>
    <NavBar />

    <div id="parking" class="container py-4">
        <!-- Loading Spinner -->
        <div v-if="isLoading" class="d-flex justify-content-center align-items-center min-vh-50">
            <div class="text-center">
                <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="fw-bold text-primary">Loading parking details...</div>
            </div>
        </div>

        <!-- if no parking found -->
        <div v-else-if="!parking" class="d-flex justify-content-center min-vh-50 align-items-center">
            <div>
                <h3>Parking not found with ID: <strong>{{ parking_id }}</strong></h3>
            </div>
        </div>

        <!-- layout only if parking is available -->
        <div v-else>
            <div class="row g-4">
                <div class="col-12 col-lg-8">
                    <div class="bg-white rounded-4 p-4 mb-4">
                        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
                            <h1 class="display-6 fw-bold text-capitalize text-dark mb-0">{{ parking.name }}</h1>
                            <div class="d-flex flex-wrap gap-2 justify-content-center">
                                <div class="px-3 py-1 bg-primary-subtle rounded">
                                    <span class="fs-4 fw-bold text-primary">₹ {{ parking.booking_fee }}</span>
                                    <small class="text-muted">Fixed</small>
                                </div>
                                <div class="px-3 py-1 bg-success-subtle rounded">
                                    <span class="fs-4 fw-bold text-success">₹ {{ parking.hourly_fee }}</span>
                                    <small class="text-muted">/hour</small>
                                </div>
                            </div>
                        </div>
                        <div class="my-3">
                            <address class="text-center text-capitalize fw-semibold mb-0">
                                <i class="bi bi-geo-alt-fill me-2"></i>{{ parking.address }}<br>
                                <i class="bi bi-telephone me-2"></i>Contact: {{ parking.phone }}
                                <span class="mx-2">|</span>
                                <i class="bi bi-123 me-2"></i>Pincode: {{ parking.pincode }}
                            </address>
                        </div>
                        <div class="row g-3 justify-content-center mb-3">
                            <div class="col-6 col-md-4">
                                <div class="p-3 fs-5 bg-primary-subtle text-primary rounded-3 text-center">
                                    Total Slots <br><strong>{{ parking.slots_num }}</strong>
                                </div>
                            </div>
                            <div class="col-6 col-md-4">
                                <div class="p-3 fs-5 bg-success-subtle text-success rounded-3 text-center">
                                    Available <br><strong>{{ parking.slots_num - parking.booked }}</strong>
                                </div>
                            </div>
                            <div class="col-12 col-md-4">
                                <div class="p-3 fs-5 bg-warning-subtle rounded-3 text-center">
                                    Reviews <br><strong>{{ parking.reviews ? parking.reviews.length : 0 }}</strong>
                                </div>
                            </div>
                        </div>
                        <div class="row" v-if="role === 'user'">
                            <div class="col">
                                <button @click="goToPayment(parking.id)" class="btn btn-dark bg-gradient w-100 py-2 fs-5 rounded-pill">
                                    <i class="bi bi-credit-card me-2"></i>Book Parking
                                </button>
                            </div>
                        </div>
                        <div v-else class="alert alert-dark fw-bold text-center mt-3" role="alert">
                            You need to login to book parking !
                        </div>
                    </div>
                </div>
                <div class="col-12 col-lg-4">
                    <div class="bg-white rounded-4 h-100">
                        <LeafletMap :parkingToShow="{ name: parking.name, lat: parking.lat, long: parking.long }" />
                    </div>
                </div>
            </div>
            <div id="parkingTabs" class="mt-4">
                <div class="d-flex gap-2 justify-content-center mb-3 flex-wrap">
                    <button @click="switchTab('slots')"
                        :class="[currentTab === 'slots' ? 'btn btn-primary' : 'btn btn-outline-primary', 'rounded-pill px-4']">Slots</button>
                    <button @click="switchTab('reviews')"
                        :class="[currentTab === 'reviews' ? 'btn btn-primary' : 'btn btn-outline-primary', 'rounded-pill px-4']">Reviews</button>
                    <button @click="switchTab('statistics')"
                        :class="[currentTab === 'statistics' ? 'btn btn-primary' : 'btn btn-outline-primary', 'rounded-pill px-4']">Statistics</button>
                </div>
                <hr>
                <div id="tab" class="p-4 bg-white rounded-4">
                    <div v-if="currentTab === 'slots'" class="row row-cols-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 g-3">
                        <div v-for="slot in parking.slots" :key="slot.id" class="col">
                            <div
                                :class="['p-2 fw-bold text-center rounded border', slot.is_occupied ? 'bg-danger-subtle text-danger border-danger' : 'bg-success-subtle text-success border-success']">
                                {{ slot.serial_id }}
                            </div>
                        </div>
                        <div v-if="parking.slots.length === 0" class="col-12">
                            <div class="p-2 fw-bold text-center rounded border border-success">
                                No slots available
                            </div>
                        </div>
                    </div>
                    <div v-if="currentTab === 'reviews'">
                        <div v-if="parking.reviews && parking.reviews.length > 0">
                            <div v-for="review in parking.reviews" :key="review.id" class="mb-3">
                                <div class="card h-100 border-0">
                                    <div class="card-body">
                                        <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start mb-2 gap-2">
                                            <h6 class="card-subtitle mb-1 text-muted">
                                                {{ review.user.name || 'Anonymous' }}
                                            </h6>
                                            <small class="text-muted text-sm-end">
                                                {{review.create_at
                                                    ? new Date(
                                                        review.create_at.replace(
                                                            /(\d{2})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(\d{2})/,
                                                            (m, d, mth, y, h, min, s) => `20${y}-${mth}-${d}T${h}:${min}:${s}`
                                                        )
                                                    ).toLocaleString()
                                                    : ''
                                                }}
                                            </small>
                                        </div>
                                        <p class="card-text">{{ review.feedback }}</p>
                                        <div class="d-flex flex-column flex-sm-row align-items-start align-items-sm-center">
                                            <div class="me-0 me-sm-2 mb-1 mb-sm-0">
                                                <span v-for="i in 5" :key="i" :class="[
                                                    'star',
                                                    i <= (review.rating || 5) ? 'text-warning' : 'text-secondary'
                                                ]" style="font-size: 1.2rem;">★</span>
                                            </div>
                                            <small class="text-muted">{{ review.rating || 5 }}/5</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="text-center py-4">
                            <div class="text-muted">
                                <i class="bi bi-chat-dots fs-1"></i>
                                <p class="mt-2">No reviews yet</p>
                                <small>Be the first to leave a review!</small>
                            </div>
                        </div>
                    </div>
                    <div v-if="currentTab === 'statistics'">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <div class="card border-0">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">Occupancy Rate</h5>
                                        <div class="display-4 text-primary">
                                            {{ parking.slots_num > 0 ? Math.round((parking.booked / parking.slots_num) * 100) : 0 }}%
                                        </div>
                                        <p class="card-text">{{ parking.booked }} of {{ parking.slots_num }} slots occupied</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <div class="card border-0">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">Average Rating</h5>
                                        <div class="display-4 text-warning">
                                            {{parking.reviews && parking.reviews.length > 0 ?
                                                (parking.reviews.reduce((sum, review) => sum + (review.rating || 5), 0) /
                                                    parking.reviews.length).toFixed(1) : 'N/A'}}
                                        </div>
                                        <p class="card-text">Based on {{ parking.reviews ? parking.reviews.length : 0 }} reviews</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Footer />
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import LeafletMap from '../components/LeafletMap.vue';
import { mapGetters, mapActions } from 'vuex';
import parking from '../store/parking';

export default {
    name: "Parking",
    components: {
        NavBar,
        Footer,
        LeafletMap
    },
    data() {
        return {
            currentTab: "slots",
            isLoading: true,
        }
    },
    computed: {
        ...mapGetters("parking", ["parking"]),
        ...mapGetters(['role', 'isAuthenticated']),
        parking_id() {
            return this.$route.params.id;
        }
    },
    methods: {
        ...mapActions("parking", ["fetchParkingById"]),
        switchTab(tab) {
            this.currentTab = tab;
        },
        goToPayment(parking_id) {
            this.$router.push({ path: `/payment/booking`, query: { parking_id: parking_id } });
        },
    },
    async created() {
        this.isLoading = true;
        await this.fetchParkingById(this.parking_id);
        this.isLoading = false;
    }
};
</script>

<style>
.vh-50 {
    min-height: 50vh;
}
.min-vh-50 {
    min-height: 50vh;
}
.bg-primary-subtle {
    background-color: #e7f1ff !important;
}
.bg-success-subtle {
    background-color: #e6f4ea !important;
}
.bg-warning-subtle {
    background-color: #fff8e1 !important;
}
.bg-danger-subtle {
    background-color: #fbeaea !important;
}
</style>
