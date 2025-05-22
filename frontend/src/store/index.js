import { createStore } from "vuex";

const store = createStore({
    state: {
        token: localStorage.getItem("token") || null,
        refreshToken: localStorage.getItem("refreshToken") || null,
    },
    mutations: {
        setAccessToken(state, token) {
            state.token = localStorage.setItem("accessToken", token);
        },
        setRefreshToken(state, token) {
            state.refreshToken = localStorage.setItem("refreshToken", token);
        },
        clearAuthData(state) {
            state.accessToken = null;
            state.refreshToken = null;

            // removing localstorage
            localStorage.clear();
        },
    },
    actions: {
        login({ commit }, { token, refreshToken }) {
            commit("setToken", token);
            commit("setRefreshToken", refreshToken);
        },
        logout({ commit }) {
            commit("clearAuthData");
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
});

export default store;