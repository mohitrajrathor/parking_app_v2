// store/modules/reservation.js
import api from '../api';

const state = {
  reservation: null,
  reservations: [],
  total: 0,
  page: 1,
  pages: 1,
};

const mutations = {
  SET_RESERVATIONS(state, payload) {
    state.reservations = payload.reservations;
    state.total = payload.total;
    state.page = payload.page;
    state.pages = payload.pages;
  },
  SET_RESERVATION(state, payload) {
    state.reservation = payload;
  }
};

const actions = {
  async fetchReservations({ commit }, { page = 1, query = '', lat = null, long = null, per_page=5 } = {}) {
    try {
      let url = `/api_v1/reservation?page=${page}`;
      const params = [];
      if (query && query !== '') params.push(`query=${encodeURIComponent(query)}`);
      if (lat !== null) params.push(`lat=${lat}`);
      if (long !== null) params.push(`long=${long}`);
    if (per_page !== 10) params.push(`per_page=${per_page}`)
      if (params.length > 0) {
        url += '&' + params.join('&');
      }

      const response = await api.get(url, {
        withCredentials: true,
      });
      const data = response.data;

      commit('SET_RESERVATIONS', {
        reservations: data.reservations || data.parkings || [],
        total: data.total,
        page: data.page,
        pages: data.pages,
      });
    } catch (error) {
      console.error('Failed to fetch reservations data:', error);
    }
  },


  async fetchReservationById({ commit }, id = 1) {
    try {

      const response = await api.get(`/api_v1/reservation/by_id?id=${id}`, {
        withCredentials: true,
      });
      const data = response.data;

      commit('SET_RESERVATION', {
        ...data
      });


    } catch (err) {
        console.error(err);
    }
  }
};

const getters = {
  reservation: (state) => state.reservation,
  reservations: (state) => state.reservations,
  rtotal: (state) => state.total,
  rpage: (state) => state.page,
  rpages: (state) => state.pages,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
