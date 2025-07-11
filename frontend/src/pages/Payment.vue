<template>
  <div class="container py-4">
    <div v-if="status === 'form'">
      <div v-if="parking" class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-6">
          <!-- Credit Card Design -->
          <div class="card bg-primary text-white mb-4 shadow-lg rounded-4 border-0 position-relative overflow-hidden">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="fw-bold fs-5">{{ parking.name }}</span>
                <i class="bi bi-credit-card-2-front-fill fs-2 text-white-50"></i>
              </div>
              <div class="fs-4 mb-2">
                •••• •••• •••• {{ (parking.id + '0000').slice(-4) }}
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-white-50 small">Card Holder</div>
                  <div class="fw-semibold">{{ user ? user.name : 'User' }}</div>
                </div>
                <div>
                  <div class="text-white-50 small">Valid Thru</div>
                  <div>12/29</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Fee Breakdown Card -->
          <div class="card shadow rounded-4 mb-4 border-0">
            <div class="card-body">
              <h4 class="card-title mb-3 text-primary">Fee Breakdown</h4>
              <ul class="list-group list-group-flush mb-3">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Parking Name</span>
                  <span class="fw-bold">{{ parking.name }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Booking Fee</span>
                  <span>₹{{ parking.booking_fee }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Hourly Fee</span>
                  <span>₹{{ parking.hourly_fee }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Payment For</span>
                  <span class="fw-bold text-capitalize">{{ paymentFor === 'booking' ? "Booking" : "Leave Parking" }}</span>
                </li>
                <hr>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Hour used</span>
                  <span>{{ hourUsed }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span class="fw-bold">Total Amount</span>
                  <span class="fw-bold text-capitalize">{{ totalAmount }}</span>
                </li>
              </ul>
              <div v-if="paymentFor==='leave_parking'" class="d-grid gap-3 mb-3">
                <div>
                  <label for="feedback" class="form-label fw-semibold text-primary">Feedback</label>
                  <textarea id="feedback" class="form-control rounded-3 bg-primary-subtle border-0 shadow-sm" rows="2" v-model="feedback" placeholder="Share your experience..."></textarea>
                </div>
                <div>
                  <label for="rating" class="form-label fw-semibold text-primary">Rating</label>
                  <select id="rating" class="form-select rounded-3 bg-primary-subtle border-0 shadow-sm" v-model="rating">
                    <option disabled value="">Select rating</option>
                    <option v-for="n in 5" :key="n" :value="n">{{ n }} Star{{ n > 1 ? 's' : '' }}</option>
                  </select>
                </div>
              </div>
              <div class="d-grid">
                <button class="btn btn-primary rounded-pill py-2 fs-5 shadow-sm" @click="payFee">
                  <i class="bi bi-credit-card me-2"></i>Pay Fee
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading parking data...</p>
      </div>
    </div>
    <div v-else-if="status === 'inprogress'" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Processing payment...</p>
    </div>

    <div v-else-if="status === 'success'" class="text-center py-5">
      <div class="d-flex justify-content-center align-items-center mb-4">
        <span class="bg-success bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center" style="width: 90px; height: 90px;">
          <i class="bi bi-check-circle-fill text-success" style="font-size: 3.5rem;"></i>
        </span>
      </div>
      <h4 class="text-success fw-bold">Payment Successful!</h4>
      <p class="mt-3">Redirecting to dashboard in {{ sec }}...</p>
    </div>

    <div v-else-if="status === 'error'" class="text-center py-5">
      <div class="d-flex justify-content-center align-items-center mb-4">
        <span class="bg-danger bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center" style="width: 90px; height: 90px;">
          <i class="bi bi-x-circle-fill text-danger" style="font-size: 3.5rem;"></i>
        </span>
      </div>
      <h4 class="text-danger fw-bold">Payment Failed</h4>
      <p class="mt-3 text-danger fw-bold">{{ errMsg }}</p>
      <button @click="$router.back()" class="btn btn-outline-danger mt-2">Go Back</button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import api from '../api';
import parking from '../store/parking';
import user from '../store/user';

export default {
  name: 'Payment',
  data() {
    return {
      status: 'form',
      sec: 3,
      summary: null,
      errMsg: "",
      timerInterval: null,
      leave_time: new Date(),
      feedback: "",
      rating: "",
    };
  },
  computed: {
    ...mapGetters('parking', ['parking']),
    ...mapGetters('user', ['user']),
    paymentFor() {
      return this.$route.query.payment_for || this.$route.params.payment_for || 'N/A';
    },
    parking_id() {
      return this.$route.query.parking_id;
    },
    booking_id() {
      return this.$route.query.booking_id;
    },
    booking_data() {
      if (!this.booking_id || !this.user || !this.user.bookings) return null;
      // booking_id may be string, so use == for comparison
      return this.user.bookings.find(bk => bk.id == this.booking_id) || null;
    },
    hourUsed() {
      const booking = this.booking_data;
      if (!booking) return 0;
      const start = new Date(booking.start_time);
      const end = booking.leave_time ? new Date(booking.leave_time) : this.leave_time;
      const diffMs = end - start;
      const hours = Math.ceil(diffMs / (1000 * 60 * 60));
      return hours > 0 ? hours : 0;
    },
    totalAmount() {
      if (!this.parking) return 0;
      if (this.paymentFor === 'booking') {
        return this.parking.booking_fee;
      } else if (this.paymentFor === 'leave_parking') {
        return this.parking.hourly_fee * this.hourUsed;
      }
      return 0;
    },
  },
  inject: ['notify'],
  methods: {
    ...mapActions('parking', ['fetchParkingById']),
    ...mapActions('user', ['fetchCurrentUser']),
    async loadUser() {
      await this.fetchCurrentUser();
    },
    startRedirectTimer() {
      this.sec = 3;
      if (this.timerInterval) clearInterval(this.timerInterval);
      this.timerInterval = setInterval(() => {
        if (this.sec > 1) {
          this.sec--;
        } else {
          clearInterval(this.timerInterval);
          this.$router.push("/user");
        }
      }, 1000);
    },
    async bookSlot() {
      try {
        this.status = 'inprogress';
        const response = await api.post("/api_v1/reservation", {
          parking_id: this.parking.id
        });
        this.summary = response.data?.payment_details;
        this.status = 'success';
        this.notify && this.notify({ message: "Successfully booked slot", type: "success" });
        this.startRedirectTimer();
      } catch (err) {
        this.status = 'error';
        this.errMsg = err?.response?.data?.message || "Oops, something went wrong :(";
        this.notify && this.notify({ message: this.errMsg, type: "danger" });
      }
    },
    async leaveSlot() {
      try {
        if (!this.feedback || !this.rating) {
          this.notify({
            message: "Feedback and rating required!",
            title: "Warning"
          })
          return;
        }

        this.status = 'inprogress';
        await api.put("/api_v1/reservation", {
          reservation_id: this.booking_id,
          parking_id : this.parking_id,
          leave_time: this.leave_time,
          feedback: this.feedback,
          rating: this.rating,
        });
        this.status = 'success';
        this.notify && this.notify({ message: "Successfully left slot", type: "success" });
        this.startRedirectTimer();
      } catch (err) {
        this.status = 'error';
        this.errMsg = err?.response?.data?.message || "Oops, something went wrong :(";
        this.notify && this.notify({ message: this.errMsg, type: "danger" });
      }
    },
    payFee() {
      if (this.paymentFor === 'booking') {
        this.bookSlot();
      } else if (this.paymentFor === 'leave_parking') {
        this.leaveSlot();
      } else {
        this.errMsg = "Invalid payment type.";
        this.status = "error";
      }
    },
  },
  async beforeMount() {
    await this.fetchParkingById(this.parking_id);
    await this.loadUser();
  },
  beforeUnmount() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  }
};
</script>

<style scoped>
.bg-primary-subtle {
  background-color: #e7f1ff !important;
}
</style>