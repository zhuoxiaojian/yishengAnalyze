import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: resolve=> require(['@/components/login/Login'], resolve),
    },
    {
      path: '/appfront/frontLogin',
      name: 'frontLogin',
      component: resolve=> require(['@/components/login/Login'], resolve),
    },
    {
      path: "*",
      redirect: "/",
      name: 'redirectLogin'
    },
    {
      path: '/appfront/Home',
      type: 'home',
      name: 'home',
      component: resolve=> require(['@/components/Frame/Home'], resolve),
      meta: {
        requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
      },
      children: [
        {
          path: '/appfront/Home',
          name: '我的首页',
          component: resolve=> require(['@/components/HelloWorld'], resolve),
          leaf: true, // 只有一个节点
          iconCls: 'iconfont icon-home', // 图标样式class
          menuShow: true,
          menuCode: 'HomePage',
          meta: {requireAuth: true,},
        },
        {
          path: '/appfront/System',
          component:  resolve=> require(['@/components/Frame/System'], resolve),
          name: '系统管理',
          iconCls: 'el-icon-menu',
          menuShow: true,
          menuCode: 'SystemPage',
          meta: {requireAuth: true,},
        },
        {
          path: '/appfront/System/UserInfo',
          component: resolve=> require(['@/components/Frame/System/UserInfo'], resolve),
          name: '用户管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'UserPage',
        },
        {
          path: '/appfront/System/MenuInfo',
          component: resolve=> require(['@/components/Frame/System/MenuInfo'], resolve),
          name: '菜单管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'MenuPage',
        },
        {
          path: '/appfront/System/RoleInfo',
          component: resolve=> require(['@/components/Frame/System/RoleInfo'], resolve),
          name: '角色管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'RolePage',
        },
        {
          path: '/appfront/System/DepartInfo',
          component: resolve=> require(['@/components/Frame/System/DepartInfo'], resolve),
          name: '部门管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'DepartPage',
        },
        {
          path: '/appfront/System/ConstantInfo',
          component: resolve=> require(['@/components/Frame/System/ConstantInfo'], resolve),
          name: '常量管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'ConstantPage',
        },
        {
          path: '/appfront/System/PermissionInfo',
          component: resolve=> require(['@/components/Frame/System/PermissionInfo'], resolve),
          name: '权限管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'PermissionPage',
        },
        {
          path: '/appfront/System/ContentTypeInfo',
          component: resolve=> require(['@/components/Frame/System/ContentTypeInfo'], resolve),
          name: '实体管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'ContentTypePage',
        },
        {
          path: '/appfront/System/BaseChartInfo',
          component: resolve=> require(['@/components/Frame/System/BaseChartInfo'], resolve),
          name: '报表管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'BaseChartPage',
        },
        {
          path: '/appfront/System/MarkDownInfo',
          component: resolve=> require(['@/components/Frame/System/MarkDownInfo'], resolve),
          name: 'MarkDown',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'MarkDownPage',
        },
        {
          path: '/appfront/System/VueEditorInfo',
          component: resolve=> require(['@/components/Frame/System/VueEditorInfo'], resolve),
          name: 'VueEditor',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'VueEditorPage',
        },
        {
          path: '/appfront/Task',
          component: resolve=> require(['@/components/Frame/Task'], resolve),
          name: '任务管理',
          iconCls: 'el-icon-menu',
          menuShow: true,
          menuCode: 'TaskPage',
          meta: {requireAuth: true},
        },
        {
          path: '/appfront/Task/PeriodicTaskInfo',
          component: resolve=> require(['@/components/Frame/Task/PeriodicTaskInfo'], resolve),
          name: '定时任务',
          menuShow: true,
          menuCode: 'PeriodicTaskPage',
          meta: {requireAuth: true},
        },
        {
          path: '/appfront/Task/IntervalScheduleInfo',
          component: resolve=> require(['@/components/Frame/Task/IntervalScheduleInfo'], resolve),
          name: '循环时间',
          menuShow: true,
          menuCode: 'IntervalSchedulePage',
          meta: {requireAuth: true},
        },
        {
          path: '/appfront/Task/CrontabScheduleInfo',
          component: resolve=> require(['@/components/Frame/Task/CrontabScheduleInfo'], resolve),
          name: '定时时间',
          menuShow: true,
          menuCode: 'CrontabSchedulePage',
          meta: {requireAuth: true},
        },{
          path: '/appfront/Task/TaskStateInfo',
          component: resolve=> require(['@/components/Frame/Task/TaskStateInfo'], resolve),
          name: '任务监控',
          menuShow: true,
          menuCode: 'TaskStatePage',
          meta: {requireAuth: true},
        },
        {
          path: '/appfront/Back',
          component: resolve=> require(['@/components/Frame/Back'], resolve),
          name: '后台管理',
          iconCls: 'el-icon-menu',
          menuShow: true,
          menuCode: 'BackPage',
          meta: {requireAuth: true,},
        },
        { path: '/appfront/Back/yiShengUser',
          component: resolve=> require(['@/components/Frame/yiSheng/yiShengUser'], resolve),
          name: '网站管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'yiShengUserPage',
        },
        {
          path: '/appfront/Back/yiShengContract',
          component: resolve=> require(['@/components/Frame/yiSheng/yiShengContract'], resolve),
          name: '合同管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'yiShengContractPage',
        },
        {
          path: '/appfront/Back/yiShengFtpUser',
          component: resolve=> require(['@/components/Frame/yiSheng/yiShengFtpUser'], resolve),
          name: 'FTP管理',
          menuShow: true,
          meta: {requireAuth: true,},
          menuCode: 'yiShengFtpUserPage'
        },

      ]
    },

  ],
  mode: "history"//干掉地址栏里边的#号键
})

