import Vue from 'vue'
import VueRouter from 'vue-router'
import Manager from '@/components/Manager'
import Login from '@/components/Login'
import Tenant from '@/components/Tenant'
import Waiter from '@/components/Waiter'

Vue.use(VueRouter)

const routes = [{
		path: '/',
		name: 'home',
		component: Login,
	},
	{
		path: '/login',
		name: 'login',
		component: Login,
	},
	{
		path: '/manager',
		name: "manager",
		component: Manager,
		props: {
			username: ''
		},
	},
	{
		path: '/waiter',
		name: "waiter",
		component: Waiter,
		props: {
			username: ''
		},
		children: [{
				path: 'openRoom',
				name:'openRoom',
				component: () => import(/* webpackChunkName: "home" */ '@/components/Manager/OpenRoom.vue'),
			},
			{
				path: 'closeRoom',
				name:'closeRoom',
				component: () => import(/* webpackChunkName: "home" */ '@/components/Manager/CloseRoom.vue'),
			},
		]
	},
	{
		path: '/tenant',
		name: "tenant",
		component: Tenant,
		props: {
			username: '',
			room_id: ''
		},
	}
	// {
	//   path: '/about',
	//   name: 'About',
	//   // route level code-splitting
	//   // this generates a separate chunk (about.[hash].js) for this route
	//   // which is lazy-loaded when the route is visited.
	//   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
	// }
]

const router = new VueRouter({
	routes
})
const originalPush = VueRouter.prototype.push
   VueRouter.prototype.push = function push(location) {
   return originalPush.call(this, location).catch(err => err)
}
export default router
