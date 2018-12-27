<template>
  <div class="departTree">
    <depart-tree-grid :columns="columns" :tree-structure="true" :data-source="dataSource"></depart-tree-grid>
  </div>
</template>

<script>
  import DepartTreeGrid from '../../treeGrid/DepartTreeGrid'
  import axios from '../../../utils/axiosConfig'
  import baseHost from '../../../api/baseHost'
  export default {
    name: 'depart-info',
    data () {
      return {
        columns: [
          {
            text: 'ID',
            dataIndex: 'id',
          },
          {
            text: '部门',
            dataIndex: 'name'
          },
          {
            text:'上级部门',
            dataIndex: 'parentId'
          },{
            text:'部门编码',
            dataIndex: 'departCode'
          }

        ],
        dataSource: []

      }
    },
    components: {
      DepartTreeGrid
    },
    mounted(){
      // console.log(this.$route.path);
      this.initTree();
      // console.log(this.$route.query.menuCode);
    },
    methods:{
      initTree(){
        let departURL = baseHost+'/depart/initDepartTree';
        let that = this;
        let http_token = that.$store.state.token;
        axios.get(departURL,{headers:{ 'Authorization':http_token}}).then((response)=>{
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
