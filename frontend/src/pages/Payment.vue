<template>
  <div class="container py-4">
    <div v-if="status === 'form'">
      <div v-if="parking" class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-6">
          <!-- Credit Card Design -->
          <div class="credit-card mb-4 shadow-lg rounded-4 position-relative overflow-hidden">
            <div class="credit-card-bg"></div>
            <div class="credit-card-content p-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="text-white fw-bold fs-5">{{ parking.name }}</span>
                <img src="https://img.icons8.com/color/48/000000/bank-card-back-side.png" alt="Card"
                  style="height: 32px;" />
              </div>
              <div class="text-white fs-4 mb-2">
                •••• •••• •••• {{ (parking.id + '0000').slice(-4) }}
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-white-50 small">Card Holder</div>
                  <div class="text-white fw-semibold">{{ user ? user.name : 'User' }}</div>
                </div>
                <div>
                  <div class="text-white-50 small">Valid Thru</div>
                  <div class="text-white">12/29</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Fee Breakdown Card -->
          <div class="card shadow rounded-4 mb-4">
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
                  <span class="fw-bold">{{ paymentFor }}</span>
                </li>
              </ul>
              <div class="d-grid">
                <button class="btn btn-gradient rounded-pill py-2 fs-5 shadow-sm" @click="payFee">
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
      <p class="mt-3">processing payment...</p>
    </div>

    <div v-else-if="status === 'success'" class="text-center py-5">
      <!-- INSERT_YOUR_CODE -->
      <div class="d-flex justify-content-center align-items-center mb-4">
        <span class="bg-success bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center" style="width: 90px; height: 90px;">
          <i class="bi bi-check-circle-fill text-success" style="font-size: 3.5rem;"></i>
        </span>
      </div>
      
      <div>

      </div>
      <p class="mt-3">Payment successful redirecting in {{ sec }}...</p>
    </div>

    <div v-else-if="status === 'error'" class="text-center py-5">
      <div class="d-flex justify-content-center align-items-center mb-4">
        <span class="bg-danger bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center" style="width: 90px; height: 90px;">
          <i class="bi bi-x-circle-fill text-danger" style="font-size: 3.5rem;"></i>
        </span>
      </div>
      <p class="mt-3 text-danger fw-bold">{{ errMsg }}</p>
      <p class="mt-3 text-danger fw-bold">Payment failed. Please try again.</p>
      <button @click="$router.back()" class="btn btn-outline-danger">Go Back</button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import parking from '../store/parking';
import api from '../api';

export default {
  name: 'Payment',
  data() {
    return {
      user: null,
      message: "processing payment...",
      status: 'form',
      sec: 3,
      summary: null,
      errMsg: "",
    };
  },
  computed: {
    ...mapGetters('parking', ['parking']),
    paymentFor() {
      // Get payment_for from route params or query
      return this.$route.query.payment_for || this.$route.params.payment_for || 'N/A';
    },
    parking_id() {
      return this.$route.query.parking_id;
    },
  },
  inject: ['notify'],
  methods: {
    ...mapActions('parking', ['fetchParkingById']),
    ...mapActions('user', ['fetchCurrentUser']),
    async loadUser() {
      const user = await this.fetchCurrentUser();
      this.user = user || null;
    },

    timer() {
    setInterval(() => {
      if (this.sec > 0) {
        this.sec--;
      } else {
        this.status = 'success';
      }
    }, 1000);
  },
  
  
  async bookSlot() {
    try {
      
      this.status = 'inprogress'
      
      console.log("parking id to revser", this.parking.id);
      console.log("given parking id", this.parking_id);

      const response = await api.post("/api_v1/reservation", {
        parking_id: this.parking.id
      })
      
      const data = await response.data;
      
      this.summary = data.payment_details;
      
      this.status = 'success';
      this.timer();
      
      this.$router.push("/user")
      
      setInterval(() => {
        // do nothing 
        if (this.sec > 0) {
          this.sec--;
        }
      }, 1);
      
      this.notify({
        message: "Successfully booked slot"
      })
      
    } catch (err) {
      console.error(err)
      this.status = 'error';
      const data = await err.response.data;
      this.errMsg = data?.message || "Oops something went wrong :("
      
    }
  },
  
  async leaveSlot() {
    try {
      
      this.status = 'inprogress'
      
      const response = await api.post("/api_v1/reservation/leave", {
        revervation_id: this.revervation_id
      })
      
      const data = await response.data;
      
      this.status = 'success';
      this.timer();
      
      this.$router.push("/user")
      
      setInterval(() => {
        // do nothing 
        if (this.sec > 0) {
          this.sec--;
        }
      }, 1);
      
      this.notify({
        message: "Successfully booked slot"
      })
      
    } catch (err) {
      this.status = 'error';
      const data = await err.response.data;
      errMsg = data?.message || "Oops something went wrong :("
    }

  },
  payFee() {
    if (this.paymentFor === 'booking') {
      this.bookSlot();
    } else if (this.paymentFor === 'leaving') {
      this.leaveSlot();
    } else {
      alert("processing payment...")
    }
  },
  },
  async created() {
    await this.fetchParkingById(this.parking_id);
    await this.loadUser();
  },
  
  
  
  
};
</script>

<style scoped>
.credit-card {
  background: linear-gradient(135deg, #1976d2 60%, #42a5f5 100%);
  min-height: 180px;
  border-radius: 1.5rem;
  position: relative;
  overflow: hidden;
}

.credit-card-bg {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 50%;
  z-index: 1;
}

.credit-card-content {
  position: relative;
  z-index: 2;
}

.btn-gradient {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  transition: box-shadow 0.2s, transform 0.2s;
}

.btn-gradient:hover {
  box-shadow: 0 4px 16px rgba(56, 249, 215, 0.18);
  transform: translateY(-2px) scale(1.03);
  color: #fff;
}

.card-title {
  font-weight: 600;
}
</style>