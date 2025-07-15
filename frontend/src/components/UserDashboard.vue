<template>
    <div id="userDashboard" class="container py-4">
        <!-- Welcome Header -->
        <div class="mb-4">
            <h2 class="fw-bold">Welcome back, <span class="fw-bold text-primary text-capitalize">{{ user?.name || 'User' }}</span>!</h2>
            <p class="fs-5">Here's
                an overview of your parking activity:</p>
        </div>
        <!-- Quick Stats -->
        <div class="row g-4 mb-4">
            <div class="col-md-12">
                <div class="card shadow-sm border-0 rounded-4 bg-white">
                    <div class="card-body p-4">
                        <h4 class="card-title fw-bold mb-3 text-black">🔍 Quick Stats</h4>
                        <div class="row row-cols-1 row-cols-md-3 g-3">
                            <div class="col">
                                <div class="card bg-light border-0 h-100">
                                    <div class="card-body text-center">
                                        <div class="fs-2 mb-2">🎫</div>
                                        <div class="fw-bold text-black">Active Bookings</div>
                                        <div class="fs-4 fw-bold text-primary">{{ user?.active_bookings ?? 0 }}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="card bg-light border-0 h-100">
                                    <div class="card-body text-center">
                                        <div class="fs-2 mb-2">⭐</div>
                                        <div class="fw-bold text-black">Average Rating</div>
                                        <div class="fs-4 fw-bold text-primary">{{ user?.average_rating ?? '-' }} / 5
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="card bg-light border-0 h-100">
                                    <div class="card-body text-center">
                                        <div class="fs-2 mb-2">💵</div>
                                        <div class="fw-bold text-black">Total Spend</div>
                                        <div class="fs-4 fw-bold text-primary">₹ {{ user?.amount_spended ?? 0 }}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="card bg-light border-0 h-100">
                                    <div class="card-body text-center">
                                        <div class="fs-2 mb-2">📅</div>
                                        <div class="fw-bold text-black">Total Reservations</div>
                                        <div class="fs-4 fw-bold text-primary">{{ user?.total_bookings ?? 0 }}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="card bg-light border-0 h-100">
                                    <div class="card-body text-center">
                                        <div class="fs-2 mb-2">📝</div>
                                        <div class="fw-bold text-black">Reviews Given</div>
                                        <div class="fs-4 fw-bold text-primary">{{ user?.total_reviews ?? 0 }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Charts Row -->
        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="bg-white rounded-4 p-4 shadow-sm h-100">
                    <UserRevenueChart :dailySpendings="user?.daily_spendings ?? []" />
                </div>
            </div>
            <div class="col-md-6">
                <div class="bg-white rounded-4 p-4 shadow-sm h-100">
                    <UserReservationChart :history="user?.history ?? []" />
                </div>
            </div>
        </div>
        <!-- Donut Charts Row -->
        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="bg-white rounded-4 p-4 shadow-sm h-100">
                    <RevenueBreakdownChart :bookingRevenue="user?.booking_revenue ?? 0"
                        :leaveRevenue="user?.leave_revenue ?? 0" />
                </div>
            </div>

            <!-- Top 3 Parkings -->
            <div class="col-md-6 g-4 mb-4">
                <div class="col-md-12">
                    <div class="bg-white rounded-4 p-4 shadow-sm">
                        <h5 class="fw-bold mb-3 text-black">Top Used Parkings (By Reservations)</h5>
                        <div class="table-responsive">
                            <table class="table table-borderless align-middle mb-0">
                                <thead>
                                    <tr class="text-black">
                                        <th>Parking Name</th>
                                        <th>Reservations</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(parking, idx) in topParkings" :key="parking.id || idx">
                                        <td>{{ parking?.name || '—' }}</td>
                                        <td>{{ parking?.reservation_count ?? '—' }}</td>
                                    </tr>
                                    <tr v-if="topParkings.length < 3">
                                        <td>—</td>
                                        <td>—</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>


            <ParkingCardContainer />

            <!-- Help Section -->
            <div class="row g-4 mb-4">
                <div class="col-md-12">
                    <div class="bg-light rounded-4 p-4 shadow-sm text-center">
                        <h5 class="fw-bold mb-2">🧾 Need Help?</h5>
                        <p>Contact support or visit our <a href="#" class="text-primary fw-bold">Help Center</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
import UserRevenueChart from './analytics/UserRevenueChart.vue';
import UserReservationChart from './analytics/UserReservationChart.vue';
import RevenueBreakdownChart from './analytics/RevenueBreakdownChart.vue';
import SlotUtilizationChart from './analytics/SlotUtilizationChart.vue';
import UserAgeDistChart from './analytics/UserAgeDistChart.vue';
import ParkingCardContainer from './user/ParkingCardContainer.vue';
import Parking from "../pages/Parking.vue";

export default {
    name: "UserDashboard",
    components: {
        UserRevenueChart,
        UserReservationChart,
        RevenueBreakdownChart,
        SlotUtilizationChart,
        UserAgeDistChart,
        ParkingCardContainer,
    },
    computed: {
        ...mapGetters('user', ['user']),
        topParkings() {
            // Top 3 parkings by reservation_count
            const parkings = this.user?.favorite_parking_locations ?? [];
            return parkings.slice(0, 3);
        },
        userAgeDist() {
            // Example: group history by age (if available)
            // Replace with actual age distribution logic if available
            return {};
        }
    },
    methods: {
        ...mapActions('user', ['fetchCurrentUser']),
    },
    created() {
        this.fetchCurrentUser();
    }
}
</script>
<style scoped>
.table th,
.table td {
    color: #000;
}
</style>