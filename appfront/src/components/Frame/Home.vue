<template>
  <el-row class="container">
    <!--头部-->
    <el-col :span="24"><!--<router-view name="top"></router-view>-->
    <top-nav></top-nav>
    </el-col>
    <el-col :span="24" class="main">
      <!--左侧导航-->
     <!-- <router-view name="aside"></router-view>-->
      <left-nav></left-nav>
      <!--右侧内容区-->
      <section class="content-container">
        <v-tags></v-tags>
        <div class="grid-content bg-purple-light">
          <el-col :span="24" class="content-wrapper">
            <transition name="fade" mode="out-in">
              <router-view></router-view>
            </transition>
          </el-col>
        </div>
      </section>
    </el-col>
    <div class="footer">
      <footer-copyright></footer-copyright>
    </div>
  </el-row>

</template>
<script>
  import TopNav from "../nav/topNav";
  import LeftNav from "../nav/leftNav";
  import vTags from "../nav/Tags";
  import bus from "../../utils/bus";
  export default {
    components: {
      LeftNav,
      TopNav,
      vTags},
    name: 'home',
    created(){
      // 只有在标签页列表里的页面才使用keep-alive，即关闭标签之后就不保存到内存中了。
      bus.$on('tags', msg => {
        let arr = [];
        for(let i = 0, len = msg.length; i < len; i ++){
          msg[i].name && arr.push(msg[i].name);
        }
        this.tagsList = arr;
      })
    },
    data () {
      return {
        loading: false,
        tagsList: [],
      }
    }
  }
</script>

