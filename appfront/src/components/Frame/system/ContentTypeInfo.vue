<template>
  <div class="content-type-info">
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="请输入实体" auto-complete="off" @keyup.enter.native="handleSearch" ><i slot="prefix" class="el-input__icon el-icon-search"></i></el-input>
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
        <el-table-column property="model" label="实体" ></el-table-column>
        <el-table-column property="app_label" label="名称"  sortable></el-table-column>
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
      <el-form :model="contentTypeForm" ref="contentTypeForm" :rules="rules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="contentTypeForm.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="名称：" :label-width="formLabelWidth" prop="app_label">
          <el-input v-model="contentTypeForm.app_label" placeholder="名称" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="实体：" :label-width="formLabelWidth" prop="model">
          <el-input v-model="contentTypeForm.model" placeholder="键值"  auto-complete="off"></el-input>
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
  import hasPermission from "../../../utils/util";
  export default {
    components: {ElRadio},
    name: 'content-type-info',
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
        contentTypeForm: {
          id: null,
          app_label: '',
          model: '',
        },
        rules:{
          app_label:[
            {required: true, trigger: 'blur', message:'请输入app_label'}
          ],
          model:[
            {required: true, trigger: 'blur', message: '请输入实体'}
          ]
        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          name: ''
        },
        hasAddPermission: hasPermission('add_contenttype'),
        hasDetailPermission: hasPermission('change_contenttype'),
        hasDeletePermission: hasPermission('delete_contenttype'),
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
      initTable:function(current_page, page_size, contentTypeName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/contentType/contentType/', {params:{page:current_page, page_size: page_size, contentTypeName: contentTypeName}, headers:{ 'Authorization':http_token}}).then((response)=>{
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
        this.contentTypeForm = row;

      },
      handleDelete(index, row) {
        let that = this;
        let deleteContentTypeInfoUrl = baseHost + '/contentType/contentTypeDetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deleteContentTypeInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
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
        this.contentTypeForm = {};
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.contentTypeForm = {};
      },
      trueSubmit:function () {
        let that = this;
        let addContentTypeInfoUrl = baseHost + '/contentType/contentType/';
        let editContentTypeInfoUrl = baseHost + '/contentType/contentTypeDetail/'+that.contentTypeForm.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.contentTypeForm;
        that.$refs['contentTypeForm'].validate((valid) => {
          if (valid) {
            if(that.contentTypeForm.id != null && that.contentTypeForm.id != ''){
              let editParams = handleParams;
              axios.put(editContentTypeInfoUrl, JSON.stringify(editParams),{
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
              axios.post(addContentTypeInfoUrl, JSON.stringify(addParams), {
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

    }
  }
</script>
