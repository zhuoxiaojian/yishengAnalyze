<template>
    <div class="">
            <el-tabs v-model="message">
                <el-tab-pane :label="`未读消息(${unread.length})`" name="first">
                    <el-table :data="unread" :show-header="false" style="width: 100%" higlight-current-row>
                        <el-table-column prop="id" v-if="show"></el-table-column>
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title">{{scope.row.message_info}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="create_date" :formatter="dateFormat"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button size="small" @click="handleRead(scope.$index, scope.row)">标为已读</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="primary" @click="handleAllToRead">全部标为已读</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane :label="`已读消息(${read.length})`" name="second">
                    <template v-if="message === 'second'">
                        <el-table :data="read" :show-header="false" style="width: 100%" higlight-current-row>
                            <el-table-column prop="id" v-if="show"></el-table-column>
                            <el-table-column >
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.message_info}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="create_date" :formatter="dateFormat"></el-table-column>
                            <el-table-column >
                                <template slot-scope="scope">
                                    <el-button type="danger" @click="handleDel(scope.$index, scope.row)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger" @click="handleRecycleAll">删除全部</el-button>
                        </div>
                    </template>
                </el-tab-pane>
                <el-tab-pane :label="`回收站(${recycle.length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="recycle" :show-header="false" style="width: 100%"higlight-current-row>
                            <el-table-column prop="id" v-if="show"></el-table-column>
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.message_info}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="create_date" :formatter="dateFormat"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button @click="handleRestore(scope.$index, scope.row)">还原</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger" @click="handleDeleteAll">清空回收站</el-button>
                        </div>
                    </template>
                </el-tab-pane>
            </el-tabs>

    </div>
</template>

<script>
    import axios from '../../../utils/axiosConfig'
    import baseHost from '../../../api/baseHost'
    export default {
        name: 'tabs-info',
        data() {
            return {
                show: false,
                message: 'first',
                showHeader: false,
                unread: [],
                read: [],
                recycle: []
            }
        },
        methods: {
          dateFormat(row, column){
            if(row.create_date == null){
              return '';
            }
            let time = new Date(row.create_date);
            return `${time.getFullYear()}-${time.getMonth() + 1 >= 10 ? (time.getMonth() + 1) : '0' + (time.getMonth() + 1)}-${time.getDate() >= 10 ? time.getDate() : '0' + time.getDate()}
                        ${time.getHours() >= 10 ? time.getHours() : '0' + time.getHours()} : ${time.getMinutes()>=10?time.getMinutes():'0'+time.getMinutes()} : ${time.getSeconds() >= 10 ? time.getSeconds() : '0' + time.getSeconds()}`;
          },
            handleMethod(params){
                let that = this;
                let handleUrl = baseHost + '/systemMessage/getSystemMessage/';
                axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
                axios.post(handleUrl, JSON.stringify(params),{
                    headers:{
                        'Content-Type': 'application/json;charset=UTF-8'
                    }
                }).then((response)=>{
                    that.initMessage();
                }).catch(()=>{

                });
            },
            handleRead(index, row) {
                //const item = this.unread.splice(index, 1);
                //this.read = item.concat(this.read);
                let params = {dataParams: row.id, methodParams: 'unreadToread'};
                this.handleMethod(params);
            },
            handleDel(index, row) {
                //const item = this.read.splice(index, 1);
                //this.recycle = item.concat(this.recycle);
                let params = {dataParams: row.id, methodParams: 'readToRecycle'};
                this.handleMethod(params);
            },
            handleRestore(index, row) {
                //const item = this.recycle.splice(index, 1);
                //this.read = item.concat(this.read);
                let params = {dataParams: row.id, methodParams: 'recycleToRead'};
                this.handleMethod(params);
            },
            handleDeleteAll(){
                let datas = this.recycle;
                let ids = "";
                if(datas.length > 0){
                    for(let i=0; i < datas.length; i++){
                        ids = ids+datas[i].id+",";
                    }
                    if(ids != ''){
                        ids = ids.substr(0,ids.length-1);
                        let params = {dataParams: ids, methodParams: 'recycleToDeleteAll'};
                        this.handleMethod(params);
                    }
                }
            },
            handleRecycleAll(){
                let datas = this.read;
                let ids = "";
                if(datas.length > 0){
                    for(let i=0; i < datas.length; i++){
                        ids = ids+datas[i].id+",";
                    }
                    if(ids != ''){
                        ids = ids.substr(0,ids.length-1);
                        let params = {dataParams: ids, methodParams: 'readToRecycleAll'};
                        this.handleMethod(params);
                    }
                }
            },
            handleAllToRead(){
                let datas = this.unread;
                let ids = "";
                if(datas.length > 0){
                    for(let i=0; i < datas.length; i++){
                        ids = ids+datas[i].id+",";
                    }
                    if(ids != ''){
                        ids = ids.substr(0,ids.length-1);
                        let params = {dataParams: ids, methodParams: 'allToRead'};
                        this.handleMethod(params);
                    }
                }
            },
            initMessage(){
                //获取消息
                let getMessageCountUrl = baseHost + '/systemMessage/getSystemMessage/';
                let that = this;
                axios.get(getMessageCountUrl, {params: {flagParams: '0,1,2'}}).then((response)=>{
                    let json_list = response.data.resultData; //list集合
                    for(let i=0; i < json_list.length; i++){
                        if(json_list[i].hasOwnProperty('flag0')){
                            that.unread = json_list[i].flag0.flag0Data;
                        }
                        if(json_list[i].hasOwnProperty('flag1')){
                            that.read = json_list[i].flag1.flag1Data;
                        }
                        if(json_list[i].hasOwnProperty('flag2')){
                            that.recycle = json_list[i].flag2.flag2Data;
                        }
                    }

                }).catch(()=>{

                });
            }
        },
        mounted(){
            this.initMessage();
        },
        computed: {
            unreadNum(){
                return this.unread.length;
            }
        }
    }

</script>

<style>
.message-title{
    cursor: pointer;
}
.handle-row{
    margin-top: 30px;
}
</style>

