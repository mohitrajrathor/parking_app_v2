<template>
    <NavBar />
    
    <div v-if="user" class="container">
        <div class="custom-padding">
            <div v-if="!isLoading" id="userProfile" class="">
                <div class="row g-4 flex-column-reverse flex-md-row">
                    <!-- left -->
                    <div class="col-12 col-md-8">
                        <div class="card shadow-sm rounded-4 border-0 mb-4">
                            <div class="card-body p-4">
                                <div
                                    class="d-flex flex-column flex-sm-row align-items-center gap-3 text-center text-sm-start">
                                    <UserLogo :name="user?.name" :size="72" class="mx-auto mx-sm-0" />
                                    <div class="ms-0 ms-sm-3 flex-grow-1 w-100">
                                        <h1 class="mb-1 display-6 text-capitalize fw-bold">{{ user?.name }}</h1>
                                        <div
                                            class="d-flex flex-wrap justify-content-center justify-content-sm-start align-items-center gap-2 mb-2">
                                            <span class="badge bg-primary bg-opacity-75 fs-6">
                                                <i class="bi bi-person-badge me-1"></i> {{ user?.profession || 'N/A' }}
                                            </span>
                                            <span class="badge bg-secondary bg-opacity-75 fs-6">
                                                <i class="bi bi-calendar-event me-1"></i> Joined: {{
                                                    formatDate(user?.join_time) }}
                                            </span>
                                            <span class="badge bg-info bg-opacity-75 fs-6">
                                                <i class="bi bi-hash me-1"></i> ID: {{ user?.unique_id }}
                                            </span>
                                            <span class="badge"
                                                :class="user?.email_confirmed ? 'bg-success' : 'bg-danger'">
                                                <i class="bi bi-envelope-check me-1"></i>
                                                {{ user?.email_confirmed ? 'Email Verified' : 'Email Not Verified' }}
                                            </span>
                                        </div>
                                        <p class="mb-0">
                                            <a class="fw-bold text-decoration-none text-dark"
                                                :href="`mailto:${user?.email}`">
                                                <i class="bi bi-envelope-at me-1"></i>{{ user?.email }}
                                            </a>
                                        </p>
                                    </div>
                                </div>
                                <hr class="my-4">
                                <div id="userContact" class="row text-center text-md-start">
                                    <div class="col-12 col-md-6 mb-2 mb-md-0">
                                        <div class="fw-bold text-capitalize">
                                            <i class="bi bi-geo-alt me-2"></i>{{ user?.address }}
                                        </div>
                                    </div>
                                    <div class="col-12 col-md-6">
                                        <div class="fw-bold">
                                            <i class="bi bi-telephone me-2"></i>{{ user?.phone }}
                                            <span class="mx-2 d-none d-md-inline">|</span>
                                            <br class="d-md-none" />
                                            <i class="bi bi-123 me-2"></i>Pincode: {{ user?.pincode }}
                                        </div>
                                        <div class="fw-bold mt-1">
                                            <i class="bi bi-cake2 me-2"></i>DOB: {{ formatDate(user?.dob) }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card shadow-sm rounded-4 h-100 border-0">
                            <div class="card-body p-4 text-center">
                                <h5 class="mb-4 fw-bold text-primary">Your Stats</h5>
                                <div class="row g-3">
                                    <div class="col-6">
                                        <div class="card bg-success bg-opacity-10 border-0 rounded-3">
                                            <div class="card-body py-3 px-2">
                                                <div class="fs-3 fw-bold text-success mb-1">{{ user?.total_bookings ?? 0
                                                    }}</div>
                                                <div class="small text-muted">Total Bookings</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="card bg-info bg-opacity-10 border-0 rounded-3">
                                            <div class="card-body py-3 px-2">
                                                <div class="fs-3 fw-bold text-info mb-1">{{ user?.active_bookings ?? 0
                                                    }}</div>
                                                <div class="small text-muted">Active Bookings</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="card bg-warning bg-opacity-10 border-0 rounded-3">
                                            <div class="card-body py-3 px-2">
                                                <div class="fs-3 fw-bold text-warning mb-1">₹{{ user?.amount_spended ??
                                                    0 }}</div>
                                                <div class="small text-muted">Total Spent</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="card bg-secondary bg-opacity-10 border-0 rounded-3">
                                            <div class="card-body py-3 px-2">
                                                <div class="fs-3 fw-bold text-secondary mb-1">{{ user?.average_rating ?
                                                    user.average_rating.toFixed(1) : 'N/A' }}</div>
                                                <div class="small text-muted">Average Rating</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


                <div id="tabs" class="d-flex justify-content-center align-items-center mb-3 mt-4">
                    <div class="btn-group bg-light" role="group" aria-label="Profile Tabs">
                        <button v-for="t in tabs" :key="t" @click="switchTab(t)" type="button"
                            :class="['btn', 'btn-lg', activeTab === t ? 'btn-primary' : 'btn-outline-primary', 'text-capitalize']">
                            <i v-if="t === 'booking'" class="bi bi-calendar2-check me-1"></i>
                            <i v-else-if="t === 'history'" class="bi bi-clock-history me-1"></i>
                            <i v-else-if="t === 'statistics'" class="bi bi-bar-chart-line me-1"></i>
                            {{ t }}
                        </button>
                    </div>
                </div>

                <div v-if="activeTab === 'booking'" id="bookingTab">
                    <div v-if="user && user.bookings && user.bookings.length > 0">
                        <div v-for="booking in user.bookings" :key="booking.id" class="mb-3">
                            <div class="card border-0 rounded-4 position-relative overflow-hidden">
                                <div class="card-body p-4">
                                    <div
                                        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3 gap-2">
                                        <div>
                                            <span class="fw-bold text-primary fs-5">{{ booking.parking?.name }}</span>
                                            <span class="badge bg-success bg-opacity-75 ms-2">Active</span>
                                        </div>
                                        <div class="text-muted small">Start: {{ formatDate(booking.start_time) }}</div>
                                    </div>
                                    <div class="mb-2">
                                        <span
                                            class="p-2 rounded-3 bg-dark-subtle bg-opacity-25 text-dark fw-semibold me-2">Slot:
                                            {{ booking.slot?.serial_id }}</span>
                                    </div>
                                    <div class="mb-3">
                                        <span class="fw-bold">Payments:</span>
                                        <div class="table-responsive mt-2">
                                            <table class="table table-bordered table-sm align-middle mb-0">
                                                <thead class="table-light">
                                                    <tr>
                                                        <th>Type</th>
                                                        <th>Amount</th>
                                                        <th>Paid At</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="charge in booking.charges" :key="charge.id">
                                                        <td class="fw-bold text-capitalize">{{ charge.pay_for }}</td>
                                                        <td class="fw-bold text-success">₹{{ charge.amount }}</td>
                                                        <td class="text-muted small">{{ formatDate(charge.paid_at) }}
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                    <div class="mb-2">
                                        <span class="fw-bold">Parking Time:</span>
                                        <span class="text-dark fw-bold ms-3">Ongoing</span>
                                    </div>
                                    <div v-if="booking.review" class="mb-2">
                                        <span class="fw-bold">Your Review:</span> {{ booking.review.feedback }}
                                        <span class="ms-2 text-warning">({{ booking.review.rating }}/5)</span>
                                    </div>
                                    <div v-else class="text-muted small">No review yet</div>
                                    <div v-if="$store.getters.role === 'user'" class="mt-3 text-end">
                                        <button @click="leaveParkingRedirect(booking?.id, booking?.parking?.id)"
                                            class="btn btn-danger btn-sm rounded-pill px-4">Leave</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-center text-muted py-4">
                        <i class="bi bi-calendar2-x fs-1"></i>
                        <p>No active bookings found.</p>
                    </div>
                </div>
                <div v-if="activeTab === 'history'" id="historyTab">
                    <div v-if="user && user.history && user.history.length > 0">
                        <div v-for="history in user.history" :key="history.id" class="mb-3">
                            <div class="card border-0 rounded-4 bg-light-subtle">
                                <div class="card-body p-4">
                                    <div
                                        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3 gap-2">
                                        <div>
                                            <span class="fw-bold text-primary fs-5">{{ history.parking?.name }}</span>
                                            <span class="badge bg-secondary bg-opacity-75 ms-2">Past</span>
                                        </div>
                                        <div class="text-muted small">Start: {{ formatDate(history.start_time) }}<span
                                                v-if="history.leave_time"> | End: {{ formatDate(history.leave_time)
                                                }}</span></div>
                                    </div>
                                    <div class="mb-2">
                                        <span
                                            class="p-2 rounded-3 bg-dark-subtle bg-opacity-25 text-dark fw-semibold me-2">Slot:
                                            {{ history.slot?.serial_id }}</span>

                                    </div>
                                    <div class="mb-3">
                                        <span class="fw-bold">Charges:</span>
                                        <div class="table-responsive mt-2">
                                            <table class="table table-bordered table-sm align-middle mb-0">
                                                <thead class="table-light">
                                                    <tr>
                                                        <th>Type</th>
                                                        <th>Amount</th>
                                                        <th>Paid At</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="charge in history.charges" :key="charge.id">
                                                        <td class="fw-bold text-capitalize">{{ charge.pay_for }}</td>
                                                        <td class="fw-bold text-success">₹{{ charge.amount }}</td>
                                                        <td class="text-muted small">{{ formatDate(charge.paid_at) }}
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                    <div class="mb-2">
                                        <span class="fw-bold">Hours Used:</span>
                                        <span class=" text-dark fw-bold ms-3">{{ getParkingHours(history.start_time,
                                            history.leave_time) }} Hours</span>
                                    </div>
                                    <div v-if="history.review" class="mb-2">
                                        <span class="fw-bold">Your Review:</span> {{ history.review.feedback }}
                                        <span class="ms-2 text-warning">({{ history.review.rating }}/5)</span>
                                    </div>
                                    <div v-else class="text-muted small">No review for this booking</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-center text-muted py-4">
                        <i class="bi bi-clock-history fs-1"></i>
                        <p>No booking history found.</p>
                    </div>
                </div>
                <div v-if="activeTab === 'statistics'" id="statisticsTab">
                    <div class="card border-0 rounded-4 bg-light-subtle p-4">
                        <h5 class="fw-bold text-primary mb-3">Booking & Payment Statistics</h5>
                        <div class="row g-3 align-items-end">
                            <div class="col-6 col-md-3">
                                <div class="text-center">
                                    <div class="fs-2 fw-bold text-success">{{ user?.total_bookings ?? 0 }}</div>
                                    <div class="small text-muted">Total Bookings</div>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-success" role="progressbar"
                                            :style="{ width: (user?.total_bookings ? Math.min(user.total_bookings * 20, 100) : 0) + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6 col-md-3">
                                <div class="text-center">
                                    <div class="fs-2 fw-bold text-info">{{ user?.active_bookings ?? 0 }}</div>
                                    <div class="small text-muted">Active Bookings</div>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-info" role="progressbar"
                                            :style="{ width: (user?.active_bookings ? Math.min(user.active_bookings * 20, 100) : 0) + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6 col-md-3">
                                <div class="text-center">
                                    <div class="fs-2 fw-bold text-warning">₹{{ user?.amount_spended ?? 0 }}</div>
                                    <div class="small text-muted">Total Spent</div>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-warning" role="progressbar"
                                            :style="{ width: (user?.amount_spended ? Math.min(user.amount_spended, 100) : 0) + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6 col-md-3">
                                <div class="text-center">
                                    <div class="fs-2 fw-bold text-secondary">{{ user?.average_rating ?
                                        user.average_rating.toFixed(1) : 'N/A' }}</div>
                                    <div class="small text-muted">Average Rating</div>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-secondary" role="progressbar"
                                            :style="{ width: (user?.average_rating ? user.average_rating * 20 : 0) + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Loading Profile data...</p>
            </div>
        </div>
    </div>

    <div v-else class="vh-50 d-flex align-items-center justify-content-center">
        <div class=" text-center">
            
            <h3 v-if="errorMessage">{{ errorMessage }}</h3>
            <h3 v-else>No User Found with id {{ user_id }}</h3>

            <button class=" btn btn-dark" @click="$router.go(-1)">Back</button>
        </div>
    </div>

    <Footer />
</template>
<script>
import { mapGetters, mapActions } from "vuex";
import user from "../store/user";
import UserLogo from "../components/user/UserLogo.vue";
import NavBar from "../components/NavBar.vue";
import Footer from "../components/Footer.vue";


export default {
    name: "UserProfile",
    data() {
        return {
            isLoading: false,
            activeTab: "booking",
            tabs: [
                "booking",
                "history",
                "statistics",
            ],
            errorMessage: "",
        }
    },
    components: {
        UserLogo,
        NavBar,
        Footer
    },
    computed: {
        ...mapGetters("user", ['user']),
        user_id() {
            return this.$route.query.user_id || null;
        }
    },
    methods: {
        ...mapActions("user", ['fetchUserById', 'fetchCurrentUser']),
        formatDate(givenDate) {
            if (!givenDate) return 'N/A';
            let dateObj = new Date(givenDate);
            if (isNaN(dateObj.getTime())) {
                // Try to parse custom format: dd-mm-yyTHH:MMSS
                // Convert to yyyy-mm-ddTHH:MM:SS
                const match = givenDate.match(/(\d{2})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(\d{2})/);
                if (match) {
                    // match: [full, dd, mm, yy, HH, MM, SS]
                    const iso = `20${match[3]}-${match[2]}-${match[1]}T${match[4]}:${match[5]}:${match[6]}`;
                    dateObj = new Date(iso);
                } else {
                    dateObj = new Date(givenDate.replace(/-/g, '/').replace('T', ' ').slice(0, 19));
                }
            }
            if (isNaN(dateObj.getTime())) return givenDate;
            // Show date and time
            return dateObj.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            });
        },
        getParkingHours(start, end) {
            if (!start || !end) return 'N/A';
            // Parse both dates using the same logic as formatDate
            function parseDate(str) {
                let d = new Date(str);
                if (isNaN(d.getTime())) {
                    const match = str.match(/(\d{2})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(\d{2})/);
                    if (match) {
                        const iso = `20${match[3]}-${match[2]}-${match[1]}T${match[4]}:${match[5]}:${match[6]}`;
                        d = new Date(iso);
                    } else {
                        d = new Date(str.replace(/-/g, '/').replace('T', ' ').slice(0, 19));
                    }
                }
                return d;
            }
            const startDate = parseDate(start);
            const endDate = parseDate(end);
            if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) return 'N/A';
            const diffMs = endDate - startDate;
            const hours = diffMs / (1000 * 60 * 60);
            return hours < 1 ? '<1' : hours.toFixed(1);
        },
        switchTab(tab) {
            this.activeTab = tab;
        },

        leaveParkingRedirect(booking_id, parking_id) {
            this.$router.push({ path: `/payment/leave_parking`, query: { parking_id: parking_id, booking_id: booking_id } });
        },

    },
    filters: {
        capitalize(value) {
            if (!value) return '';
            return value.charAt(0).toUpperCase() + value.slice(1);
        }
    },
    mounted() {
        this.isLoading = true;
        console.log(this.user);
        if (this.$store.getters.role === 'user') this.fetchCurrentUser();
        if (this.$store.getters.role === 'admin' && this.user_id) this.fetchUserById(this.user_id);
        this.errorMessage = "You are not Authorized to view profile !"
        this.isLoading = false;
    }
}
</script>
<style scoped>
.custom-padding {
    padding-bottom: 100px;
}
</style>