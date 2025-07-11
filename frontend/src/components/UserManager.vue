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
        <div class="my-3">
            <UserTable :isLoading="isLoading" :users="users" :page="page" :pages="pages" @update:page="changePage" />

        </div>
    </div>
</template>
<script>
import UserAgeDistChart from './UserAgeDistChart.vue';
import UserProfessionDist from './UserProfessionDist.vue';
import UserGrowthChart from './UserGrowthChart.vue';
import UserTable from './user/UserTable.vue';
import {
    mapGetters, mapActions
} from "vuex";

export default {
    name: "UserManager",
    components: {
        UserGrowthChart,
        UserProfessionDist,
        UserAgeDistChart,
        UserTable,
    },
    computed: {
        ...mapGetters("user", ["users", "pages", "page"]),
    },
    data() {
        return {
            isLoading: false
        };
    },
    methods: {
        ...mapActions("user", ["fetchUsers"]),
        async changePage(newPage) {
            this.isLoading = true;
            await this.fetchUsers({page: newPage});
            this.isLoading = false;
        },
    },
    async mounted() {
        this.isLoading = true;
        await this.fetchUsers();
        this.isLoading = false;
    }
}
</script>
<style scoped></style>