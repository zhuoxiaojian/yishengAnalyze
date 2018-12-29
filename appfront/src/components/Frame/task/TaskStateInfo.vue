<template>
  <div class="task-state-info">
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="请输入名称" auto-complete="off" @keyup.enter.native="handleSearch" ><i slot="prefix" class="el-input__icon el-icon-search"></i></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="default" size="medium" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" higlight-current-row>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="name" label="名称"  ></el-table-column>
        <el-table-column property="task_id" label="任务ID" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column property="state" label="状态"  ></el-table-column>
        <el-table-column property="runtime" label="执行时长" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column property="tstamp" label="运行时间"
                         :formatter="dateFormat" sortable></el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                       :current-page="currentPage" :page-sizes="[10, 50, 100, 200]" :page-size="pageSize"
                       layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </el-col>
    </el-col>
  </div>
</template>
<script>
  import axios from '../../../utils/axiosConfig'
  import baseHost from '../../../api/baseHost'
  import ElRadio from "element-ui/packages/radio/src/radio";
  import hasPermission from "../../../utils/util";
  export default {
    components: {ElRadio},
    name: 'task-state-info',
    inject: ['reload'],
    data: function(){
      return {

        show: false,
        loading: false,
        total: 0,
        currentPage: 1,
        pageSize: 10,
        tableData: [],
        filters: {
          name: ''
        },
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
      dateFormat(row, column){
        if(row.tstamp == null){
          return '';
        }
        let time = new Date(row.tstamp);
        return `${time.getFullYear()}-${time.getMonth() + 1 >= 10 ? (time.getMonth() + 1) : '0' + (time.getMonth() + 1)}-${time.getDate() >= 10 ? time.getDate() : '0' + time.getDate()}
                     ${time.getHours() >= 10 ? time.getHours() : '0' + time.getHours()} : ${time.getMinutes()>=10?time.getMinutes():'0'+time.getMinutes()} : ${time.getSeconds() >= 10 ? time.getSeconds() : '0' + time.getSeconds()}`;
      },
      initTable:function(current_page, page_size, taskStateName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/systemTask/taskState/', {params:{page:current_page, page_size: page_size, taskStateName: taskStateName}, headers:{ 'Authorization':http_token}}).then((response)=>{
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
    }
  }
</script>
