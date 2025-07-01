// store/modules/parking.js
import api from '../api';

const state = {
  parking: null,
  parkings: [],
  total: 0,
  page: 1,
  pages: 1,
};

const mutations = {
  SET_PARKINGS(state, payload) {
    state.parkings = payload.parkings;
    state.total = payload.total;
    state.page = payload.page;
    state.pages = payload.pages;
  },
  SET_PARKING(state, payload) {
    state.parking = payload;
  }
};


const actions = {
  async fetchParkings({ commit }, { page = 1, query = '', lat = null, long = null } = {}) {
    try {
      let url = `/api_v1/parking?page=${page}`;
      const params = [];
      if (query && query !== '') params.push(`query=${encodeURIComponent(query)}`);
      if (lat !== null) params.push(`lat=${lat}`);
      if (long !== null) params.push(`long=${long}`);
      if (params.length > 0) {
        url += '&' + params.join('&');
      }

      const response = await api.get(url, {
        withCredentials: true,
      });
      const data = response.data;

      commit('SET_PARKINGS', {
        parkings: data.parkings,
        total: data.total,
        page: data.page,
        pages: data.pages,
      });
    } catch (error) {
      console.error('Failed to fetch parking data:', error);
    }
  },


  async fetchParkingById({ commit }, id = 1) {
    try {

      const response = await api.get(`/api_v1/parking/by_id?id=${id}`, {
        withCredentials: true,
      });
      const data = response.data;

      commit('SET_PARKING', {
        ...data
      });


    } catch (err) {

    }
  }
};

const getters = {
  parking: (state) => state.parking,
  parkings: (state) => state.parkings,
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
