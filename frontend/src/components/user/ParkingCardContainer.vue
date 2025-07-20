<template>
  <div class="p-2 bg-primary-subtle rounded-4 ">
    <div class="container py-4">

      <div class="row g-2 align-items-center mb-4 flex-column flex-md-row">
        <div class="col-12 col-md-auto mb-2 mb-md-0">
          <h2 class="text-primary fw-bold mb-0 d-flex align-items-center">
            <i class="bi bi-geo-alt-fill me-2 fs-3 text-dark"></i>
            Parkings
          </h2>
        </div>
        <div class="col-12 col-md flex-grow-1">
          <form class="d-flex" @submit.prevent="onQuerySubmit">
            <input v-model="query" type="text"
              class="form-control rounded-start-pill border-primary border-end-0 shadow-sm"
              placeholder="Search parkings by name, area..." aria-label="Search parkings" />
            <button class="btn btn-primary rounded-end-pill px-4 shadow-sm" type="submit" style="margin-left: -1px;">
              <i class="bi bi-search"></i>
            </button>
          </form>
        </div>
      </div>

      <div v-if="parkings.length" class="row g-4 justify-content-center">
        <div class="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3 d-flex align-items-stretch" v-for="parking in parkings" :key="parking.id">
          <ParkingCard :id="parking.id" :name="parking.name" :bookingFee="parking.booking_fee"
            :hourlyFee="parking.hourly_fee" :availableSlots="parking.slots_num - (parking.booked || 0)"
            @view="handleViewParking" class="card h-100 w-100 shadow-sm border-0" />
        </div>
      </div>
      <div v-else style="min-height: 250px;" class="d-flex text-primary justify-content-center align-items-center">
        <div>
          <h2 class="text-center">Oops</h2>
          <h3 class="text-center">No Parkings found !</h3>
        </div>
      </div>

      <div class="d-flex justify-content-center mt-4">
        <Pagination :page="page" :pages="pages" @update:page="changePage" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import ParkingCard from "./ParkingCard.vue";
import Pagination from "../Pagination.vue";

export default {
  name: "ParkingCardContainer",
  data() {
    return {
      query: '',
      lat: null,
      long: null,
    };
  },
  computed: {
    ...mapGetters("parking", ["parkings", "page", "pages"])
  },
  emits: ['update:page'],
  methods: {
    ...mapActions("parking", ["fetchParkings"]),

    changePage(newPage) {
      this.$emit('update:page', newPage);
      this.fetchParkings({ page: newPage, query: this.query, lat: this.lat, long: this.long });
    },
    handleViewParking(id) {
      this.$router.push(`/parking/${id}`);
      return;
    },
    onQuerySubmit() {
      this.fetchParkings({ page: 1, query: this.query, lat: this.lat, long: this.long });
    }
  },
  created() {
    this.fetchParkings({ page: 1, query: this.query, lat: this.lat, long: this.long });
  },
  components: {
    ParkingCard,
    Pagination
  }
};
</script>

<style scoped>
.bg-primary-subtle {
  background-color: #e7f1ff !important;
}
</style>