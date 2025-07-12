<template>
    <div id="adminDashboard" class="mb-5">
        <div class="container py-4">
            <!-- Welcome Header -->
            <div class="row mb-4">
                <div class="col">
                    <h2 class="fw-bold text-center">Welcome, <span class="text-primary">Admin</span></h2>
                </div>
            </div>

            <!-- KPI Cards -->
            <div class="row g-3 text-center">
                <div class="col-md-3">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <h5 class="card-title text-dark">Active Bookings</h5>
                            <p class="fs-4 fw-semibold text-success mb-0">{{ dashboardAnalyticsData?.active_bookings ?? 0 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <h5 class="card-title text-dark">Total Reservations</h5>
                            <p class="fs-4 fw-semibold text-dark mb-0">{{ dashboardAnalyticsData?.total_reservations ?? 0 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <h5 class="card-title text-dark">Booking Revenue</h5>
                            <p class="fs-4 fw-semibold text-primary mb-0">₹{{ dashboardAnalyticsData?.booking_revenue ?? 0 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <h5 class="card-title text-dark">Total Revenue</h5>
                            <p class="fs-4 fw-semibold text-info mb-0">₹{{ dashboardAnalyticsData?.total_revenue ?? 0 }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Revenue Trend and Average Rating -->
            <div class="row mt-4 g-3">
                <div class="col-md-8">
                    <div class="card shadow rounded-4 h-100 border-0 bg-white">
                        <div class="card-body">
                            <RevenueChart :dailyRevenue="dashboardAnalyticsData?.daily_revenue ?? {}" themeColor="#0d6efd" />
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow rounded-4 h-100 border-0 bg-white">
                        <div class="card-body d-flex flex-column justify-content-center align-items-center">
                            <h5 class="card-title text-dark">Average Rating</h5>
                            <p class="display-6 fw-bold text-warning mb-0">{{ dashboardAnalyticsData?.avg_rating ?? 'N/A' }} ★</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Top Parking and Review Count -->
            <div class="row mt-4 g-3">
                <div class="col-md-8">
                    <div class="card shadow rounded-4 h-100 border-0 bg-white">
                        <div class="card-body">
                            <h5 class="card-title text-dark">Top Parking Locations</h5>
                            <ul class="list-group list-group-flush">
                                <li v-for="p in dashboardAnalyticsData?.top_parkinsg ?? []" :key="p.parking_id"
                                    class="list-group-item d-flex justify-content-between align-items-center bg-white">
                                    <router-link :to="`/parking/${p.parking_id}`"><span class="fw-bold text-primary">{{
                                            p.name }}</span></router-link>
                                    <span class="badge bg-success bg-opacity-75">{{ p.reservation_count }}
                                        bookings</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow rounded-4 h-100 border-0 bg-white">
                        <div class="card-body text-center">
                            <h5 class="card-title text-dark">Total Reviews</h5>
                            <p class="fs-3 fw-semibold text-info mb-0">{{ dashboardAnalyticsData?.total_reviews ?? 0 }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Slot Usage & Spending Breakdown -->
            <div class="row mt-4 g-3">
                <div class="col-md-6">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <SlotUtilizationChart :totalSlots="dashboardAnalyticsData?.total_slots" :bookedSlots="dashboardAnalyticsData?.booked_slots" themeColor="#0d6efd" />
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card shadow rounded-4 border-0 bg-white">
                        <div class="card-body">
                            <RevenueBreakdownChart :bookingRevenue="dashboardAnalyticsData?.booking_revenue"
                                :totalRevenue="dashboardAnalyticsData?.total_revenue" themeColor="#0d6efd" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Stats from './Stats.vue';
import LeafletMap from '../components/LeafletMap.vue';
import RevenueChart from './analytics/RevenueChart.vue';
import UserAgeDistChart from './UserAgeDistChart.vue';
import UserGrowthChart from './UserGrowthChart.vue';
import { mapActions, mapGetters } from 'vuex/dist/vuex.cjs.js';
import RevenueBreakdownChart from './analytics/RevenueBreakdownChart.vue';
import SlotUtilizationChart from './analytics/SlotUtilizationChart.vue';

export default {
    name: "AdminDashboard",
    components: {
        Stats,
        LeafletMap,
        UserAgeDistChart,
        UserGrowthChart,
        RevenueChart,
        RevenueBreakdownChart,
        SlotUtilizationChart
    },
    computed: {
        ...mapGetters('analytics', ['dashboardAnalyticsData'])
    },
    methods: {
        ...mapActions('analytics', ['fetchDBAData'])
    },
    created() {
        this.fetchDBAData();
    }
}
</script>

<style scoped></style>