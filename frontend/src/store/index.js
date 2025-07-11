import { createStore } from "vuex";
import parking from "./parking";
import user from "./user";
import reservation from "./reservation";


const store = createStore({
  state: {
    role: localStorage.getItem("role") || null,
    token: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
    position: {
      lat: null,
      long: null
    },
    choosenPos: {
      lat: null,
      long: null
    }
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
    
    setPosition(state, cord) {
      state.position = cord;
    },

    choosePos(state, coords) {
      state.choosenPos = coords;
    }

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

    addNtfy({commit}, notify_obj) {
      commit("addNtfy", notify_obj);
    },

    clearNotifications({commit}) {
      commit("clearNtfy");
    },


    choosePosition({commit}, coords) {
      commit("choosePos", coords);
    },


    startTracking({commit}) {
      if (!navigator.geolocation) {
        console.error("Geolocation not supported.");
        return;
      }

      navigator.geolocation.getCurrentPosition((pos) => {
          commit("setPosition", {
            lat: pos.coords.latitude,
            long: pos.coords.longitude,
          })
        },
        (err) => {
          console.error("Error getting location:", err);
        }
      )
    }

  },
  getters: {
    role: (state) => state.role,
    getToken: (state) => state.token,
    getRefreshToken: (state) => state.refreshToken,
    isAuthenticated: (state) => !!state.token,
    getPosition: (state) => state.position,
    getChoosenPos: (state) => state.choosenPos,
  },

  modules: {
    parking,
    user,
    reservation
  }

});

export default store;
