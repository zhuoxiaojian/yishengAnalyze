<template>
  <div>
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.username" placeholder="请输入用户名" auto-complete="off" @keyup.enter.native="handleSearch" ><i slot="prefix" class="el-input__icon el-icon-search"></i></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" @click="showAddDialog" :disabled="hasAddPermission">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" higlight-current-row>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="username" label="用户名"  sortable></el-table-column>
        <el-table-column property="password" label="密码"  :show-overflow-tooltip="true" v-if="show"></el-table-column>
        <el-table-column property="is_superuser" label="超级用户" :formatter="formatterIsSupersuer" v-if="show"></el-table-column>
        <el-table-column property="is_staff" label="职员状态" :formatter="formatterIsStaff" v-if="show"></el-table-column>
        <el-table-column property="is_active" label="是否有效" :formatter="formatterIsActive" v-if="show"></el-table-column>
        <el-table-column property="phone" label="手机" v-if="show"></el-table-column>
        <el-table-column property="qq" label="QQ" v-if="show"></el-table-column>
        <el-table-column property="email" label="邮箱" v-if="show"></el-table-column>
        <el-table-column property="first_name" label="姓氏"></el-table-column>
        <el-table-column property="last_name" label="名字"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleDetail(scope.$index, scope.row)" :disabled="hasDetailPermission">详情</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)" :disabled="hasDeletePermission">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                       :current-page="currentPage" :page-sizes="[10, 50, 100, 200]" :page-size="pageSize"
                       layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </el-col>
    </el-col>

    <el-dialog :title="dialogTitle" :close-on-press-escape="false" :close-on-click-modal="false" :visible.sync="dialogAddVisible" :before-close="handleClose">
      <el-form :model="form" ref="form" :rules="rules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="form.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="用户名：" :label-width="formLabelWidth" prop="username">
          <el-input v-model="form.username" placeholder="用户名" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码：" :label-width="formLabelWidth" prop="password">
          <el-input v-model="form.password" placeholder="密码" auto-complete="off" :readonly="isOnlyRead"></el-input>
        </el-form-item>
        <el-form-item label="状态：" :label-width="formLabelWidth">
          <el-checkbox label="管理员" v-model="form.is_superuser"></el-checkbox>
          <el-checkbox label="职员状态" v-model="form.is_staff"></el-checkbox>
          <el-checkbox label="账号有效" v-model="form.is_active"></el-checkbox>
        </el-form-item>

        <el-form-item label="姓氏：" :label-width="formLabelWidth" prop="first_name">
          <el-input v-model="form.first_name" placeholder="姓氏" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="名字：" :label-width="formLabelWidth" prop="last_name">
          <el-input v-model="form.last_name" placeholder="名字" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="QQ：" :label-width="formLabelWidth" prop="qq">
          <el-input v-model="form.qq" placeholder="QQ" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机：" :label-width="formLabelWidth" prop="phone">
          <el-input v-model="form.phone" placeholder="手机" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱：" :label-width="formLabelWidth" prop="email">
          <el-input v-model="form.email" placeholder="邮箱" auto-complete="off"></el-input>
        </el-form-item>
        <!--用户角色-->
        <el-form-item label="用户角色：" :label-width="formLabelWidth" v-if="roles.length>0" >
          <el-radio-group v-model="userRole" @change="onRadioChange">
            <!--<el-radio :label="3">备选项</el-radio>-->
            <!--<el-radio :label="6">备选项</el-radio>-->
            <!--<el-radio :label="9">备选项</el-radio>-->
            <el-radio :key="item.id" :label="item.id" v-for="item in roles">{{item.name}}</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="最后登录："  :label-width="formLabelWidth" prop="last_login">

            <el-date-picker
              v-model="form.last_login"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择日期">
            </el-date-picker>

        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="cancleSubmit">取消</el-button>
        <el-button type="primary" @click.native="trueSubmit">提交</el-button>
      </div>
    </el-dialog>

  </div>
