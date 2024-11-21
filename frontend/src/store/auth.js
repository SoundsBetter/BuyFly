const state = {
    user: JSON.parse(localStorage.getItem('user')) || null,
    isRefreshing: false
};

const mutations = {
    SET_USER_DATA(state, userData) {
        state.user = userData;
        localStorage.setItem('user', JSON.stringify(userData));
    },
    CLEAR_USER_DATA(state) {
        state.user = null;
        localStorage.removeItem('user');
    },
    setIsRefreshing(state, isRefreshing) {
        state.isRefreshing = isRefreshing;
    }
};

const actions = {
    saveUserData({commit}, userData) {
        commit('SET_USER_DATA', userData);
    },
    logout({commit}) {
        commit('CLEAR_USER_DATA');
    },
    startTokenRefresh({commit}) {
        commit('setIsRefreshing', true);
    },
    finishTokenRefresh({commit}) {
        commit('setIsRefreshing', false);
    }
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
};
