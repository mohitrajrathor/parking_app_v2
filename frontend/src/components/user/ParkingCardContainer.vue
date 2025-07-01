<template>
  <div class="p-2 bg-warning rounded-4 bg-opacity-5 min-vh-50">
    <div class="container py-4">

      <div class="row flex-column flex-md-row justify-content-between align-items-center mb-4 g-2">
        <div class="col-auto text-center text-md-start mb-2 mb-md-0">
          <h2 class="text-light">Parkings</h2>
        </div>
        <div class="col-auto w-100 w-md-auto">
          <form class="d-flex flex-column flex-sm-row gap-2" @submit.prevent="onQuerySubmit">
            <div class="input-group">
              <input
                v-model="query"
                type="text"
                class="form-control rounded-pill rounded-end-0"
                placeholder="Search parkings..."
                style="border-right: 0;"
              />
              <button
                class="btn btn-primary rounded-pill rounded-start-0"
                type="submit"
                style="margin-left: -12px;"
              >
                Search
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-sm-6 col-md-4" v-for="parking in parkings" :key="parking.id">
          <ParkingCard
            :id="parking.id"
            :name="parking.name"
            :bookingFee="parking.booking_fee"
            :hourlyFee="parking.hourly_fee"
            :availableSlots="parking.slots_num - (parking.booked || 0)"
            @view="handleViewParking"
          />
        </div>
      </div>
      <div class="d-flex justify-content-center mt-4">
        <Pagination
          :page="page"
          :pages="pages"
          @update:page="changePage"
        />
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
@media (max-width: 575.98px) {
  .container {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
  }
  .row.g-4 > [class^='col-'] {
    margin-bottom: 1.5rem;
  }
}
</style>