import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from "@/views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import TicketList from "@/components/TicketList.vue";
import FlightList from "@/components/FlightList.vue";

const routes = [{
    path: '/', name: 'home', component: HomeView
}, {
    path: '/about', name: 'about', // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
}, {
    path: "/register", name: 'register', component: RegisterView
}, {
    path: "/login", name: 'login', component: LoginView
}, {
    path: "/tickets", name: 'tickets', component: TicketList
}, {
    path: "/flights", name: 'flights', component: FlightList
}
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL), routes
})

export default router
