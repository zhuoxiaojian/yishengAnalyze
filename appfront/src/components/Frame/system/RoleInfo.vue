<template>
  <div>
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="请输入角色名称" auto-complete="off" @keyup.enter.native="handleSearch"><i slot="prefix" class="el-input__icon el-icon-search"></i></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" @click="showAddDialog">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" ></el-table-column>
        <el-table-column prop="name" label="名称" width="180" sortable></el-table-column>
        <!--<el-table-column label="所属部门" :formatter="formatterColumn" ></el-table-column>-->
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleDetail(scope.$index, scope.row)">详情</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
        <el-form-item label="ID" hidden="true" prop="id"  :label-width="formLabelWidth">
          <el-input  v-model="form.id" auto-complete="off" ></el-input>
        </el-form-item>
        <el-form-item label="名称：" :label-width="formLabelWidth" prop="name">
          <el-input v-model="form.name" placeholder="名称" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <el-form :model="depart">
        <el-form-item label="部门ID:" hidden="true"  prop="departId"  :label-width="formLabelWidth">
          <el-input  v-model="depart.departId" auto-complete="off" ></el-input>
        </el-form-item>
        <el-form-item label="所属部门：" :label-width="formLabelWidth" prop="departName">
          <el-input  placeholder="所属部门" v-model="departName" auto-complete="off" @click.native="selectDepart" style="background-color: #6b7879"></el-input>
        </el-form-item>
      </el-form>

      <el-form>
        <el-form-item label="菜单权限：" :label-width="formLabelWidth">
          <el-tree
            ref="roleMenuTreeRef"
            node-key="id"
            :data="roleMenuTree"
            :props="roleMenuProps"
            @node-click="handleRoleMenuTreeNodeClick"
            show-checkbox
            @check-change="handleRoleMenuTreeCheckChange"
            default-expand-all
          ></el-tree>
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="功能权限：" :label-width="formLabelWidth">
          <el-select v-model="choosePermissions" multiple coolapse-tags placeholder="请选择" style="width: 100%; border-radius: 20px;" @change="selectAllPermission">
            <el-option v-for="item in selectPermissionOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="cancleSubmit">取消</el-button>
        <el-button type="primary" @click.native="editFormSubmit">提交</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="部门树"
      :visible.sync="dialogTreeVisible"
      width="30%"
      @close='closeTreeDialog'>
      <el-tree :data="myDepartTree"
               :props="defaultProps"
               @node-click="handleNodeClick"
               :default-checked-keys="resourceCheckedKey"
      ></el-tree>
      <!--
                 show-checkbox
                @check-change="handleCheckChange"
      <div slot="footer" class="dialog-footer">
         <el-button @click="cancelTreeModel">取 消</el-button>
         <el-button type="primary" @click="trueTreeModel">确 定</el-button>
       </div>
       -->
    </el-dialog>
  </div>
