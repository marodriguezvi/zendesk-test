import Vue from 'vue'
import App from './App.vue'
import VueResource from 'vue-resource'
import './registerServiceWorker'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

Vue.config.productionTip = false
Vue.use(VueResource)

new Vue({
  render: h => h(App)
}).$mount('#app')
