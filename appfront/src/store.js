import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookie'
Vue.use(Vuex)

const state = {
  topNavState: 'home',
  leftNavState: 'home',
  superUserRoleName: 'superUser',
  normalUserRoleName: 'normalUser',
  collapsed: false, // 左侧导航折叠状态
  isLogin:0, //判断是否登录, 0为未登录
  username: Cookie.get("username"),
  token: Cookie.get("token"),
}

const mutations = {
    saveToken:function (state, userToken) {
      state.username = userToken.username;
      state.token = userToken.token;
      Cookie.set("username", userToken.username, "20min");
      Cookie.set("token", userToken.token, "20min");
    },
  clearToken:function (state) {
    state.username = null;
    state.token = null;
    Cookie.delete("username");
    Cookie.delete("token");
  }
}

export default new Vuex.Store({
  state,
  mutations
})

