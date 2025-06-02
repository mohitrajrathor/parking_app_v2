import { createStore } from "vuex";

const store = createStore({
  state: {
    token: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
  },
  mutations: {
    setAccessToken(state, token) {
      state.token = token;
      localStorage.setItem("accessToken", token);
    },
    setRefreshToken(state, token) {
      state.refreshToken = token;
      localStorage.setItem("refreshToken", token);
    },
    clearAuthData(state) {
      state.token = null;
      state.refreshToken = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
  },
  actions: {
    login({ commit }, { token, refreshToken }) {
      commit("setAccessToken", token);
      commit("setRefreshToken", refreshToken);
    },
    setToken({ commit }, token) {
      commit("setAccessToken", token);
    },
    logout({ commit }) {
      commit("clearAuthData");
    },
  },
  getters: {
    getToken: (state) => state.token,
    getRefreshToken: (state) => state.refreshToken,
    isAuthenticated: (state) => !!state.token,
  },
});

export default store;
