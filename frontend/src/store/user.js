// store/modules/user.js
import api from '../api';

const state = {
    user: localStorage.getItem("user") || null,
    users: [],
    total: 0,
    page: 1,
    pages: 1,
    userAnalytics: null,
};

const mutations = {
    SET_USERS(state, payload) {
        state.users = payload.users;
        state.total = payload.total;
        state.page = payload.page;
        state.pages = payload.pages;
    }, 
    SET_USER(state, payload){
        state.user = payload;
    },
    SET_USER_ANALYTICS(state, payload) {
        state.userAnalytics = payload;
    }
};

const actions = {

    async fetchUserAnalytics({ commit }) {
    try {
      const response = await api.get("/api_v1/analytics/user_analytics", {
        withCredentials: true,
      });
      const data = response.data;
      commit('SET_USER_ANALYTICS', { ...data });
    } catch (err) {
      console.error(err.message || "Unable to fetch user analytics data.");
      if (err.response && err.response.data) {
        console.error(err.response.data.message || "Unable to fetch user analytics data");
      }
    }
    },


    async fetchCurrentUser({commit}) {
        const response = await api.get(`/api_v1/user/me`, {
            withCredentials: true,
        });

        const data = await response.data;
        commit('SET_USER', data);
    },
    

    async fetchUserById({commit}, id) {
        const response = await api.get(`/api_v1/user/by_id?id=${id}`, {
            withCredentials: true,
        });

        const data = await response.data;
        commit('SET_USER', data);
    },


    async fetchUsers({ commit }, {page =1, query = null, per_page=10} = {}) {
        try {

            let url = `/api_v1/user?page=${page}&per_page=${per_page}`

            if (query != null) {
                url = `/api_v1/user?page=${page}&query=${query}&per_page=${per_page}`
            } 
            const response = await api.get(url, {
                withCredentials: true,
            });
            const data = await response.data;


            commit('SET_USERS', {
                users: data.users,
                total: data.total,
                page: data.page,
                pages: data.pages,
            });
        } catch (error) {
            console.error('Failed to fetch user data:', error);
        }
    },
};

const getters = {
    user: (state) => state.user,
    users: (state) => state.users,
    total: (state) => state.total,
    page: (state) => state.page,
    pages: (state) => state.pages,
    userAnalyticsData: (state) => state.userAnalytics,
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
};
