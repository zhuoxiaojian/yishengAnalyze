<template>
  <div id="loginBox" >
    <el-form :model="account" :rules="rules" ref="account">
      <el-form-item>
        <img src="../../assets/login/bigyishubao.png" width="18%" height="18%">
      </el-form-item>
      <el-form-item>
        <h2 style="text-align: center" class="myTitle">易数宝大数据分析平台</h2>
      </el-form-item>
      <el-form-item prop="name">
        <el-input id="name" v-model="account.name" placeholder="请输入帐号" auto-complete="off">
          <template slot="prepend"><i class="fa fa-user fa-fw"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input id="password" v-model="account.password" type="password" placeholder="请输入密码" auto-complete="off">
          <template slot="prepend"><i class="fa fa-lock fa-fw"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button id="login" v-on:click="check('account')" style="width:100%" type="primary">登录</el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
  import axios from 'axios'
  import * as appfrontLoginAPI from '@/api/appfrontLoginAPI'
  import * as constant from '@/utils/constant'
  import ElForm from "element-ui/packages/form/src/form";
  import ElFormItem from "element-ui/packages/form/src/form-item";
  import { setCookie } from '@/utils/cookie'
  import {getCookie} from "../../utils/cookie";
  export default {
    components: {
      ElFormItem,
      ElForm},
    name: 'Login',
    data(){
      return {
        account: {
          name: "root",
          password: "root123456"
        },
        rules:{
          name:[
            {required: true, message: '请输入用户名', trigger: 'blur'}
          ],
          password:[
            {required: true, message: '请输入密码', trigger: 'blur'}
          ]
        }
      };
    },
    computed: {},
    watch: {},
    methods:{
      check(formName){
        let that = this;

        that.$refs[formName].validate((valid) =>{
          if(valid){
            let params = {username: that.account.name, password: that.account.password};
            let url = appfrontLoginAPI.appfrontLoginAPI;
            axios.post(url, JSON.stringify(params),{headers:{ 'Content-Type': 'application/json;charset=UTF-8'}}).then((response) => {
              if(response.data.code == '0'){
                let user_token = response.data.user_token;
                let user_info = response.data.userInfo;
                let role_name = response.data.user_role;
                localStorage.setItem('access-user', JSON.stringify(user_info));
                localStorage.setItem('access-user-roleName', role_name);
                that.$store.commit('saveToken', {token:user_token, username: that.account.name});
                that.$router.push({path: '/appfront/Home'});
              }else {
                alert(response.data.message);
              }
            }).catch(function (response) {
              console.log(response);
            });
          } else{
            console.log('error submit!!');
          }
        })
      },
    },

  }
</script>

<style scoped>
  .el-form-item{
    margin: 20px;
  }
  .myTitle{
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: 500;
    line-height: 1.1;
    color: inherit;
  }
  #loginBox {
    text-align: center; /*让div内部文字居中*/
    background-color: #F8F8F8;
    border-radius: 20px;
    width:350px;
    height:380px;
    position:absolute;
    left:50%;
    top:20%;
    margin:-75px 0 0 -135px;
  }
</style>
