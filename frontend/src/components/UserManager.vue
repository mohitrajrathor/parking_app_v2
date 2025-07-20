<template>
  <div id="userManager">
    <!-- analytics -->
    <div id="userAnalytics" class="rounded-4">
      <div class="p-3 bg-white rounded-4">
        <div class="row g-4">
          <div class="col-md-12">
            <UserGrowthChart :monthlyGrowth="userAnalyticsData?.monthly_user_growth || {}" />
          </div>
          <div class="col-md-6">
            <UserProfessionDistChart :professionDist="userAnalyticsData?.profession_dist || {}" />
          </div>
          <div class="col-md-6">
            <UserAgeDistChart :ageDist="userAnalyticsData?.age_dist || {}" />
          </div>
        </div>
      </div>
    </div>
    <!-- user -->
    <div class="my-3">
      <UserTable :isLoading="isLoading" :users="users" :page="page" :pages="pages" @update:page="changePage"
        @search:query="queryResult" />
    </div>
  </div>
</template>
<script>
import UserGrowthChart from './analytics/UserGrowthChart.vue';
import UserProfessionDistChart from './analytics/UserProfessionDistChart.vue';
import UserAgeDistChart from './analytics/UserAgeDistChart.vue';
import UserTable from './user/UserTable.vue';
import { mapGetters, mapActions } from "vuex";

export default {
  name: "UserManager",
  components: {
    UserGrowthChart,
    UserProfessionDistChart,
    UserAgeDistChart,
    UserTable,
  },
  computed: Object.assign({},
    mapGetters("user", ["users", "pages", "page", "userAnalyticsData"])
  ),
  data() {
    return {
      isLoading: false,
      query: ""
    };
  },
  methods: Object.assign({},
    mapActions("user", ["fetchUsers", "fetchUserAnalytics"]),
    {
      async changePage(newPage) {
        this.isLoading = true;
        await this.fetchUsers({ page: newPage, query: this.query });
        this.isLoading = false;
      },
      async queryResult(query) {
        this.isLoading = true;
        this.query = query;
        await this.fetchUsers({ query: query });
        this.isLoading = false;
      }
    }
  ),
  async mounted() {
    this.isLoading = true;
    await Promise.all([
      this.fetchUsers(),
      this.fetchUserAnalytics()
    ]);
    this.isLoading = false;
  }
}
</script>
<style scoped>
#userAnalytics {
  background: #fff;
}
</style>