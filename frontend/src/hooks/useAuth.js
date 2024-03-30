import { computed } from 'vue';
import { useStore } from 'vuex';

export function useAuth() {
  const store = useStore();

  const user = computed(() => store.state.auth.user);

  const hasRole = (role) => user.value?.groups?.includes(role) || false;

  return { user, hasRole };
}
