<template>
  <div class="periodic-task-info">
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
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" higlight-current-row>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="name" label="名称" ></el-table-column>
        <el-table-column property="task" label="任务"  sortable></el-table-column>
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
      <el-form :model="PeriodicTaskForm" ref="PeriodicTaskForm" :rules="PeriodicTaskFormRules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="PeriodicTaskForm.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="名称：" :label-width="formLabelWidth" prop="name">
          <el-input v-model="PeriodicTaskForm.name" placeholder="名称" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="任务：" :label-width="formLabelWidth" prop="task">
          <el-input v-model="PeriodicTaskForm.task" placeholder="任务，格式：users.tasks.test" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="周期：" :label-width="formLabelWidth" prop="interval">
          <el-select class="item-choose" v-model="PeriodicTaskForm.interval" size="small">
            <el-option
              v-for="(item,index) in IntervalIdOptions"
              :key="index"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="定时：" :label-width="formLabelWidth" prop="crontab">
          <el-select class="item-choose" v-model="PeriodicTaskForm.crontab" size="small">
            <el-option
              v-for="(item,index) in CrontabIdOptions"
              :key="index"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="参数：" :label-width="formLabelWidth" prop="args">
          <el-input type="textarea" :rows="7" v-model="PeriodicTaskForm.args" placeholder="请输入参数，格式：[1,2]"></el-input>
        </el-form-item>
        <el-form-item label="关键字参数：" :label-width="formLabelWidth" prop="kwargs">
          <el-input type="textarea" :rows="7" v-model="PeriodicTaskForm.kwargs" placeholder="请输入关键字参数，格式：{}"></el-input>
        </el-form-item>
        <el-form-item label="队列：" :label-width="formLabelWidth" prop="queue">
          <el-input v-model="PeriodicTaskForm.queue" placeholder="Queue defined in CELERY_QUEUES" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="Exchange：" :label-width="formLabelWidth" prop="exchange">
          <el-input v-model="PeriodicTaskForm.exchange" placeholder="Exchange" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="RoutingKey：" :label-width="formLabelWidth" prop="routing_key">
          <el-input v-model="PeriodicTaskForm.routing_key" placeholder="RoutingKey" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="状态：" :label-width="formLabelWidth">
          <el-checkbox v-model="PeriodicTaskForm.enabled" label="启动"></el-checkbox>
        </el-form-item>
        <el-form-item label="描述：" :label-width="formLabelWidth" prop="description">
          <el-input type="textarea" :rows="7" v-model="PeriodicTaskForm.description" placeholder="请输入任务描述"></el-input>
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
  import ElInput from "element-ui/packages/input/src/input";
  import ElFormItem from "element-ui/packages/form/src/form-item";
  export default {
    components: {
      ElFormItem,
      ElInput,
      ElRadio},
    name: 'periodic-task-info',
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
        PeriodicTaskForm: {
          id: null,
          name: '',
          task: '',
          interval:'',
          crontab:'',
          args:[],
          kwargs:{},
          queue:'',
          enabled:true,
          description:'',
          routing_key:'',
          exchange:''
        },
        PeriodicTaskFormRules:{
          name:[
            {required: true, trigger: 'blur', message:'请输入名称',}
          ],
          task:[
            {required: true, trigger: 'blur', message: '请填写任务，格式：users.tasks.test',}
          ],

        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          name: ''
        },
        hasAddPermission: hasPermission('add_periodictask'),
        hasDetailPermission: hasPermission('change_periodictask'),
        hasDeletePermission: hasPermission('delete_periodictask'),
        IntervalIdOptions:[],
        CrontabIdOptions:[],

      };
    },
    mounted(){

    },
    created(){
      this.initTable(this.currentPage, this.pageSize, this.filters.name);
      this.initIngervalIdsOptions();
      this.initCrontabIdsOptions();
    },
    watch: {

    },
    methods: {
      initIngervalIdsOptions:function () {
        let getAllIntervalScheduleUrl = baseHost + "/systemTask/getAllIntervalSchedule/";
        let that = this;
        axios.get(getAllIntervalScheduleUrl).then((response)=>{
          that.IntervalIdOptions = response.data.resultData;
        }).catch(()=>{
        });
      },
      initCrontabIdsOptions:function () {
        let getAllCrontabScheduleUrl = baseHost + "/systemTask/getAllCrontabSchedule/";
        let that = this;
        axios.get(getAllCrontabScheduleUrl).then((response)=>{
          that.CrontabIdOptions = response.data.resultData;
        }).catch(()=>{
        });
      },
      initTable:function(current_page, page_size, periodicTaskName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/systemTask/periodicTask/', {params:{page:current_page, page_size: page_size, periodicTaskName: periodicTaskName}, headers:{ 'Authorization':http_token}}).then((response)=>{
          that.tableData = response.data.results;
          that.total = response.data.count;
        }).catch(function () {
          console.log("fail");
        })
      },
      handleSearch(){
        // console.info(this.filters.name);
        this.initTable(this.currentPage, this.pageSize, this.filters.name)
      },
      handleDetail(index, row) {
        this.dialogTitle = '详情';
        this.dialogAddVisible = true;
        this.PeriodicTaskForm = row;

      },
      handleDelete(index, row) {
        let that = this;
        let deletePeriodicTaskInfoUrl = baseHost + '/systemTask/periodicTaskDetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deletePeriodicTaskInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
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
        this.PeriodicTaskForm = {};
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.PeriodicTaskForm = {};
        //清除验证
        let that = this;
        setTimeout(function () {
          that.$refs['PeriodicTaskForm'].clearValidate();
        }, 100);
      },
      trueSubmit:function () {
        let that = this;
        let addPeriodicTaskInfoUrl = baseHost + '/systemTask/periodicTask/';
        let editPeriodicTaskInfoUrl = baseHost + '/systemTask/periodicTaskDetail/'+that.PeriodicTaskForm.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.PeriodicTaskForm;
        that.$refs['PeriodicTaskForm'].validate((valid) => {
          if (valid) {
            if(that.PeriodicTaskForm.id != null && that.PeriodicTaskForm.id != ''){
              let editParams = handleParams;
              axios.put(editPeriodicTaskInfoUrl, JSON.stringify(editParams),{
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': http_token
                }
              }).then(()=>{
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
              axios.post(addPeriodicTaskInfoUrl, JSON.stringify(addParams), {
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': http_token
                }
              }).then(()=>{
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
