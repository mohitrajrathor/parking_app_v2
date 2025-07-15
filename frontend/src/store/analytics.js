// store/modules/parking.js
import api from '../api';

const state = {
  dashboardAnalyticsData: null,
  parkingAnalyticsData: null,
};

const mutations = {
  SET_DASHBOARD_DATA(state, payload) {
    state.dashboardAnalyticsData = payload;
  },
  SET_PARKING_ANALYTIC_DATA(state, payload) {
    state.parkingAnalyticsData = payload;
  }
};


const actions = {
  async fetchParkingAnalytics({ commit }) {
    try {
      const response = await api.get("/api_v1/analytics/parking_analytics", {
        withCredentials: true,
      });
      const data = response.data;
      commit('SET_PARKING_ANALYTIC_DATA', { ...data });
    } catch (err) {
      console.error(err.message || "Unable to fetch parking analytics data.");
      if (err.response && err.response.data) {
        console.error(err.response.data.message || "Unable to fetch parking analytics data");
      }
    }
    },


  async fetchDBAData({ commit }) {
    try {
      const response = await api.get("/api_v1/analytics/databoard_analytics", {
        withCredentials: true,
      });
      const data = await response.data;
      commit('SET_DASHBOARD_DATA', { ...data });
    } catch (err) {
      console.error(err.message || "Unable to fetch dashboard analytics data.");
    }

  }
};

const getters = {
  dashboardAnalyticsData: (state) => state.dashboardAnalyticsData,
  parkingAnalyticsData: (state) => state.parkingAnalyticsData,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
