<template>
  <div class="constant-info">
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="请输入名称" auto-complete="off" @keyup.enter.native="handleSearch" ><i slot="prefix" class="el-input__icon el-icon-search"></i></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="default" size="medium" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" @click="showAddDialog" :disabled="hasAddPermission">新增</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="danger" size="medium" @click="delAll">批量删除</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" @selection-change="handleSelectionChange" higlight-current-row>
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="name" label="键名"  sortable></el-table-column>
        <el-table-column property="value" label="键值" ></el-table-column>
        <el-table-column property="remark" label="备注"  :show-overflow-tooltip="true" ></el-table-column>
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
      <el-form :model="constantForm" ref="constantForm" :rules="rules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="constantForm.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="键名：" :label-width="formLabelWidth" prop="name">
          <el-input v-model="constantForm.name" placeholder="键名" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="键值：" :label-width="formLabelWidth" prop="value">
          <el-input v-model="constantForm.value" placeholder="键值"  auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="备注：" :label-width="formLabelWidth" prop="remark">
          <el-input v-model="constantForm.remark" placeholder="备注"  auto-complete="off"></el-input>
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
  import axios from '../../../utils/axiosConfig'
  import baseHost from '../../../api/baseHost'
  import ElRadio from "element-ui/packages/radio/src/radio";
  import hasPermission from "../../../utils/util";
  import ElFormItem from "element-ui/packages/form/src/form-item";
  export default {
    components: {
      ElFormItem,
      ElRadio},
    name: 'constant-info',
    inject: ['reload'],
    data: function(){
      return {
        multipleSelection: [],
        del_list: [],
        show: false,
        loading: false,
        total: 0,
        currentPage: 1,
        pageSize: 10,
        tableData: [],
        dialogTitle: null,
        constantForm: {
          id: null,
          name: '',
          value: '',
          remark: '',
        },
        rules:{
          name:[
            {required: true, trigger: 'blur', validator:this.validateConstantName}
          ],
        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          name: ''
        },
        hasAddPermission: hasPermission('add_constant'),
        hasDetailPermission: hasPermission('change_constant'),
        hasDeletePermission: hasPermission('delete_constant'),
      };
    },
    mounted(){

    },
    created(){
      this.initTable(this.currentPage, this.pageSize, this.filters.name);
    },
    watch: {

    },
    methods: {
      //校验用户名
      validateConstantName:function (rule, value, callback) {
        if(!value){
          return callback(new Error('请输入键名'));
        }
        let checkConstantNameUrl = baseHost + '/constant/checkConstantName/';
        let checkParams = {constantId:this.constantForm.id, constantName: value};
        axios.get(checkConstantNameUrl, {params: checkParams}).then((response)=>{
          if(response.data.code == 300){
            return callback(new Error(response.data.message));
          }else {
            return callback();
          }
        }).catch(()=>{
          return callback();
        });

      },

      initTable:function(current_page, page_size, constantName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/constant/constant/', {params:{page:current_page, page_size: page_size, constantName: constantName}, headers:{ 'Authorization':http_token}}).then((response)=>{
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
        this.dialogTitle = '详情';
        this.dialogAddVisible = true;
        this.constantForm = row;

      },
      handleDelete(index, row) {
        let that = this;
        let deleteConstantInfoUrl = baseHost + '/constant/constantdetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deleteConstantInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
            that.$message({
              type: 'success',
              message: '删除成功!'
            });
            that.initTable(that.currentPage, that.pageSize, this.filters.name);
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
        that.initTable(that.currentPage, that.pageSize, this.filters.name);
      },
      handleCurrentChange(val){
        let that = this;
        that.currentPage = val;
        that.initTable(that.currentPage, that.pageSize, this.filters.name);
      },
      showAddDialog(){
        this.dialogTitle = '新增';
        this.dialogAddVisible = true;
        this.constantForm = {};
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.constantForm = {};
        //清除验证
        let that = this;
        setTimeout(function () {
          that.$refs['constantForm'].clearValidate();
        }, 100);
      },
      trueSubmit:function () {
        let that = this;
        let addConstantInfoUrl = baseHost + '/constant/constant/';
        let editConstantInfoUrl = baseHost + '/constant/constantdetail/'+that.constantForm.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.constantForm;
        that.$refs['constantForm'].validate((valid) => {
          if (valid) {
            if(that.constantForm.id != null && that.constantForm.id != ''){
              let editParams = handleParams;
              axios.put(editConstantInfoUrl, JSON.stringify(editParams),{
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
                that.initTable(that.currentPage, that.pageSize, this.filters.name);
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
              axios.post(addConstantInfoUrl, JSON.stringify(addParams), {
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
                that.initTable(that.currentPage, that.pageSize, this.filters.name);

              }).catch(()=>{
                that.dialogAddVisible = false;
                this.$message({
                  type: 'fail',
                  message: '添加失败!'
                });

              });
            }
          }else {
            // alert('校验不通过');
          }
        });
      },
      delAll:function () {
        const length = this.multipleSelection.length;
        let str = '';
        this.del_list = this.del_list.concat(this.multipleSelection);
        for (let i = 0; i < length; i++) {
          str += this.multipleSelection[i].id + ',';
        }
        if(str != ''){
          str = str.substring(0, str.lastIndexOf(','));
        }else{
          this.$message.error('请勾选要删除的数据');
          return ;
        }
        this.$message.error('删除了' + str);
        this.multipleSelection = [];
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
    }
  }
</script>
