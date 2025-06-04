import { createStore } from "vuex";

const store = createStore({
  state: {
    role: localStorage.getItem("role") || null,
    token: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
  },
  mutations: {
    setRole(state, role) {
      state.role = role;
      localStorage.setItem("role", role);
    },
    setAccessToken(state, token) {
      state.token = token;
      localStorage.setItem("accessToken", token);
    },
    setRefreshToken(state, token) {
      state.refreshToken = token;
      localStorage.setItem("refreshToken", token);
    },
    clearAuthData(state) {
      state.role = null;
      state.token = null;
      state.refreshToken = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("role");
    },
  },
  actions: {
    login({ commit }, { role, token, refreshToken }) {
      commit("setAccessToken", token);
      commit("setRefreshToken", refreshToken);
      commit("setRole", role);
    },
    setToken({ commit }, token) {
      commit("setAccessToken", token);
    },
    logout({ commit }) {
      commit("clearAuthData");
    },
  },
  getters: {
    role: (state) => state.role,
    getToken: (state) => state.token,
    getRefreshToken: (state) => state.refreshToken,
    isAuthenticated: (state) => !!state.token,
  },
});

export default store;
