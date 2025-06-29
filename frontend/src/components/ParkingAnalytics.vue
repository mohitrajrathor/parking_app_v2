<template>
  <div class="p-2 bg-light rounded-3 my-3">
    <div class="rounded-4 p-5">
      <ParkingSlotGrowthChart />
    </div>
    <div class="row align-items-center p-md-4">
      <div class="col-md-6 p-3">
        <ParkingAreaChart />
      </div>
      <div class="col-md-6 p-3">
        <ParkingDemandChart />
      </div>
    </div>
  </div>
</template>

<script>
import ParkingAreaChart from './ParkingAreaChart.vue';
import ParkingDemandChart from './ParkingDemandChart.vue';
import ParkingSlotGrowthChart from './ParkingSlotGrowthChart.vue';

export default {
  name: "ParkingAnalytics",
  components: { ParkingAreaChart, ParkingDemandChart, ParkingSlotGrowthChart }
};
</script>
