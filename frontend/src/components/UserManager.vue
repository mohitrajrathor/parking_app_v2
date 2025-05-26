<template>
    <div id="userManager">
        <!-- analytics -->
        <div id="userAnalytics">
            <div class="p-3 m-1 bg-light rounded-4">
                <div class="p-3">
                    <UserGrowthChart />
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="p-3">
                            <UserProfessionDist />
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3">
                            <UserAgeDistChart />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- user -->
        <div class=" bg-primary m-1 text-light rounded-4 p-3 mt-3">

            <h1 class="text-center">
                Recent Users
            </h1>

            <div class="p-3">
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
</template>
<script>
import UserAgeDistChart from './UserAgeDistChart.vue';
import UserTile from './UserTile.vue';
import UserProfessionDist from './UserProfessionDist.vue';
import UserGrowthChart from './UserGrowthChart.vue';

export default {
    name: "UserManager",
    components: {
        UserGrowthChart,
        UserProfessionDist,
        UserAgeDistChart,
        UserTile,
    }
}
</script>
<style scoped></style>