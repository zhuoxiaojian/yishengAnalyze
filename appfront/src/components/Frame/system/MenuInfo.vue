<template>
  <div class="hello">
    <tree-grid :columns="columns" :tree-structure="true" :data-source="dataSource"></tree-grid>
  </div>
</template>

<script>
  import TreeGrid from '../../treeGrid/TreeGrid'
  import axios from '../../../utils/axiosConfig'
  import baseHost from '../../../api/baseHost'
  export default {
    name: 'menu-info',
    data () {
      return {
        columns: [
          {
            text: 'ID',
            dataIndex: 'id',
          },
          {
            text: '菜单',
            dataIndex: 'name'
          },
          {
            text: '路径',
            dataIndex: 'path'
          },{
            text:'父菜单',
            dataIndex: 'parentId'
          },{
            text:'菜单编码',
            dataIndex: 'menuCode'
          },{
            text: '菜单图标',
            dataIndex: 'iconCls'
          }
        ],
        dataSource: []

      }
    },
    components: {
      TreeGrid
    },
    mounted(){
      // console.log(this.$route.path);
      this.initTree();
      // console.log(this.$route.query.menuCode);
    },
    methods:{
      initTree(){
        let menuURL = baseHost+'/menu/initMenuTree';
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(menuURL,{headers:{ 'Authorization':http_token}}).then((response)=>{
          let data = response.data.message;
          that.dataSource = data;
        }).catch(function (response) {
          console.log("请求失败");
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
