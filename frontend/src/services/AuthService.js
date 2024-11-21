import store from "@/store";
import API from "@/api/api";

class AuthService {
  login(user) {
    return API
      .post('accounts/login/', user)
      .then(response => {
        if (response.data.access) {
          this.handleResponse(response.data);
        }
        return response.data;
      });
  }

  register(user) {
    return API
      .post('accounts/registration/', user)
      .then(response => {
        if (response.data.access) {
          this.handleResponse(response.data);
        }
        return response.data;
      });
  }

  handleResponse(data) {
    const userData = {
      ...data.user,
      accessToken: data.access,
      refreshToken: data.refresh,
    };
    store.dispatch('auth/saveUserData', userData);
  }

  logout() {
    store.dispatch('auth/logout');
  }
}

export default new AuthService();
