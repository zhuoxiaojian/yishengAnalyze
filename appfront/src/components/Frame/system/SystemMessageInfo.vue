<template>
  <div class="system-message-info">
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
             <el-select class="item-choose" v-model="filters.name" size="small" @change="handleSearch">
            <el-option
              v-for="(item,index) in flagSearchOptions"
              :key="index"
              :label="item.name"
              :value="item.value"
            ></el-option>
          </el-select>
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
      <el-table :data="tableData" border style="width: 100%" tooltip-effect="dark" @selection-change="handleSelectionChange" higlight-current-row>
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column property="id" label="ID"></el-table-column>
        <el-table-column property="message_info" label="消息"  sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column property="create_date" label="时间" :formatter="dateFormat" sortable></el-table-column>
        <el-table-column property="flag" label="标签" :formatter="flagFormat"></el-table-column>
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
      <el-form :model="systemMessageForm" ref="systemMessageForm" :rules="rules">
        <el-form-item label="ID：" :label-width="formLabelWidth" prop="id" hidden="true">
          <el-input v-model="systemMessageForm.id" placeholder="ID" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="消息：" :label-width="formLabelWidth" prop="message_info">
          <el-input type="textarea" :rows="7" v-model="systemMessageForm.message_info" placeholder="消息" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="时间：" :label-width="formLabelWidth" prop="value">
           <el-date-picker
              v-model="systemMessageForm.create_date"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择日期">
            </el-date-picker>
        </el-form-item>
        <el-form-item label="标签：" :label-width="formLabelWidth" prop="flag">
           <el-select class="item-choose" v-model="systemMessageForm.flag" size="small">
            <el-option
              v-for="(item,index) in flagOptions"
              :key="index"
              :label="item.name"
              :value="item.value"
            ></el-option>
          </el-select>
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
    name: 'system-message-info',
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
        flagOptions: [
            {'name': '已读', 'value': 1},
            {'name': '未读', 'value': 0},
            {'name': '回收', value: 2}
        ],
        flagSearchOptions: [
            {'name': '已读', 'value': 1},
            {'name': '未读', 'value': 0},
            {'name': '回收', value: 2},
            {'name': '全部', value: null}
        ],
        systemMessageForm: {
          id: null,
          message_info: '',
          create_date: '',
          flag: '',
        },
        rules:{
          message_info:[
            {required: true, trigger: 'blur', message: '请输入消息'}
          ],
        },
        formLabelWidth: '120px',
        dialogAddVisible: false,
        filters: {
          name: ''
        },
        hasAddPermission: hasPermission('add_systemmessage'),
        hasDetailPermission: hasPermission('change_systemmessage'),
        hasDeletePermission: hasPermission('delete_systemmessage'),
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
        flagFormat(row, column){
            let flag = row.flag;
            if(flag == 0){
                return "未读";
            }else if(flag == 1){
                return "已读";
            }else if(flag == 2){
                return "回收";
            }else{
                return "未读";
            }
        },
        dateFormat(row, column){
            if(row.create_date == null){
            return '';
            }
            let time = new Date(row.create_date);
            return `${time.getFullYear()}-${time.getMonth() + 1 >= 10 ? (time.getMonth() + 1) : '0' + (time.getMonth() + 1)}-${time.getDate() >= 10 ? time.getDate() : '0' + time.getDate()}
                        ${time.getHours() >= 10 ? time.getHours() : '0' + time.getHours()} : ${time.getMinutes()>=10?time.getMinutes():'0'+time.getMinutes()} : ${time.getSeconds() >= 10 ? time.getSeconds() : '0' + time.getSeconds()}`;
      },
      initTable:function(current_page, page_size, flagName){
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(baseHost+'/systemMessage/systemMessage/', {params:{page:current_page, page_size: page_size, search: flagName}, headers:{ 'Authorization':http_token}}).then((response)=>{
          that.tableData = response.data.results;
          that.total = response.data.count;
        }).catch(function () {
          console.log("fail");
        })
      },
      handleSearch(){
        this.initTable(this.currentPage, this.pageSize, this.filters.name)
      },
      handleDetail(index, row) {
        this.dialogTitle = '详情';
        this.dialogAddVisible = true;
        this.systemMessageForm = row;

      },
      handleDelete(index, row) {
        let that = this;
        let deleteSystemMessageInfoUrl = baseHost + '/systemMessage/systemMessage/'+row.id+'/';
        let http_token = that.$store.state.token;
        that.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(()=>{
          axios.delete(deleteSystemMessageInfoUrl,  {headers:{'Authorization':http_token}}).then(()=>{
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
        this.systemMessageForm = {};
      },
      handleClose(done){  //关闭弹窗
        done();
      },
      cancleSubmit:function () {
        this.dialogAddVisible = false;
        this.systemMessageForm = {};
        //清除验证
        let that = this;
        setTimeout(function () {
          that.$refs['systemMessageForm'].clearValidate();
        }, 100);
      },
      trueSubmit:function () {
        let that = this;
        let addSystemMessageInfoUrl = baseHost + '/systemMessage/systemMessage/';
        let editSystemMessageInfoUrl = baseHost + '/systemMessage/systemMessage/'+that.systemMessageForm.id+'/';
        let http_token = that.$store.state.token;
        axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        let handleParams = that.systemMessageForm;
        that.$refs['systemMessageForm'].validate((valid) => {
          if (valid) {
            if(that.systemMessageForm.id != null && that.systemMessageForm.id != ''){
              let editParams = handleParams;
              axios.put(editSystemMessageInfoUrl, JSON.stringify(editParams),{
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
              axios.post(addSystemMessageInfoUrl, JSON.stringify(addParams), {
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
