<template>
  <div class="crontab-schedule-info">
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="default" size="medium" @click="showAddDialog" :disabled="hasAddPermission">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <!--表格数据-->
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" higlight-current-row>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="minute" label="minute" sortable></el-table-column>
        <el-table-column property="hour" label="hour" sortable></el-table-column>
        <el-table-column property="day_of_week" label="day_of_week" sortable></el-table-column>
        <el-table-column property="day_of_month" label="day_of_month" sortable></el-table-column>
        <el-table-column property="month_of_year" label="month_of_year" sortable></el-table-column>
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
      <el-form :model="CrontabScheduleForm" ref="CrontabScheduleForm" :rules="CrontabScheduleFormRules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="CrontabScheduleForm.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="minute：" :label-width="formLabelWidth" prop="minute">
          <el-input v-model="CrontabScheduleForm.minute" placeholder="minute" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="hour：" :label-width="formLabelWidth" prop="hour">
          <el-input v-model="CrontabScheduleForm.hour" placeholder="hour" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="day_of_week：" :label-width="formLabelWidth" prop="day_of_week">
          <el-input v-model="CrontabScheduleForm.day_of_week" placeholder="day_of_week" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="day_of_month：" :label-width="formLabelWidth" prop="day_of_month">
          <el-input v-model="CrontabScheduleForm.day_of_month" placeholder="day_of_month" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="month_of_year：" :label-width="formLabelWidth" prop="month_of_year">
          <el-input v-model="CrontabScheduleForm.month_of_year" placeholder="month_of_year" auto-complete="off"></el-input>
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
  export default {
    components: {ElRadio},
    name: 'crontab-schedule-info',
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
        CrontabScheduleForm: {
          id: null,
          minute: '*',
          hour: '*',
          day_of_week: '*',
          day_of_month: '*',
          month_of_year: '*'
        },
        CrontabScheduleFormRules:{
          minute:[
            {required: true, trigger: 'blur', message:'minute',}
          ],
          hour:[
            {required: true, trigger: 'blur', message: 'hour',}
          ],
          day_of_week:[
            {required: true, trigger: 'blur', message: 'day_of_week',}
          ],
          day_of_month:[
            {required: true, trigger: 'blur', message: 'day_of_month',}
          ],
          month_of_year:[
            {required: true, trigger: 'blur', message: 'month_of_year',}
          ]
        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        hasAddPermission: hasPermission('add_crontabschedule'),
        hasDetailPermission: hasPermission('change_crontabschedule'),
        hasDeletePermission: hasPermission('delete_crontabschedule'),
      };
    },
    mounted(){

    },
    created(){
      this.initTable(this.currentPage, this.pageSize);
    },
    watch: {

    },
    methods: {
      initTable:function(current_page, page_size){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/systemTask/crontabSchedule/', {params:{page:current_page, page_size: page_size}, headers:{ 'Authorization':http_token}}).then((response)=>{
          that.tableData = response.data.results;
          that.total = response.data.count;
        }).catch(function () {
          console.log("fail");
        })
      },
      handleSearch(){
        // console.info(this.filters.name);
        this.initTable(this.currentPage, this.pageSize)
      },
      handleDetail(index, row) {
        this.dialogTitle = '详情';
        this.dialogAddVisible = true;
        this.CrontabScheduleForm = row;

      },
      handleDelete(index, row) {
        let that = this;
        let deleteCrontabScheduleInfoUrl = baseHost + '/systemTask/crontabScheduleDetail/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deleteCrontabScheduleInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
            that.$message({
              type: 'success',
              message: '删除成功!'
            });
            that.initTable(that.currentPage, that.pageSize);
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
        that.initTable(that.currentPage, that.pageSize);
      },
      handleCurrentChange(val){
        let that = this;
        that.currentPage = val;
        that.initTable(that.currentPage, that.pageSize);
      },
      showAddDialog(){
        this.dialogTitle = '新增';
        this.dialogAddVisible = true;
        this.CrontabScheduleForm = {};
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.CrontabScheduleForm = {};
        //清除验证
        let that = this;
        setTimeout(function () {
          that.$refs['CrontabScheduleForm'].clearValidate();
        }, 100);
      },
      trueSubmit:function () {
        let that = this;
        let addCrontabScheduleInfoUrl = baseHost + '/systemTask/crontabSchedule/';
        let editCrontabScheduleInfoUrl = baseHost + '/systemTask/crontabScheduleDetail/'+that.CrontabScheduleForm.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.CrontabScheduleForm;
        that.$refs['CrontabScheduleForm'].validate((valid) => {
          if (valid) {
            if(that.CrontabScheduleForm.id != null && that.CrontabScheduleForm.id != ''){
              let editParams = handleParams;
              axios.put(editCrontabScheduleInfoUrl, JSON.stringify(editParams),{
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
                that.initTable(that.currentPage, that.pageSize);
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
              axios.post(addCrontabScheduleInfoUrl, JSON.stringify(addParams), {
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
                that.initTable(that.currentPage, that.pageSize);

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
