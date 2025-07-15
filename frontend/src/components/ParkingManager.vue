<template>
  <div class="parkingManager">

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Parking Management</h2>
      <button class="btn btn-primary rounded-pill" @click="$router.push({ name: 'AddParking' })">
        <i class="bi bi-plus-circle"></i> New Parking
      </button>
    </div>


    <div class="p-4 bg-white rounded-4">
      <ReservationTrendChart :dailyReservations="parkingAnalyticsData?.daily_reservations" />
    </div>

    <div class="my-4">
      <LeafletMap />
    </div>

    <ParkingTable :isLoading="isParkingLoading" :parkings="parkings" :page="parkingPage" :pages="parkingPages" @update:page="fetchParkingsPage" />
    <ReservationTable :isLoading="isReservationLoading" :reservations="reservations" :page="reservationPage" :pages="reservationPages" @update:page="fetchReservationsPage" />
  </div>
</template>

<script>
import ParkingTable from './ParkingTable.vue';
import LeafletMap from './LeafletMap.vue';
import { mapGetters, mapActions } from 'vuex';
import ReservationTable from './reservation/ReservationTable.vue';
import ReservationTrendChart from './analytics/ReservationTrendChart.vue';


export default {
  name: "ParkingManager",
  components: {
    ParkingTable,
    LeafletMap,
    ReservationTable,
    ReservationTrendChart
  },
  data() {
    return {
      isParkingLoading: false,
      isReservationLoading: false
    };
  },
  computed: {
    ...mapGetters("parking", ['parkings', 'page', 'pages']),
    ...mapGetters("reservation", ['reservations', 'rpage', 'rpages']),
    ...mapGetters('analytics', ['parkingAnalyticsData']),
    
    
    
    parkingPage() { return this.page; },
    parkingPages() { return this.pages; },
    reservationPage() { return this.rpage; },
    reservationPages() { return this.rpages; }
  },
  methods: {
    ...mapActions("parking", ['fetchParkings']),
    ...mapActions("reservation", ['fetchReservations']),
    ...mapActions('analytics', ['fetchParkingAnalytics']),


    async fetchParkingsPage(newPage) {
      this.isParkingLoading = true;
      await this.fetchParkings({ page: newPage });
      this.isParkingLoading = false;
    },
    async fetchReservationsPage(newPage) {
      this.isReservationLoading = true;
      await this.fetchReservations({ page: newPage });
      this.isReservationLoading = false;
    }
  },
  async mounted() {
    this.isParkingLoading = true;
    await this.fetchParkings();
    this.isParkingLoading = false;
    this.isReservationLoading = true;
    await this.fetchReservations();
    this.isReservationLoading = false;
    this.fetchParkingAnalytics();    

  }
};
</script>
