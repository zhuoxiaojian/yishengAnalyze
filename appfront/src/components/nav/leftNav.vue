<template>
  <!--左侧导航-->
  <aside :class="{showSidebar:!collapsed}">
    <!--展开折叠开关-->
    <div class="menu-toggle" @click.prevent="collapse">
      <i class="iconfont icon-outdent" v-show="!collapsed" title="收起"></i>
      <i class="iconfont icon-indent" v-show="collapsed" title="展开"></i>
    </div>
    <el-menu default-active="0"  router :collapse="collapsed"  backgroud-color="#F0F6F6" active-text-color="black">
      <nav-menu :navMenus="menuInfos"></nav-menu>
    </el-menu>
    <!--导航菜单 $router.options.routes-->
    <!--<el-menu router :collapse="collapsed">-->
        <!--<template v-if="menuRoleName=== $store.state.superUserRoleName" v-for="(issue,index) in menuInfos">-->
          <!--<template v-if="issue.name === $store.state.leftNavState">-->
            <!--<template v-for="(item,index) in issue.children">-->
              <!--<el-submenu v-if="!item.leaf" :index="index+''" v-show="item.menuShow">-->
                <!--<template slot="title"><i :class="item.iconCls"></i><span slot="title">{{item.name}}</span></template>-->
                <!--<el-menu-item v-for="term in item.children" :key="term.path" :index="term.path" v-if="term.menuShow"-->
                              <!--:class="$route.path==term.path?'is-active':''">-->
                  <!--<i :class="term.iconCls"></i><span slot="title">{{term.name}}</span>-->
                <!--</el-menu-item>-->
              <!--</el-submenu>-->
              <!--<el-menu-item v-else-if="item.leaf" :index="item.path"-->
                            <!--:class="$route.path==item.path?'is-active':''" v-show="item.menuShow">-->
                <!--<i :class="item.iconCls"></i><span slot="title">{{item.name}}</span>-->
              <!--</el-menu-item>-->
            <!--</template>-->
          <!--</template>-->
        <!--</template>-->


        <!--<template v-if="menuRoleName=== $store.state.normalUserRoleName" v-for="(item,index) in menuInfos">-->
          <!--<span>{{item.name}}</span>-->
              <!--<el-submenu v-if="!item.leaf" :index="index+''" v-show="item.menuShow">-->
                <!--<template slot="title"><i :class="item.iconCls"></i><span slot="title">{{item.name}}</span></template>-->
                <!--<el-menu-item v-for="term in item.children" :key="term.path" :index="term.path" v-if="term.menuShow"-->
                              <!--:class="$route.path==term.path?'is-active':''">-->
                  <!--<i :class="term.iconCls"></i><span slot="title">{{term.name}}</span>-->
                <!--</el-menu-item>-->
              <!--</el-submenu>-->
              <!--<el-menu-item v-else-if="item.leaf" :index="item.path"-->
                            <!--:class="$route.path==item.path?'is-active':''" v-show="item.menuShow">-->
                <!--<i :class="item.iconCls"></i><span slot="title">{{item.name}}</span>-->
              <!--</el-menu-item>-->
        <!--</template>-->

    <!--</el-menu>-->
  </aside>
</template>
<script>
  import axios from 'axios'
  import baseHost from '../../api/baseHost'
  import ElMenu from "element-ui/packages/menu/src/menu";
  import NavMenu from "./navMenu";
  export default {
    components: {
      NavMenu,
      ElMenu},
    name: 'leftNav',
    data () {
      return {
        loading: false,
        collapsed: this.$store.state.collapsed,
        menuInfos: [],
        menuRoleName: 'normalUser'
      }
    },
    mounted(){
      let that = this;
      let token = that.$store.state.token;
      let getMenuUrl = baseHost + '/roleMenu/getRoleMenuList/';//'/roleMenu/getRoleMenuCodeList/';
      axios.get(getMenuUrl, {headers:{ 'Authorization':token}}).then((response)=>{
        let r = that.$router.options.routes;
        let rr;
        let menuCodeList = response.data.MenuCodeList;
        for(let index in r){
          if(r[index].name == that.$store.state.leftNavState){
             rr = r[index].children;
          }
        }
        if(response.data.MenuRoleName === 'superUser'){
          that.menuInfos = menuCodeList;
          that.menuRoleName = response.data.MenuRoleName;
        }else{
          that.menuInfos = menuCodeList;
          that.menuRoleName = response.data.MenuRoleName;
        }

      }).catch((error)=>{
        that.menuInfos = []
      });


    },
    methods: {
      //递归遍历判断
      judgeJson:function (menuCodeList, jsonObject) {
        let that = this;
        for(let index in jsonObject){
          if(menuCodeList.indexOf(jsonObject[index].menuCode) != -1){
            //存在
            jsonObject[index].menuShow = true;
          }else {
            jsonObject[index].menuShow = false;
          }
          if(jsonObject[index].children){
            setTimeout(function () {
              that.judgeJson(menuCodeList, jsonObject[index].children);
            }, 500);
          }
        }

      },
      //折叠导航栏
      collapse: function () {
        this.collapsed = !this.collapsed;
        this.$store.state.collapsed = this.collapsed;
      },
      jumpTo(url, menuCode){
        this.$router.push({path:url, query:{menuCode: menuCode}}); //用go刷新
      }
    },
    watch: {
      '$route': function(to, from){ // 路由改变时执行
        // console.info("to.path:" + to.name);
      }
    },
    created(){

    }
  }
</script>

