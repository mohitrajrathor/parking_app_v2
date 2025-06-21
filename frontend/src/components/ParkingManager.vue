<template>
    <div class="parkingManager">

        <div class=" d-flex justify-content-between align-items-center">
            <h2>
                Parking Managment
            </h2>
            <div class="">
                <button class="btn btn-primary rounded-pill" @click="$router.push({ name: 'CreateParking' })">
                    <i class="bi bi-plus-circle"></i> New Parking
                </button>
            </div>
        </div>

        <!-- analytics -->
        <div class="p-2 bg-light rounded-3 my-3">
            <div class="rounded-4 p-3">
                <ParkingSlotGrowthChart />
            </div>
            <div class="row align-items-center p-md-3">
                <div class="col-md-6 p-3">
                    <ParkingAreaChart />
                </div>
                <div class="col-md-6 p-3">
                    <ParkingDemandChart />
                </div>
            </div>
        </div>

        <!-- parking lots -->
        <div class="text-light bg-primary p-3 rounded-4">
            <h3>
                Parking lots
            </h3>

            <div class=" row-cols-md-6">
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
                <div class="col">
                    <ParkingCard />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import ParkingAreaChart from './ParkingAreaChart.vue';
import ParkingDemandChart from './ParkingDemandChart.vue';
import ParkingSlotGrowthChart from './ParkingSlotGrowthChart.vue';
import ParkingCard from './ParkingCard.vue'


export default {
    name: "ParkingManager",
    components: {
        ParkingSlotGrowthChart,
        ParkingAreaChart,
        ParkingDemandChart,
        ParkingCard
    }
}
</script>
<style scoped></style>