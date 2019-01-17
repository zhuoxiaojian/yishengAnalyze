<template>
  <div>
  <el-row class="container">
    <!--头部-->
    <el-col :span="24" class="topbar-wrap">
      <div class="topbar-logo topbar-btn">
        <a href="#"><img src="../../assets/login/bigyishubao.png" style="padding-left:8px;"></a>
      </div>
      <div class="topbar-logos">
        <a href="#" style="color: #fff;">易数宝大数据分析平台</a>
      </div>
      <div class="topbar-account topbar-btn">
        <el-dropdown trigger="click">
             <!-- 全屏显示 -->
                <div class="btn-fullscreen" @click="handleFullScreen">
                    <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">
                        <i class="el-icon-rank"></i>
                    </el-tooltip>
                </div>
        </el-dropdown>
        <el-dropdown trigger="click">
          <!-- 消息中心 -->
                <div class="btn-bell">
                    <el-tooltip effect="dark" :content="messageCount?`有${messageCount}条未读消息`:`消息中心`" placement="bottom">
                        <router-link to="/appfront/Demo/TabsInfo">
                            <i class="el-icon-bell"></i>
                        </router-link>
                    </el-tooltip>
                    <span class="btn-bell-badge" v-if="messageCount"></span>
                </div>
        </el-dropdown>
        <el-dropdown trigger="click">
          <span class="el-dropdown-link userinfo-inner">
            <i class="iconfont icon-user"></i> {{roleName}}-{{nickname}}   <i class="el-icon-caret-bottom"></i></span>
          <el-dropdown-menu slot="dropdown">
         <el-dropdown-item>
              <div @click="showUserInfoDialog"><span style="color: #555;font-size: 14px;">个人信息</span></div>
            </el-dropdown-item>
            <el-dropdown-item>
              <div @click="showPassInfoDialog"><span style="color: #555;font-size: 14px;">修改密码</span></div>
            </el-dropdown-item>
            <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
  </el-row>
  <el-dialog
    title="个人信息"
    :visible.sync="showUserInfoDialogVisible"
    width="30%"
    @close='closeShowUserInfoDialogDialog'>
    <el-form :model="userInfoForm" ref="userInfoForm" :rules="userInfoFormRules">
      <el-form-item prop="id" :label-width="formLabelWidth" label="ID：" hidden="true">
        <el-input v-model="userInfoForm.id"></el-input>
      </el-form-item>
        <el-form-item prop="username" :label-width="formLabelWidth" label="账号：">
          <el-input v-model="userInfoForm.username"  auto-complete="off" placeholder="账号" readonly></el-input>
        </el-form-item>
      <el-form-item prop="first_name" :label-width="formLabelWidth" label="姓氏：">
        <el-input v-model="userInfoForm.first_name" auto-complete="off" placeholder="姓氏"></el-input>
      </el-form-item>
      <el-form-item prop="last_name" :label-width="formLabelWidth" label="名字：">
        <el-input v-model="userInfoForm.last_name" auto-complete="off" placeholder="名字"></el-input>
      </el-form-item>
      <el-form-item prop="phone" :label-width="formLabelWidth" label="手机：">
        <el-input v-model="userInfoForm.phone" auto-complete="off" placeholder="手机"></el-input>
      </el-form-item>
      <el-form-item prop="qq" :label-width="formLabelWidth" label="QQ：">
        <el-input v-model="userInfoForm.qq" auto-complete="off" placeholder="QQ" ></el-input>
      </el-form-item>
      <el-form-item prop="email" :label-width="formLabelWidth" label="邮箱：">
        <el-input v-model="userInfoForm.email" auto-complete="off" placeholder="邮箱"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
       <el-button @click="closeShowUserInfoDialogDialog">取 消</el-button>
       <el-button type="primary" @click="submitUserInfoDialog" :disabled="hasDetailPermission">确 定</el-button>
     </div>
  </el-dialog>

    <el-dialog
      title="修改密码"
      :visible.sync="showPasswordDialogVisible"
      width="30%"
      @close='closeShowPasswordInfoDialogDialog'>
      <el-form :model="passwordInfoForm" ref="passwordInfoForm" :rules="passwordInfoFormRules">
        <el-form-item prop="id" :label-width="formLabelWidth" label="ID：" hidden="true">
          <el-input v-model="passwordInfoForm.id"></el-input>
        </el-form-item>
        <el-form-item prop="oldPassword" :label-width="formLabelWidth" label="旧密码：">
          <el-input v-model="passwordInfoForm.oldPassword" auto-complete="off" placeholder="请输入旧密码" type="password"></el-input>
        </el-form-item>
        <el-form-item prop="newPassword" :label-width="formLabelWidth" label="新密码：">
          <el-input v-model="passwordInfoForm.newPassword" auto-complete="off" placeholder="请输入新密码" type="password"></el-input>
        </el-form-item>
        <el-form-item prop="firstPassword" :label-width="formLabelWidth" label="新密码：">
          <el-input v-model="passwordInfoForm.firstPassword" auto-complete="off" placeholder="请重新输入新密码" type="password"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeShowPasswordInfoDialogDialog">取 消</el-button>
        <el-button type="primary" @click="submitPasswordInfoDialog">确 定</el-button>
      </div>
    </el-dialog>


  </div>
