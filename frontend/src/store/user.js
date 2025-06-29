// store/modules/parking.js
import api from '../api';

const state = {
    user: localStorage.getItem("user") || null,
    users: [],
    total: 0,
    page: 1,
    pages: 1,
};

const mutations = {
    SET_USERS(state, payload) {
        state.parkings = payload.users;
        state.total = payload.total;
        state.page = payload.page;
        state.pages = payload.pages;
    }
};

const actions = {

    async fetchCurrentUser({commit}) {
        const response = await api.get("/api_v1/user")
    },

    async fetchUsers({ commit }, page = 1, query = null, lat = null, long = null) {
        try {

            let url = `/api_v1/user?page=${page}`

            if (query != null) {
                url = `/api_v1/user?page=${page}&query=${query}`
            } else if (query != null & lat != null & long != null) {
                url = `/api_v1/user?page=${page}&query=${query}&lat=${lat}&long=${long}`
            } else if (lat != null & long != null) {
                url = `/api_v1/user?page=${page}&lat=${lat}&long=${long}`
            }



            const response = await api.get(url, {
                withCredentials: true,
            });
            const data = response.data;

            commit('SET_USER', {
                parkings: data.parkings,
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
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
};
