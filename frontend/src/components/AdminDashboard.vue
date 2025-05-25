<template>
    <div id="adminDashboard">
        <h2 class="text-start">Dashboard</h2>
        <Stats />

        <div class="row mt-3">
            <div class="col-lg-6 bg-light p-3">
                <BarChart />
                <div class="p-lg-2 mt-3">
                    <LeafletMap />
                </div>
            </div>

            <div class="col-lg-6 overflow-auto">
                <div class="row my-3">
                    <div class="col-lg-6">
                        <BarChart />
                    </div>
                    <div class="col-lg-6">
                        <BarChart />
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
import BarChart from '../components/BarChart.vue';
import Stats from './Stats.vue';
import LeafletMap from '../components/LeafletMap.vue';
import UserTile from './UserTile.vue';

export default {
    name: "AdminDashboard",
    components: {
        BarChart,
        Stats,
        LeafletMap,
        UserTile
    }
}
</script>
<style scoped></style>