</template>
<script>
  import 'element-ui/lib/theme-chalk/display.css';
  import axios from '../../utils/axiosConfig'
  import baseHost from '../../api/baseHost'
  import ElFormItem from "element-ui/packages/form/src/form-item";
  import ElInput from "element-ui/packages/input/src/input";
  import hasPermission from "../../utils/util"
  export default {
    components: {
      ElInput,
      ElFormItem},
    data(){
      return {
        fullscreen: false,
        loading: false,
        nickname: '',
        roleName: '',
        messageCount: null,
        formLabelWidth: '80px',
        showUserInfoDialogVisible: false,
        showPasswordDialogVisible: false,
        userInfoForm:{
          id:'',
          username:'',
          first_name:'',
          last_name:'',
          phone:'',
          qq:'',
          email:''
        },
        userInfoFormRules:{
          phone:[
            {pattern:/^(13[0-9]{9})|(18[0-9]{9})|(14[0-9]{9})|(17[0-9]{9})|(15[0-9]{9})|((19[8|9])\d{8})$/, message:'手机号格式错误', trigger:'blur'}
          ],
          qq:[
            {pattern:/^\d{4,10}$/, message:'QQ号格式错误', trigger:'blur'}
          ],
          email:[
            {pattern:/^\w+@\w+\.\w+(\.\w+)*$/, message:'邮箱格式错误', trigger:'blur'}
          ]
        },
        passwordInfoForm:{
          id:'',
          oldPassword:'',
          newPassword:'',
          firstPassword:''
        },
        passwordInfoFormRules:{
          oldPassword:[{required:true, trigger:'blur', validator: this.validateOldPassword}],
          newPassword:[{required:true, message:'请输入新密码', trigger:'blur'}],
          firstPassword:[{required:true, message:'请重新输入新密码', trigger:'blur'}]
        },
        hasDetailPermission: hasPermission('change_userprofile'),
      }
    },
    mounted() {
      let user = localStorage.getItem('access-user');
      let user_role_name = localStorage.getItem('access-user-roleName');
      if(user != null){
        let user_json = JSON.parse(user);
        this.nickname = user_json.username;
        if(user_role_name != null){
          this.roleName = user_role_name;
        }else {
          this.roleName = '游客'
        }
      }else {
        this.$router.push('/');
      }
      let token = this.$store.state.token;
      if(token == null){
        this.$router.push('/');
      }else{
        let checkUsrTokenUrl = baseHost + '/user/checkUserToken/';
        axios.get(checkUsrTokenUrl,{headers:{ 'Authorization':token}}).then((response)=>{
            if(response.data.code == 300){
              this.$router.push('/');
            }
          }).catch((error)=>{
            this.$router.push('/');
          });
      }
      //获取未读消息总数
      let getMessageCountUrl = baseHost + '/systemMessage/getSystemMessage/';
      let that = this;
      axios.get(getMessageCountUrl, {params: {flagParams: '0,1'}}).then((response)=>{
        let json_list = response.data.resultData; //list集合
        for(let i=0; i < json_list.length; i++){
          if(json_list[i].hasOwnProperty('flag0')){
             that.messageCount = json_list[i].flag0.flag0Count;
             break;
          }
        }

      }).catch(()=>{

      });
    },
    created(){
      
    },
    watch:{

    },
    methods: {
      //校验旧密码是否正确
      validateOldPassword:function (rule, value, callback) {
        let that = this;
        let checkUserPasswordUrl = baseHost + '/user/checkOrChangeUserPassword/'+ that.passwordInfoForm.id+'/';
        let oldPasswordParam = {oldPassword: value};
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        if(!value){
          return callback(new Error('请输入旧密码'));
        }else {
            axios.get(checkUserPasswordUrl,
              {
                params:oldPasswordParam,
                headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': http_token
              }}).then((response)=>{
                  if(response.data.code != 200){
                    return callback(new Error(response.data.message));
                  }
            }).catch(()=>{
                return callback();
            });
        }
      },
      jumpTo (url){
        this.$router.push(url); //用go刷新
      },
      logout(){
        //logout
        let that = this;

        this.$confirm('确认退出吗?', '提示', {
          confirmButtonClass: 'el-button--warning'
        }).then(() => {
          //确认
          let logoutURL = baseHost+'/user/appfrontLogout';
          let token = that.$store.state.token;
          axios.get(logoutURL, {headers:{ 'Authorization':token}}).then((response)=>{
              if(response.data.code == '0'){
                that.$store.commit("clearToken");
                localStorage.removeItem('access-user');
                localStorage.removeItem('access-user-roleName');
                that.$router.push('/');
              }
          }).catch();

        }).catch(() => {});
      },
      showUserInfoDialog:function () {
        this.showUserInfoDialogVisible = true;
        let user = localStorage.getItem('access-user');
        if(null == user){
          this.$router.push('/');
        }else{
          this.userInfoForm = JSON.parse(user);
        }

      },
      closeShowUserInfoDialogDialog:function () {
        this.showUserInfoDialogVisible = false;
      },
      submitUserInfoDialog:function () {
        let that = this;
        let http_token = that.$store.state.token;
        let submitUserInfoUrl = baseHost + '/user/userdetail/'+that.userInfoForm.id+'/';
        let params = that.userInfoForm;
        let editAllParams = {params: params};
        axios.put(submitUserInfoUrl, JSON.stringify(editAllParams),
          {headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': http_token
          }}).then(()=>{
          that.showUserInfoDialogVisible = false;
          that.$message({
            type: 'success',
            message: '修改成功!'
          });

        }).catch(()=>{
          that.$message({
            type: 'fail',
            message: '修改失败!'
          });
        });

      },
      showPassInfoDialog:function () {
        this.showPasswordDialogVisible = true;
        let user = localStorage.getItem('access-user');
        if(null != user){
          this.passwordInfoForm.id = JSON.parse(user).id;
        }else {
          this.$router.push('/');
        }
      },
      closeShowPasswordInfoDialogDialog:function(){
        let that = this;
        that.showPasswordDialogVisible = false;
        setTimeout(function () {
          that.$refs['passwordInfoForm'].clearValidate();
        }, 100);
        that.passwordInfoForm = {}
      },
      submitPasswordInfoDialog:function () {
        let that = this;
        let changeUserOwnPasswordUrl = baseHost + '/user/checkOrChangeUserPassword/'+ that.passwordInfoForm.id+'/';
        let passwordParam = {newPassword: that.passwordInfoForm.newPassword, firstPassword: that.passwordInfoForm.firstPassword};
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        that.$refs['passwordInfoForm'].validate((valid)=>{
            if(valid){
              if(that.passwordInfoForm.newPassword != that.passwordInfoForm.firstPassword){
                alert('新密码不一致，请重新输入');
                return;
              }
              axios.put(changeUserOwnPasswordUrl, JSON.stringify(passwordParam), {
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': http_token
                }
              }).then((response)=>{
                  if(response.data.code == 200){
                    alert(response.data.message);
                    that.$router.push('/');
                  }else{
                    alert(response.data.message);
                  }
              }).catch();
            }
          });
      },
      handleFullScreen(){
        let element = document.documentElement;
          if (this.fullscreen) {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitCancelFullScreen) {
                        document.webkitCancelFullScreen();
                } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                }
          } else {
                if (element.requestFullscreen) {
                    element.requestFullscreen();
                } else if (element.webkitRequestFullScreen) {
                    element.webkitRequestFullScreen();
                } else if (element.mozRequestFullScreen) {
                    element.mozRequestFullScreen();
                } else if (element.msRequestFullscreen) {
                    // IE11
                    element.msRequestFullscreen();
                }
              }
        this.fullscreen = !this.fullscreen;    
      },
    }
  }
</script>
<style scoped>
  .btn-bell-badge{
        position: absolute;
        right: 0;
        top: 15px;
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background: #f56c6c;
        color: #fff;
    }
    .btn-bell .el-icon-bell{
        color: #fff;
    }
    .btn-fullscreen .el-icon-rank{
      color: #fff;
    }
    .btn-fullscreen{
      margin-right: 10px;
    }
     
</style>