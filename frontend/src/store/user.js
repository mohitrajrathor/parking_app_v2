// store/modules/user.js
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
        state.users = payload.users;
        state.total = payload.total;
        state.page = payload.page;
        state.pages = payload.pages;
    }, 
    SET_USER(state, payload){
        state.user = payload;
    },
};

const actions = {

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

            console.log(data);

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
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
};
