<template>
    <div id="adminDashboard" class="mb-5">
        <h2 class="text-start mb-4">Dashboard</h2>

        <Stats />

        <div class="px-4">
            <div class="p-4 bg-light rounded-4">
                <ParkingSlotGrowthChart />
            </div>

        </div>


    </div>
</template>
<script>
import Stats from './Stats.vue';
import LeafletMap from '../components/LeafletMap.vue';

import UserAgeDistChart from './UserAgeDistChart.vue';
import UserGrowthChart from './UserGrowthChart.vue';
import ParkingSlotGrowthChart from './ParkingSlotGrowthChart.vue';

export default {
    name: "AdminDashboard",
    components: {
        ParkingSlotGrowthChart,
        Stats,
        LeafletMap,
        UserAgeDistChart,
        UserGrowthChart
    }
}
</script>
<style scoped></style>