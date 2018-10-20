<template>
    <div class="mavMenu">
      <label v-for="navMenu in navMenus">
        <el-menu-item v-if="navMenu.children==null" v-show="navMenu.menuShow" :key="navMenu.menuCode" :data="navMenu" :index="navMenu.path" disabled="">
          <i :class="navMenu.iconCls"></i>
          <span slot="title">{{navMenu.name}}</span>
        </el-menu-item>
        <el-submenu v-else-if="navMenu.children" v-show="navMenu.menuShow" :key="navMenu.menuCode" :data="navMenu" :index="navMenu.path">
          <template slot="title">
            <i :class="navMenu.iconCls"></i>
            <span>{{navMenu.name}}</span>
          </template>
          <nav-menu :navMenus="navMenu.children"></nav-menu>
        </el-submenu>
      </label>
    </div>
</template>

<script>
    import ElMenuItem from "element-ui/packages/menu/src/menu-item";

    export default {
      components: {ElMenuItem},
      name: "nav-menu",
        props: ['navMenus'],
        data(){
          return {}
        },
        methods:{}
    }
</script>

<style scoped>

</style>
