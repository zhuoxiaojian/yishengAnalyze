<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
  import { getCookie } from '@/utils/cookie'
  import * as constant from '@/utils/constant'

export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: ''
    }
  },
  created(){
    //渲染前执行
    let before_token = this.$store.state.token;
    if(before_token == null){
      this.$router.push({path: '/'});
      return;
    }else {
      this.msg = before_token;
    }

  },
  mounted(){
    //渲染后执行

  },
  method:{

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
