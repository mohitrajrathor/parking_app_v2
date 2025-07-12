// store/modules/parking.js
import api from '../api';

const state = {
  dashboardAnalyticsData: null,
};

const mutations = {
  SET_DASHBOARD_DATA(state, payload) {
    state.dashboardAnalyticsData = payload;
  },
};


const actions = {
    async fetchDBAData({ commit }) {
        try {
            const response = await api.get("/api_v1/analytics/databoard_analytics", {
        withCredentials: true,
      });
            const data = response.data;
            commit('SET_DASHBOARD_DATA', {...data});
        } catch (err) {
            console.error(err.message || "Unable to fetch dashboard analytics data.");
        }

    }
};

const getters = {
  dashboardAnalyticsData: (state) => state.dashboardAnalyticsData,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
