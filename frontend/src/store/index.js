import { createStore } from 'vuex';

const store = createStore({
  state: {
    isRefreshing: false,
  },
  mutations: {
    setIsRefreshing(state, isRefreshing) {
      state.isRefreshing = isRefreshing;
    }
  },
  actions: {
    startTokenRefresh({ commit }) {
      commit('setIsRefreshing', true);
    },
    finishTokenRefresh({ commit }) {
      commit('setIsRefreshing', false);
    }
  }
});

export default store;
