import {createRouter, createWebHistory} from 'vue-router'
import TicketList from "@/components/TicketList.vue";
import store from "@/store";

const routes = [{
    path: '/',
    name: 'home',
    component: () => import('@/views/LoginView.vue'),
}, {
    path: "/register",
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
}, {
    path: "/login",
    name: 'login',
    component: () => import('@/views/LoginView.vue')
}, {
    path: "/tickets",
    name: 'tickets',
    component: TicketList
}, {
    path: "/flights",
    name: 'flights',
    component: () => import('@/views/SearchFlightView.vue'),
}, {
    path: "/flights/create",
    name: 'create_flight',
    component: () => import('@/views/FlightCreateView.vue'),
    meta: {'role': 'supervisors'},
}]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL), routes
})

router.beforeEach((to, from, next) => {
    const user = store.state.auth.user;
    const groups = user?.groups;
    const requiresRole = to.meta.role;

    if (requiresRole && !groups.includes(requiresRole)) {
        next('/');
    } else {
        next();
    }
});

export default router
