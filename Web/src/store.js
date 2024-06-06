// src/store.js
import { createStore } from 'vuex';

const store = createStore({
  state: {
    data: null
  },
  mutations: {
    setData(state, newData) {
      state.data = newData;
    }
  },
  actions: {
    updateData({ commit }, newData) {
      commit('setData', newData);
    }
  },
  getters: {
    getData: (state) => state.data
  }
});

export default store;
