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

  export default {
    components: {
      LeftNav,
      TopNav},
    name: 'home',
    data () {
      return {
        loading: false
      }
    }
  }
</script>

