// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'font-awesome/css/font-awesome.min.css'
//自己写的样式
import '@/assets/css/style.css'
import '@/assets/iconfont.css'
import store from './store'
// 注册element-ui
Vue.use(ElementUI)
Vue.component('footer-copyright', {
  template: '<p class="footer-msg">©CopyRight 2014-2016 广东原昇科技有限公司 版权所有 <a href="http://www.semyes.cn/" target="_blank">粤ICP备16061139号-2</a></p>'
});


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})

/*添加全局守卫，作用类似与中间件*/
router.beforeEach(function (to, from, next) {
  if(to.meta.requireAuth){
      if(store.state.token){
         next()
      }else{
        next({name: 'Login'});
      }
  }else{
    next()
  }
})
