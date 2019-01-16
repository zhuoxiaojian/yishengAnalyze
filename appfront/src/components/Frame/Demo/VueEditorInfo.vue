<template>
  <div>
      <!-- 图片上传组件辅助-->
      <el-upload
        class="avatar-uploader"
        :action="serverUrl"
        name="file"
        :headers="header"
        :show-file-list="false"
        :on-success="uploadSuccess"
        :on-error="uploadError"
        :before-upload="beforeUpload">
      </el-upload>
      <el-row v-loading="quillUpdateImg">
      <quill-editor ref="myTextEditor" v-model="content" :options="editorOption"></quill-editor>
      <el-button class="editor-btn" type="primary" @click="submit">提交</el-button>
      </el-row>
  </div>

</template>

<script>
  import 'quill/dist/quill.core.css';
  import 'quill/dist/quill.snow.css';
  import 'quill/dist/quill.bubble.css';
  import { quillEditor } from 'vue-quill-editor';
  import baseHost from '../../../api/baseHost';
  // 工具栏配置
  const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['blockquote', 'code-block'],
    [{'header': 1}, {'header': 2}],               // custom button values
    [{'list': 'ordered'}, {'list': 'bullet'}],
    [{'script': 'sub'}, {'script': 'super'}],      // superscript/subscript
    [{'indent': '-1'}, {'indent': '+1'}],          // outdent/indent
    [{'direction': 'rtl'}],                         // text direction
    [{'size': ['small', false, 'large', 'huge']}],  // custom dropdown
    [{'header': [1, 2, 3, 4, 5, 6, false]}],
    [{'color': []}, {'background': []}],          // dropdown with defaults from theme
    [{'font': []}],
    [{'align': []}],
    // ['link', 'image', 'video'],
    ['image'],
    ['clean'],                                         // remove formatting button
  ]

  export default {
    name: 'vue-editor-info',
    data: function(){
      return {
        quillUpdateImg: false,
        serverUrl: '',  // 这里写你要上传的图片服务器地址
        header:{},
        content: '',
        editorOption: {
          placeholder: 'Hello World',
          modules:{
            toolbar:{
              container: toolbarOptions,  // 工具栏
              handlers:{
                'image': function(value){
                   if(value){
                     document.querySelector('.avatar-uploader input').click();
                   }else{
                     this.quill.format('image', false);
                   }
                }
              }
            }
          }
        }
      }
    },
    components: {
      quillEditor
    },
    created(){
      let uploadUrl = baseHost + '/file/handleFileUpload/';
      this.serverUrl = uploadUrl;
    },
    methods: {
      onEditorChange({ editor, html, text }) {
        this.content = html;
      },
      submit(){
        console.log(this.content);
        this.$message.success('提交成功！');
      },
      // 上传图片前
      beforeUpload(res, file) {
        // 显示loading动画
        this.quillUpdateImg = true;
      },
      // 上传图片成功
      uploadSuccess(res, file) {
        // res为图片服务器返回的数据
        // 获取富文本组件实例
        let quill = this.$refs.myTextEditor.quill;
        // 如果上传成功
        if (res.info !== null) {
          // 获取光标所在位置
          let length = quill.getSelection().index;
          // 插入图片  res.info为服务器返回的图片地址
          quill.insertEmbed(length, 'image', res.url);
          // 调整光标到最后
          quill.setSelection(length + 1);
        } else {
          this.$message.error('图片插入失败');
        }
        // loading动画消失
        this.quillUpdateImg = false;
      },
      // 上传图片失败
      uploadError(res, file) {
        // loading动画消失
        this.quillUpdateImg = false;
        this.$message.error('图片插入失败');
      }
    }
  }
</script>
<style scoped>
  .editor-btn{
    margin-top: 20px;
  }
</style>
