/**
 * -*- coding: utf-8 -*-
 * @Time    : 2018/12/27 13:49
 * @Author  : zjj
 * @Email   : 1933860854@qq.com
 * @File    : axiosConfig.js
 * @Software: PyCharm
 */
import axios from 'axios'
import store from "../store";
import _this from "../router/index"
axios.interceptors.request.use(config => {
  config.headers.Authorization = store.state.token;
  return config;
},error => {
  return Promise.reject(error);
});
axios.interceptors.response.use(response =>{
  return response;
}, error => {
  if(error && error.response){

    switch (error.response.status){
      case 400:
        error.message = '请求错误'
        break
      case 401:
        error.message = '未授权，请登录'
        store.commit("clearToken");
        localStorage.removeItem('access-user');
        localStorage.removeItem('access-user-roleName');
        _this.push('/');
        break
      case 403:
        error.message = '拒绝访问'
        break
      case 404:
        error.message = `请求地址出错: ${error.response.config.url}`
        break
      case 408:
        error.message = '请求超时'
        break
      case 500:
        error.message = '服务器内部错误'
        break
      case 501:
        error.message = '服务未实现'
        break
      case 502:
        error.message = '网关错误'
        break
      case 503:
        error.message = '服务不可用'
        break
      case 504:
        error.message = '网关超时'
        break
      case 505:
        error.message = 'HTTP版本不受支持'
        break
      default:
    }
  }
  return Promise.reject(error);
});

axios.install = (Vue) => {
  Vue.prototype.axios = axios
}
export default axios