</template>
<script>
  import axios from 'axios'
  import baseHost from '../../../api/baseHost'
  import ElFormItem from "element-ui/packages/form/src/form-item";
  import ElForm from "element-ui/packages/form/src/form";
  import ElTree from "element-ui/packages/tree/src/tree";
  import ElOption from "element-ui/packages/select/src/option";
  export default {
    components: {
      ElOption,
      ElTree,
      ElForm,
      ElFormItem},
    name: 'role-info',
    inject: ['reload'],
    data: function(){
      return {
        dialogTitle: '',
        loading: false,
        radio: '1',
        total: 0,
        currentPage: 1,
        pageSize: 10,
        tableData: [],
        form: {
          id: null,
          name: '',
        },
        rules:{
          name:[
            {required: true, trigger: 'blur', validator:this.validateRoleName}
          ],
        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          name: ''
        },
        myDepartTree:[],
        defaultProps: {
          children: 'children',
          label: 'name'
        },
        roleMenuTree:[],
        roleMenuProps:{
          children: 'children',
          label: 'name'
        },
        dialogTreeVisible: false,
        depart: {
          departId: null,
        },
        departName: null,
        resourceCheckedKey: [],
        choosePermissions:[],
        selectPermissionOptions: []
      };
    },
    mounted(){
      let departURL = baseHost+'/depart/initDepartTree';
      let that = this;
      let http_token = that.$store.state.token;
      axios.get(departURL, {headers:{ 'Authorization':http_token}}).then((response)=>{
        let data = response.data.message;
        that.myDepartTree = data;
      }).catch(()=>{
        console.log("请求失败");
      });
      let menuURL = baseHost+'/menu/initMenuTree';
      axios.get(menuURL, {headers:{ 'Authorization':http_token}}).then((response)=>{
        let data = response.data.message;
        that.roleMenuTree = data;
      }).catch(()=>{
        console.log("请求失败");
      });

      let getAllPermissonUrl = baseHost + '/permissions/getAllPermission/';
      axios.get(getAllPermissonUrl, {headers:{ 'Authorization':http_token}}).then((response)=>{
          that.selectPermissionOptions = JSON.parse(response.data.permissionJson);
      }).catch(()=>{
        console.log("请求失败");
      });

    },
    created(){
      this.initTable(this.currentPage, this.pageSize, null);
    },
    methods: {
      validateRoleName:function (rule, value, callback) {
        let checkRoleNameUrl = baseHost + '/role/checkRoleName/';
        let checkParams = {roleId:this.form.id, roleName: value};
        if(!value){
          return callback(new Error('请输入名称'));
        }
        axios.get(checkRoleNameUrl, {params: checkParams}).then((response)=>{
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
      initTable:function(current_page, page_size, roleName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/role/role/', {params:{page:current_page, page_size: page_size, roleName: roleName}, headers:{ 'Authorization':http_token}}).then((response)=>{
          that.tableData = response.data.results;
          that.total = response.data.count;

        }).catch(function () {
          console.log("fail");
        })
      },
      handleSearch(){
        console.info(this.filters.name);
        this.initTable(this.currentPage, this.pageSize, this.filters.name)
      },
      handleDetail(index, row) {
        let that = this;
        //开始赋值啦啦啦
        let getUrl = baseHost + '/role/initRoleEditValue/';
        let params = {queryRoleId: row.id};
        let http_token = that.$store.state.token;
        axios.get(getUrl, {headers:{'Authorization':http_token}, params: params}).then((response)=>{
          // console.log(response.data.menuKey);
          if(response.data.departKey){
            that.depart.departId = response.data.departKey;
          }
          if(response.data.departName){
            that.departName = response.data.departName;
          }
          if(response.data.menuKey.length > 0){
            that.editCheckedTree(response.data.menuKey);
            // console.log('赋值完毕');
          }

          that.choosePermissions = response.data.rolePermissions;


        }).catch((response)=>{
          console.log(response);
        });
        that.form = row;
        that.dialogAddVisible = true;
        that.dialogTitle = '编辑';
      },
      handleDelete(index, row) {
        let that = this;
        let deletURL = baseHost+'/role/roledetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deletURL, {headers:{'Authorization':http_token}}).then(()=>{
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
            that.initTable(that.currentPage, that.pageSize, null);
          }).catch(()=>{
            this.$message({
              type: 'fail',
              message: '删除失败!'
            });
          })
        }).catch(()=>{
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },
      handleSizeChange(val){
        let that = this;
        that.pageSize = val;
        that.currentPage = 1;
        that.initTable(that.currentPage, that.pageSize, null);
      },
      handleCurrentChange(val){
        let that = this;
        that.currentPage = val;
        that.initTable(that.currentPage, that.pageSize, null);
      },
      showAddDialog(){
        let that = this;
        that.dialogAddVisible = true;
        that.dialogTitle = '添加';
        that.form = {};
        that.depart = {};
        that.departName=null;
        that.addCheckedTree();
        that.choosePermissions = [];
      },
      editCheckedTree(array){
        let that = this;
        if(that.$refs.roleMenuTreeRef){
          that.$refs.roleMenuTreeRef.setCheckedKeys([]);
          that.$refs.roleMenuTreeRef.setCheckedKeys(array);
        }else{
          setTimeout(function () {
              that.editCheckedTree(array);
          }, 500)
        }

      },
      addCheckedTree(){
        let that = this;
        if(that.$refs.roleMenuTreeRef){
          that.$refs.roleMenuTreeRef.setCheckedKeys([]);
        }else{
          setTimeout(function () {
            that.addCheckedTree();
          }, 500)
        }
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit(){
        let that = this;
        that.dialogAddVisible = false;
        that.form = {};
        that.depart = {};
        that.departName=null;
        that.addCheckedTree();
        that.choosePermissions = [];
      },
      editFormSubmit(){
        let that = this;
        // console.log(this.$refs.roleMenuTreeRef.getCheckedKeys());
        let permissionsKey = that.choosePermissions;
        let menuKey = that.$refs.roleMenuTreeRef.getCheckedKeys();
        let departKey = that.depart.departId;
        let extraParams = {};
        // console.log(this.$refs.roleMenuTreeRef.getCheckedNodes());
        let menuNodes = that.$refs.roleMenuTreeRef.getCheckedNodes();
        let menuData = new Set(menuKey);
        for(let menu in menuNodes){
          if(menuNodes[menu].parentId != null){
            menuData.add(menuNodes[menu].parentId);
          }
        }
        extraParams.menuKey = Array.from(menuData);
        if(departKey != null){
          extraParams.departKey = departKey;
        }else{
          extraParams.departKey = null;
        }
        if(permissionsKey != null){
          extraParams.permissionsKey = permissionsKey;
        }else{
          extraParams.permissionsKey = null;
        }
        that.$refs['form'].validate((valid) => {
          if (valid) {
            let http_token = that.$store.state.token;
            let params = {};
            axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';


            if (that.form.id != null && that.form.id != "") {
              let editURL = baseHost + "/role/roledetail/" + that.form.id + "/";
              params.id = that.form.id;
              params.name = that.form.name;
              let allParams = {params: params, extraParams: extraParams};
              axios.put(editURL, JSON.stringify(allParams), {
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': http_token
                }
              })
                .then(() => {
                  that.dialogAddVisible = false;
                  that.$message({
                    type: 'success',
                    message: '修改成功!'
                  });
                  // that.reload();
                  that.initTable(that.currentPage, that.pageSize, null);
                }).catch(() => {
                that.dialogAddVisible = false;
                that.$message({
                  type: 'fail',
                  message: '修改失败!'
                });
                that.initTable(that.currentPage, that.pageSize, null);
              })

            } else {
              let addURL = baseHost + "/role/role/";
              params.name = that.form.name;
              let allParams = {params: params, extraParams: extraParams};
              axios.post(addURL, JSON.stringify(allParams), {
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': http_token
                }
              })
                .then(() => {
                  that.dialogAddVisible = false;
                  that.$message({
                    type: 'success',
                    message: '添加成功!'
                  });
                  that.initTable(that.currentPage, that.pageSize, null);
                }).catch(() => {
                that.dialogAddVisible = false;
                that.$message({
                  type: 'fail',
                  message: '添加失败!'
                });
              })
            }
          }else{

          }});
      },
      selectDepart(){
        this.dialogTreeVisible = true;
      },
      handleNodeClick(data) {
        // console.log(JSON.stringify(data));
        this.departName = data.name;
        this.depart.departId = data.id;

      },
      handleRoleMenuTreeNodeClick(data){
        // console.log(data);
        // const newChild = { id: 100, name: 'testtest', children: [] };
        // if (!data.children) {
        //   this.$set(data, 'children', []);
        // }
        // data.children.push(newChild);
      },
      handleRoleMenuTreeCheckChange(data, checked, indeterminate){
        // console.log(data, checked, indeterminate);
        // if(checked){
        //   console.log(data.name);
        // }
      },
      closeTreeDialog(){
        this.dialogTreeVisible = false;

        //window.location.reload();
      },
      selectAllPermission(val){
        let that = this;
        that.choosePermissions = val;
      }
    }
  }
</script>
