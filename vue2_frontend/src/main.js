import Vue from 'vue'
import App from './App.vue'
import router from './router'

// import ElementUI from 'element-ui'  //全部引入
// Vue.use(ElementUI)
import './plugins/element.js'  //部分引入
import axios from 'axios'
// import Vuex from 'vuex'

Vue.config.productionTip = false

Vue.prototype.$axios = axios

const baseURL = 'http://127.0.0.1:8000'  //django服务器地址
// 全局的 axios 默认值
axios.defaults.baseURL = baseURL

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
