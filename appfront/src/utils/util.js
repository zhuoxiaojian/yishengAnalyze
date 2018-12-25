/**
 * -*- coding: utf-8 -*-
 * @Time    : 2018/12/24 17:47
 * @Author  : zjj
 * @Email   : 1933860854@qq.com
 * @File    : util.js
 * @Software: PyCharm
 * 判断是否有权限，有权限返回false，无权限返回true
 */
export default function hasOpeartionPermission(operationName) {
  let user_permission = JSON.parse(localStorage.getItem('access-user')).currentUserRolePermissions;
  let user_role = localStorage.getItem('access-user-roleName');
  if("超级管理员" == user_role){
    return false;
  }else {
    if(null != user_permission){
      let str = user_permission.toString();
      if(str.indexOf(operationName) > -1){
        return false;
      }else {
        return true;
      }
    }else {
      return true;
    }
  }
}
