<template>
  <div class="parkingManager">

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Parking Management</h2>
      <button class="btn btn-primary rounded-pill" @click="$router.push({ name: 'AddParking' })">
        <i class="bi bi-plus-circle"></i> New Parking
      </button>
    </div>

    
    <ParkingAnalytics />
    
    <div class="my-4">
      <LeafletMap />
    </div>

    <ParkingTable :parkings="parkings" :page="page" :pages="pages" @update:page="fetchParkings" />
  </div>
</template>

<script>
import ParkingAnalytics from './ParkingAnalytics.vue';
import ParkingTable from './ParkingTable.vue';
import LeafletMap from './LeafletMap.vue';
import { mapGetters, mapActions } from 'vuex';



export default {
  name: "ParkingManager",
  components: {
    ParkingAnalytics,
    ParkingTable,
    LeafletMap
  },
  computed: {
    ...mapGetters("parking", ['parkings', 'page', 'pages'])
  },
  methods: {
    ...mapActions("parking", ['fetchParkings'])
  },
  mounted() {
    this.fetchParkings();
  }
};
</script>
