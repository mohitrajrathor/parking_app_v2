<template>
    <div id="adminDashboard">
        <h2 class="text-start">Dashboard</h2>
        <Stats />

        <div class="row m-2">
            <div class="col-lg-6 bg-light rounded-4 p-3">
                <div class="p-3 rounded-3">
                    <ParkingLotGrowthChart />
                </div>
                <div class="p-lg-2 mt-3">
                    <LeafletMap />
                </div>
            </div>

            <div class="col-lg-6 -2 overflow-auto">
                <div class="row p-3 rounded-4 bg-light">
                    <div class="col-lg-6">
                        <UserGrowthChart />
                    </div>
                    <div class="col-lg-6">
                        <UserAgeDistChart />
                    </div>
                </div>

                <div class="p-3 bg-primary text-light rounded-3">
                    <h3>Recent User</h3>

                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />
                    <UserTile :user="{
                        status: true,
                        name: 'user 01',
                        phone: '9876543210',
                        email: 'test@parkly.com'
                    }" />

                </div>


            </div>
        </div>
    </div>
</template>
<script>
import Stats from './Stats.vue';
import LeafletMap from '../components/LeafletMap.vue';
import UserTile from './UserTile.vue';
import UserAgeDistChart from './UserAgeDistChart.vue';
import UserGrowthChart from './UserGrowthChart.vue';
import ParkingLotGrowthChart from './ParkingLotGrowthChart.vue';

export default {
    name: "AdminDashboard",
    components: {
        ParkingLotGrowthChart,
        Stats,
        LeafletMap,
        UserTile,
        UserAgeDistChart,
        UserGrowthChart
    }
}
</script>
<style scoped></style>