</template>
<script>
  import axios from 'axios'
  import baseHost from '../../../api/baseHost'
  import ElRadio from "element-ui/packages/radio/src/radio";
  import ElButton from "element-ui/packages/button/src/button";
  import hasPermission from '../../../utils/util'
  export default {
    components: {
      ElButton,
      ElRadio},
    name: 'user-info',
    inject: ['reload'],
    data: function(){
      return {
        show: false,
        loading: false,
        total: 0,
        currentPage: 1,
        pageSize: 10,
        tableData: [],
        dialogTitle: null,
        isOnlyRead: false,
        form: {
          id: null,
          username: '',
          password: '',
          is_superuser: false,
          is_staff: true,
          is_active: false,
          qq:'',
          phone: '',
          email: '',
          first_name:'',
          last_name:'',
          last_login: new Date(),
        },
        rules:{
          username:[
            {required: true, trigger: 'blur', validator:this.validateUserName}
          ],
          password:[
            {required:true, message:'请输入密码', trigger:'blur'}
          ],
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
        userRole:null,
        roles:[],
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          username: ''
        },
        radio:'',
        hasAddPermission: hasPermission('add_userprofile'),
        hasDetailPermission: hasPermission('change_userprofile'),
        hasDeletePermission: hasPermission('delete_userprofile'),
      };
    },
    mounted(){
      let getAllRolesUrl = baseHost + '/role/getAllRoles/';
      let http_token = this.$store.state.token;
      axios.get(getAllRolesUrl, {headers:{ 'Authorization':http_token}}).then((response)=>{
        if(response.data){
          this.roles = JSON.parse(response.data.roleJson);
        }

      }).catch((error)=>{
         console.log('fail');
      });
      // console.log(this.$route.query.menuCode);
    },
    created(){
      this.initTable(this.currentPage, this.pageSize, this.filters.username);
    },
    watch: {

    },
    methods: {
      //校验用户名
      validateUserName:function (rule, value, callback) {
        let checkUserNameUrl = baseHost + '/user/checkUserName/';
        let checkParams = {userId:this.form.id, userName: value};
        if(!value){
          return callback(new Error('请输入用户名'));
        }else{
          let reg = /^[a-zA-Z0-9_-]{4,16}$/;
          if(!reg.test(value)){
            return callback(new Error('请输入4-16位由数字和字母组成的用户名'));
          }
        }
        axios.get(checkUserNameUrl, {params: checkParams}).then((response)=>{
          if(response.data.code == 300){
            // alert(response.data.message);
            return callback(new Error(response.data.message));
          }else {
            return callback();
          }
        }).catch(()=>{
          return callback();
        });

      },
      onRadioChange(item) {
        console.log("item", item);
      },
      initTable:function(current_page, page_size, userName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/user/users/', {params:{page:current_page, page_size: page_size, userName: userName}, headers:{ 'Authorization':http_token}}).then((response)=>{
          that.tableData = response.data.results;
          that.total = response.data.count;
        }).catch((error)=>{
          console.log(error.response.status);
          console.log("fail");
        })
      },
      handleSearch(){
        console.info(this.filters.username);
        this.initTable(this.currentPage, this.pageSize, this.filters.username)
      },
      handleDetail(index, row) {
        // console.log(index, row);
        // console.log(row.username);
        this.dialogTitle = '详情';
        this.dialogAddVisible = true;
        this.form = row;
        this.form.last_login = this.dateFormatter(row.last_login, true);
        this.isOnlyRead = true;
        let getUserOwnRoleUrl = baseHost + '/userRole/getUserOwnRole/';
        let http_token = this.$store.state.token;
        let checkParams = {checkUserId: row.id};
        axios.get(getUserOwnRoleUrl, {headers:{'Authorization':http_token}, params: checkParams}).then((response)=>{
           if(response.data.roleId != null){
               this.userRole = response.data.roleId;
           }
        }).catch(()=>{
        });

      },
      handleDelete(index, row) {
        console.log(index, row);
        let that = this;
        let deleteUserInfoUrl = baseHost + '/user/userdetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deleteUserInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
            that.$message({
              type: 'success',
              message: '删除成功!'
            });
            that.initTable(that.currentPage, that.pageSize, this.filters.username);
          }).catch(()=>{
            that.$message({
              type: 'fail',
              message: '删除失败!'
            });
          });
        }).catch(()=>{
          that.$message({
            type: 'fail',
            message: '删除失败!'
          });
        });


      },
      handleSizeChange(val){
        let that = this;
        that.pageSize = val;
        that.currentPage = 1;
        that.initTable(that.currentPage, that.pageSize, this.filters.username);
      },
      handleCurrentChange(val){
        let that = this;
        that.currentPage = val;
        that.initTable(that.currentPage, that.pageSize, this.filters.username);
      },
      showAddDialog(){
        this.dialogTitle = '新增';
        this.dialogAddVisible = true;
        this.form = {};
        this.form.last_login = this.dateFormatter(new Date(), true);
        this.userRole = null;
        this.isOnlyRead = false;
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      formatterIsSupersuer:function(row, column){
        if(column){
          return '是';
        }else{
          return '否';
        }
      },
      formatterIsStaff:function (row, column) {
        if(column){
          return '是';
        }else{
          return '否';
        }
      },
      formatterIsActive:function (row, column) {
        if(column){
          return '有效';
        }else{
          return '无效';
        }
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.form = {};
        this.userRole = null;
        this.isOnlyRead = false;
        //清除验证
        let that = this;
        setTimeout(function () {
          that.$refs['form'].clearValidate();
        }, 100);
      },
      trueSubmit:function () {
        let that = this;
        let addUserInfoUrl = baseHost + '/user/users/';
        let editUserInfoUrl = baseHost + '/user/userdetail/'+that.form.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.form;
        let userRoleParams = that.userRole;
        let extraParams = {};
        if(userRoleParams != null){
          extraParams.userRoleParams = userRoleParams;
        }else{
          extraParams.userRoleParams = null;
        }

        that.$refs['form'].validate((valid) => {
          if (valid) {
              if(that.form.id != null && that.form.id != ''){
                 let editParams = handleParams;
                 let editAllParams = {params: editParams, extraParams: extraParams};
                 // alert(JSON.stringify(editAllParams));
                 axios.put(editUserInfoUrl, JSON.stringify(editAllParams),{
                   headers: {
                     'Content-Type': 'application/json;charset=UTF-8',
                     'Authorization': http_token
                   }
                 }).then((response)=>{
                   that.dialogAddVisible = false;
                   this.$message({
                     type: 'success',
                     message: '修改成功!'
                   });
                   that.initTable(that.currentPage, that.pageSize, this.filters.username);
                 }).catch(()=>{
                   that.dialogAddVisible = false;
                   this.$message({
                     type: 'fail',
                     message: '修改失败!'
                   });
                 });
              }else{
                let addParams = handleParams;
                delete addParams['id'];
                let addAllParams = {params: addParams, extraParams: extraParams};
                axios.post(addUserInfoUrl, JSON.stringify(addAllParams), {
                  headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': http_token
                  }
                }).then((response)=>{
                  that.dialogAddVisible = false;
                  this.$message({
                    type: 'success',
                    message: '添加成功!'
                  });
                  that.initTable(that.currentPage, that.pageSize, this.filters.username);

                }).catch(()=>{
                  that.dialogAddVisible = false;
                  this.$message({
                    type: 'fail',
                    message: '添加失败!'
                  });

                });
              }
          }else {
            alert('校验不通过');
          }
        });
      },
      dateFormatter:function (str, flag) {
        var hasTime = flag != false ? true : false;//可传第二个参数false，返回yyyy-MM-dd
        console.log(typeof str);
        var d = new Date(str);
        var year = d.getFullYear();
        var month = (d.getMonth()+1)<10 ? '0'+(d.getMonth()+1) : (d.getMonth()+1);
        var day = d.getDate()<10 ? '0'+d.getDate() : d.getDate();
        var hour = d.getHours()<10 ? '0'+d.getHours() : d.getHours();
        var minute = d.getMinutes()<10 ? '0'+d.getMinutes() : d.getMinutes();
        var second = d.getSeconds()<10 ? '0'+d.getSeconds() : d.getSeconds();
        if(hasTime){
          return [year, month, day].join('-') + " " + [hour, minute, second].join(':');
        }else{
          return [year, month, day].join('-');
        }
      },
    }
  }
</script>
