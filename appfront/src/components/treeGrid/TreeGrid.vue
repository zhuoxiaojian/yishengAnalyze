<template>
  <div>
    <el-button type="default" size="medium" @click="addEquipment" :disabled="hasAddPermission">新增</el-button>　
    <el-button type="primary" size="medium" @click="oneKeyToAdd" :disabled="hasAddPermission">一键添加</el-button>
  <el-table
    :data="data"
    border
    style="width: 100%; margin-top: 10px;"
    :row-style="showTr">
    <el-table-column v-for="(column, index) in columns" :key="column.dataIndex"
                     :label="column.text">
      <template slot-scope="scope">
        <span v-if="spaceIconShow(index)" v-for="(space, levelIndex) in scope.row._level" class="ms-tree-space"></span>
        <button class="button is-outlined is-primary is-small" v-if="toggleIconShow(index,scope.row)" @click="toggle(scope.$index)">
          <i v-if="!scope.row._expanded" class="el-icon-caret-right" aria-hidden="true"></i>
          <i v-if="scope.row._expanded" class="el-icon-caret-bottom" aria-hidden="true"></i>
        </button>
        <span v-else-if="index===0" class="ms-tree-space"></span>
        {{scope.row[column.dataIndex]}}
      </template>
    </el-table-column>
    <el-table-column label="操作" v-if="treeType === 'normal'" width="260">
      <template slot-scope="scope">
        <el-button type="button" class="el-button el-button--default el-button--small" @click="handleEdit(scope.row)"
          :disabled="hasDetailPermission">
            编辑
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.row)"
          :disabled="hasDeletePermission">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>

    <el-dialog
      :title="titleMap[dialogStatus]"
      :visible.sync="dialogVisible"
      @close="closeModelDialog">
      <el-form :model="form" ref="form" :rules="rules">
        <el-form-item label="ID：" hidden="true" prop="id">
          <el-input  v-model="form.id" auto-complete="off" ></el-input>
        </el-form-item>

          <el-form-item prop="is_parent" >
            <el-checkbox label="是否根菜单" v-model="form.is_parent"></el-checkbox>
          </el-form-item>
        <el-form-item label="菜单：" prop="name">
          <el-input v-model="form.name" auto-complete="off" placeholder=" 输入菜单名或按钮名"></el-input>
        </el-form-item>
        <el-form-item label="父菜单ID：" hidden="true" prop="parentId">
          <el-input v-model="form.parentId" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="父菜单："  prop="parentIdName" :hidden=isFlag>
          <el-input v-model="parentIdName" auto-complete="off" readonly="readonly" placeholder="上级菜单" @click.native="selectTree" style="background: #8c939d"></el-input>
          <!--<el-button type="primary" @click="selectTree">选择</el-button>-->
        </el-form-item>
        <el-form-item label="路径：" prop="url">
          <el-input v-model="form.path" auto-complete="off" placeholder=" 输入菜单路径"></el-input>
        </el-form-item>
        <el-form-item label="图标：" prop="icon">
          <el-input v-model="form.iconCls" auto-complete="off"  placeholder=" 输入菜单图标"></el-input>
        </el-form-item>
        <el-form-item label="菜单编码：" prop="menuCode">
          <el-input v-model="form.menuCode" auto-complete="off" placeholder=" 输入菜单编码"></el-input>

        </el-form-item>

      </el-form>
      <a  @click="showTip">*点击提示*</a>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelModel">取 消</el-button>
        <el-button type="primary" @click="trueModel">确 定</el-button>
      </div>
    </el-dialog>



    <el-dialog
      title="菜单树"
      :visible.sync="dialogTreeVisible"
      width="30%"
      @close='closeTreeDialog'>
      <el-tree :data="myMenuTree"
               :props="defaultProps"
               @node-click="handleNodeClick"

      ></el-tree>
     <!--
              :before-close="handleClose"
                show-checkbox
               @check-change="handleCheckChange"
     <div slot="footer" class="dialog-footer">
        <el-button @click="cancelTreeModel">取 消</el-button>
        <el-button type="primary" @click="trueTreeModel">确 定</el-button>
      </div>
      -->
    </el-dialog>

    <el-dialog
      title="提示"
      :visible.sync="dialogTipVisible">
      {{RouteMenuCodeList}}
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogTipVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogTipVisible = false">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>
  <script>
    import DataTransfer from '../../utils/dataTranslate.js'
    import Vue from 'vue'
    import ElButton from "element-ui/packages/button/src/button";
    import ElFormItem from "element-ui/packages/form/src/form-item";
    import ElInput from "element-ui/packages/input/src/input";
    import axios from '../../utils/axiosConfig'
    import baseHost from '../../api/baseHost'
    import hasPermission from '../../utils/util'
    export default {
      inject: ['reload'],
      components: {
        ElInput,
        ElFormItem,
        ElButton},
      name: 'tree-grid',
      props: {
// 该属性是确认父组件传过来的数据是否已经是树形结构了，如果是，则不需要进行树形格式化
        treeStructure: {
          type: Boolean,
          default: function () {
            return false
          }
        },
// 这是相应的字段展示
        columns: {
          type: Array,
          default: function () {
            return []
          }
        },
// 这是数据源
        dataSource: {
          type: Array,
          default: function () {
            return []
          }
        },
// 这个作用是根据自己需求来的，比如在操作中涉及相关按钮编辑，删除等，需要向服务端发送请求，则可以把url传过来
        requestUrl: {
          type: String,
          default: function () {
            return ''
          }
        },
// 这个是是否展示操作列
        treeType: {
          type: String,
          default: function () {
            return 'normal'
          }
        },
// 是否默认展开所有树
        defaultExpandAll: {
          type: Boolean,
          default: function () {
            return false
          }
        }
      },
      data () {
        return {
          myMenuTree: [],
          defaultProps: {
            children: 'children',
            label: 'name'
          },
          dialogTreeVisible: false,
          isFlag: true,
          parentIdName: null,
          dialogVisible:false,     //模态框是否显示
          addLoading: false,       //是否显示loading
          form:{
            id : null,
            is_parent: false,
            parentId: null,
            name:"",
            path:"",
            iconCls:"",
            menuCode:"",
          },
          //rules
          rules:{
            name:[
              {required: true, message: '请输入菜单名', trigger: 'blur'}
            ],
            menuCode:[
              {required: true, trigger: 'blur', validator: this.validateMenuCode},
              {min:1, max:20, message: '菜单编码不得超过20个字符', trigger: 'blur'}
            ],
            path:[
              {required: true, message: '请输入菜单路径', trigger: 'blur'}
            ]
          },
          //新增or编辑弹框标题(根据点击的新增or编辑按钮显示不同的标题)
          titleMap: {
            addEquipment:'新增',
            editEquipment: '编辑',
          },
          //新增和编辑弹框标题
          dialogStatus: "",
          RouteMenuCodeList: [],
          dialogTipVisible:false,
          hasAddPermission: hasPermission('add_menu'),
          hasDetailPermission: hasPermission('change_menu'),
          hasDeletePermission: hasPermission('delete_menu'),
        }
      },
      computed: {
        // 格式化数据源
        data: function () {
          let me = this
          if (me.treeStructure) {
            let data = DataTransfer.treeToArray (me.dataSource, null, null, me.defaultExpandAll)
            return data
          }
          return me.dataSource
        }
      },
      watch: {
        // form:{
        //   handler(newVal, oldVal){
        //     console.log(newVal.is_parent);
        //   },
        //   deep: true,
        //   immediate: false
        // }

        "form.is_parent": function is_parent(newVal, oldVal){
           if(newVal){
             this.parentIdName = null;
             this.form.parentId = null;
             this.isFlag = true;
           }else{
             this.isFlag = false;
           }
        },

      },
      mounted(){
        let menuURL = baseHost+'/menu/initMenuTree';
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(menuURL, {headers:{ 'Authorization':http_token}}).then((response)=>{
          let data = response.data.message;
          that.myMenuTree = data;
        }).catch(function (response) {
          console.log("请求失败");
        });
        // console.log(that.RouteMenuCodeList);

      },
      methods: {
        //生成菜单树
        getRouteMenuCodeTree:function (jsonObject) {
          let that = this;
          for(let index in jsonObject){
            if(jsonObject[index].menuCode != 'HomePage'){
              let children = that.getRouteMenuCodeTreeNode(jsonObject[index]);
              if(jsonObject[index].children){
                children.children = [];
                for(let ch in jsonObject[index].children){
                  children.children[ch] = (that.getRouteMenuCodeTreeNode(jsonObject[index].children[ch]));
                  children.children[ch].parent_code = jsonObject[index].menuCode;
                }
              }
              that.RouteMenuCodeList.push(children);
            }
          }
        },
        //单个节点的处理
        getRouteMenuCodeTreeNode:function (jsonObject) {
            let jsonMenu = {};
            if(jsonObject.name){
              jsonMenu.name = jsonObject.name;
            }
            if(jsonObject.path){
              jsonMenu.path = jsonObject.path;
            }
            if(jsonObject.menuCode){
              jsonMenu.menuCode = jsonObject.menuCode;
            }
            if(jsonObject.iconCls){
              jsonMenu.iconCls = jsonObject.iconCls;
            }else{
              jsonMenu.iconCls = null;
            }
            if(jsonObject.children){
              jsonMenu.is_parent = true;
            }else{
              jsonMenu.is_parent = false;
            }

           return jsonMenu;
        },
        //弹出提示
        showTip:function () {
          let that = this;
          that.RouteMenuCodeList = []
          that.getRouteMenuCodeTree(require('../../constant/menuJson/menu.json'));
          this.dialogTipVisible = true;

        },
        //校验菜单编码是否存在
        validateMenuCode:function (rule, value, callback) {
          if(!value){
            return callback(new Error('请输入菜单编码'));
          }
          let checkMenuCodeUrl = baseHost+'/menu/checkMenuCode/';
          let checkParams = {menuId: this.form.id, menuCode: value};
          axios.get(checkMenuCodeUrl, {params: checkParams}).then((response)=>{
            if(response.data.code == 300){
              return callback(new Error(response.data.message));
            }else {
              return callback();
            }
          }).catch(()=>{
            return callback();
          });
        },
        // 显示行
        showTr: function (row, index) {
          let show = (row.row._parent ? (row.row._parent._expanded && row.row._parent._show) : true)
          row.row._show = show
          return show ? '' : 'display:none;'

        },
        // 展开下级
        toggle: function (trIndex) {
          let me = this
          let record = me.data[trIndex]
          record._expanded = !record._expanded
        },
        // 显示层级关系的空格和图标
        spaceIconShow (index) {
          let me = this
          if (me.treeStructure && index === 0) {
            return true
          }
          return false
        },
        // 点击展开和关闭的时候，图标的切换
        toggleIconShow (index, record) {

          let me = this
          if (me.treeStructure && index === 0 && record.children && record.children.length > 0) {
            return true
          }
          return false
        },
        handleDelete (row) {
          // alert(row.id);
          let that = this;
          this.$confirm('此操作将永久删除该记录, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'error'
          }).then(() => {
            let deleteURL = baseHost+'/menu/menudetail/'+row.id+'/';
            let http_token = that.$store.state.token;
            axios.delete(deleteURL,{headers:{'Authorization':http_token}}).then((response)=>{
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
              this.reload();
            }).catch((response)=>{
              this.$message({
                type: 'fail',
                message: '删除失败！',
              });
              console.log("delete fail");
            });


          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
          })
        },
        handleEdit(row){
          this.form={};
          //显示弹框
          let that = this;
          this.dialogVisible = true;
          //编辑弹框标题
          this.dialogStatus = "editEquipment";
          this.form = row;
          let http_token = that.$store.state.token;
          let parent_id = row.parentId;
          if(parent_id != null && parent_id != ''){
            let queryParentNameUrl = baseHost+'/menu/menudetail/'+parent_id+'/';
            axios.get(queryParentNameUrl,{headers:{'Authorization':http_token}}).then((response)=>{
              // console.log(response);
              that.parentIdName = response.data.name;
              that.isFlag = false;

            }).catch(function (response) {
              console.log("请求失败");
            })
          }
        },
        //新增
        addEquipment() {
          //显示弹框
          this.dialogVisible = true;
          //新增弹框标题
          this.dialogStatus = "addEquipment";
          this.form={};
          this.isFlag = true;
          this.parentIdName = null;
        },

        selectTree(){
          this.dialogTreeVisible = true;
        },
        handleNodeClick(data) {
          // console.log(JSON.stringify(data));
          this.parentIdName = data.name;
          this.form.parentId = data.id;
        },
        closeTreeDialog(){
          this.dialogTreeVisible = false;
          //window.location.reload();
        },
        closeModelDialog(){
          this.reload();
        },cancelModel(){
          this.dialogVisible = false;
        },
        trueModel(){
          let that = this;
          that.$refs['form'].validate((valid) => {
            if (valid) {
              that.dialogVisible = false;
              if (that.form.id != null) {
                let putURL = baseHost + '/menu/menudetail/' + that.form.id + '/';
                let params = {};
                params.id = that.form.id;
                params.is_parent = that.form.is_parent;
                params.name = that.form.name;
                params.parentId = that.form.parentId;
                params.path = that.form.path;
                params.iconCls = that.form.iconCls;
                params.menuCode = that.form.menuCode;
                axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';  //此处是增加的代码，设置请求头的类型
                //"Access-Control-Allow-Origin", "*"
                let http_token = that.$store.state.token;
                axios.put(putURL, JSON.stringify(params),
                  {
                    headers: {
                      'Content-Type': 'application/json;charset=UTF-8',
                      'Authorization': http_token
                    }

                  }
                ).then((response) => {
                  this.$message({
                    type: 'success',
                    message: '修改成功!'
                  });
                  that.reload();
                  console.log("success");
                }).catch(()=> {
                  this.$message({
                    type: 'fail',
                    message: '修改失败!'
                  });
                  console.log("fail");
                })
                //
              } else {
                let addURL = baseHost + '/menu/menu/';
                let data = {};
                data.is_parent = that.form.is_parent;
                data.path = that.form.path;
                data.iconCls = that.form.iconCls;
                data.name = that.form.name;
                data.parentId = that.form.parentId;
                data.menuCode = that.form.menuCode;

                let http_token = that.$store.state.token;
                axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
                axios.post(addURL, JSON.stringify(data), {
                  headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': http_token
                  }
                }).then((response) => {
                  this.$message({
                    type: 'success',
                    message: '添加成功!'
                  });
                  that.reload();
                  console.log("添加成功");
                }).catch(()=>{
                  this.$message({
                    type: 'fail',
                    message: '添加失败!'
                  });
                  console.log("添加失败");
                })
              }
            }
          })
        },
        handleCheckChange(data, checked, indeterminate) {
          console.log(data, checked, indeterminate);
        },
        oneKeyToAdd:function () {
          let that = this;
          that.RouteMenuCodeList = []
          // let r = that.$router.options.routes;
          // for(let index in r){
          //   if(r[index].name == that.$store.state.leftNavState){
          //     that.getRouteMenuCodeTree(r[index].children);
          //   }
          // }
          that.getRouteMenuCodeTree(require('../../constant/menuJson/menu.json'));
          let oneKeyAddUrl = baseHost + '/menu/oneKeyToAddMenu/';
          axios.post(oneKeyAddUrl, JSON.stringify(that.RouteMenuCodeList), {headers:{'Content-Type': 'application/json;charset=UTF-8'}}).then(()=>{
            that.$message({
              type: 'success',
              message: '添加成功!'
            });
            that.reload();
          }).catch(()=>{
            that.$message({
              type: 'fail',
              message: '添加失败!'
            });
          });
        }
      }
    }
  </script>
  <style scoped>
    .ms-tree-space{position: relative;
      top: 1px;
      display: inline-block;
      font-family: 'Glyphicons Halflings';
      font-style: normal;
      font-weight: 400;
      line-height: 1;
      width: 18px;
      height: 14px;}
    .ms-tree-space::before{content: ""}
    table td{
      line-height: 26px;
    }
  </style>
