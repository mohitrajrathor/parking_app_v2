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
            <UserTable :users="users" :page="page" :pages="pages" @update:page="fetchUsers" />

        </div>
    </div>
</template>
<script>
import UserAgeDistChart from './UserAgeDistChart.vue';
import UserProfessionDist from './UserProfessionDist.vue';
import UserGrowthChart from './UserGrowthChart.vue';
import UserTable from './user/UserTable.vue';
import api from '../api';
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
    methods: {
        ...mapActions("user", ["fetchUsers"]),
        changePage(newPage) {
            this.fetchUsers(newPage);
        },

        // async fetchUsers(page = 1, query = null) {
        //     try {

        //         let url = `/api_v1/user?page=${page}`

        //         if (query != null) {
        //             url = `/api_v1/user?page=${page}&query=${query}`
        //         }
        //         const response = await api.get(url, {
        //             withCredentials: true,
        //         });
        //         const data = await response.data;

        //         console.log(data);
        //     } catch (error) {
        //         console.error('Failed to fetch user data:', error);
        //     }
        // },
    },
    mounted() {
        this.fetchUsers();
    }
}
</script>
<style scoped></style>