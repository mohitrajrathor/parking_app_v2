<template>
  <div id="addParking" class="mb-5">
    <div class="card card-custom rounded-5 p-4 p-md-5 w-100">
      <h2 class="card-title text-center mb-4 mb-md-5 fw-bold text-dark">
        Parking Spot Details
      </h2>
      <form @submit.prevent="submitForm">
        <!-- Name Input -->
        <div class="mb-3">
          <label for="name" class="form-label text-muted">Parking Name</label>
          <input
            v-model="name"
            type="text"
            class="form-control"
            id="name"
            placeholder="e.g., City Parking Lot A"
            required
          />
        </div>

        <!-- Address Input -->
        <div class="mb-3">
          <label for="address" class="form-label text-muted">Address</label>
          <input
            v-model="address"
            type="text"
            class="form-control"
            id="address"
            placeholder="e.g., 123 Main St, Anytown"
            required
          />
        </div>

        <div class="row g-3 mb-3">
          <!-- Pincode Input -->
          <div class="col-md-6">
            <label for="pincode" class="form-label text-muted">Pincode</label>
            <input
              v-model="pincode"
              type="text"
              class="form-control"
              id="pincode"
              placeholder="e.g., 123456"
              required
            />
          </div>

          <!-- Phone Input -->
          <div class="col-md-6">
            <label for="phone" class="form-label text-muted">Phone Number</label>
            <input
              v-model="phone"
              type="tel"
              class="form-control"
              id="phone"
              placeholder="e.g., 9876543210"
              required
            />
          </div>
        </div>

        <div class="row g-3 mb-4">
          <!-- Latitude Input -->
          <div class="col-md-6">
            <label for="lat" class="form-label text-muted">Latitude</label>
            <input
              v-model="lat"
              type="number"
              class="form-control"
              id="lat"
              placeholder="e.g., 34.0522"
              step="any"
              readonly
            />
          </div>

          <!-- Longitude Input -->
          <div class="col-md-6">
            <label for="long" class="form-label text-muted">Longitude</label>
            <input
              v-model="long"
              type="number"
              class="form-control"
              id="long"
              placeholder="e.g., -118.2437"
              step="any"
              readonly
            />
          </div>
        </div>

        <div class="row g-3 mb-4">
          <h6 class="text-muted">Choose on map</h6>
          <LeafletMap />
        </div>

        <div class="row g-3 mb-4">
          <!-- Fee Input -->
          <div class="col-md-6">
            <label for="fee" class="form-label text-muted">Parking Fee (per hour)</label>
            <input
              v-model="fee"
              type="number"
              class="form-control"
              id="fee"
              placeholder="e.g., 50"
              min="0"
              required
            />
          </div>

          <!-- Number of Slots Input -->
          <div class="col-md-6">
            <label for="slots_num" class="form-label text-muted">Number of Slots</label>
            <input
              v-model="slots_num"
              type="number"
              class="form-control"
              id="slots_num"
              placeholder="e.g., 100"
              min="0"
              required
            />
          </div>
        </div>

        <!-- Submit Button -->
        <div class="d-grid">
          <button type="submit" class="btn btn-primary btn-lg">Add Parking Spot</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import LeafletMap from './LeafletMap.vue';

export default {
  name: "AddParking",
  components: {
    LeafletMap,
  },
  data() {
    return {
      name: "",
      address: "",
      pincode: "",
      fee: "",
      phone: "",
      lat: null,
      long: null,
      slots_num: "",
    };
  },
  computed: {
    choosenPos() {
      return this.$store.getters.getChoosenPos;
    }
  },
  watch: {
    choosenPos: {
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.lat && newVal.long) {
          this.lat = newVal.lat;
          this.long = newVal.long;
        }
      }
    }
  },
  methods: {
    submitForm() {
      const parkingData = {
        name: this.name,
        address: this.address,
        pincode: this.pincode,
        phone: this.phone,
        lat: this.lat,
        long: this.long,
        fee: this.fee,
        slots_num: this.slots_num
      };
      console.log("🚀 Submitting parking data:", parkingData);

      // You could dispatch an action or make an API call here
      // this.$store.dispatch('addParking', parkingData)
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
