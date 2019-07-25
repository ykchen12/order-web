<style scoped>
  .ck-card {
    width: 400px;
    height: 100px;
  }
  .ck-title {
    height: 20px;
    line-height: 20px;
    text-align: center;
    font-style: initial;
    font-size: 14px;
  }
  .ck-content {
    margin-top: 10px;
    text-align: center;
    font-style: initial;
    font-size: 14px;
  }
</style>

<template>
  <div class="container">
    <div>
      <el-row :gutter="12">
        <el-col :span="6" v-for="(item, index) in workflows" :key="index" :value="item.id">
          <el-card class="ck-card box-card" shadow="hover">
              <template>
                <span class="ck-title">{{item.name}}</span>
                <hr>
                <span class="ck-content">{{item.description}}</span>
              </template>
            <!--<i class="el-icon-plus"></i>-->
              <p><el-button
                type="text"
                @click.prevent="handleWorkflow(item)"
              >新建工单</el-button></p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <Spin fix v-if="loading">
      <Icon type="load-c" size="50" class="demo-spin-icon-load"></Icon>
      <div style="font-size: 28px;">loading...</div>
    </Spin>
  </div>
</template>

<script>
import Validators from "../../utils/validators";
import { Date } from "../../utils/datetime";
import ueditor from "./components/ueditor";

export default {
  name: "new",
  components: {
    ueditor
  },
  data() {
    return {
      loading: false,
      workflows: [],
      accountList: [],
      workflow: null,
      init_state: {},
      workflowTitle: "",
      ueditorConfig: {}
    };
  },
  methods: {
    init() {
      this.loading = true;
      this.$store.dispatch("api_workflows").then(resp => {
        console.log(resp.data.data);
        this.workflows = resp.data.data.value;
        this.loading = false;
      });
    },
    handleWorkflow(workflow) {
      this.$router.push({
        // path: `/ticket/create/${workflow.id}/${workflow.value}`
        name: "create",
        params: { id: workflow.id, value: workflow.name }
      });
      // this.workflowTitle = workflow.value;
      // this.workflow = workflow.id;
      // this.loading = true;
      // this.$store
      //   .dispatch("api_init_state", { id: workflow.id })
      //   .then(resp => {
      //     this.init_state = resp.data.data;
      //     if (this.init_state.field_list) {
      //       this.$store.dispatch("api_fetch_account_list").then(resp => {
      //         this.accountList = resp.data.data;
      //         this.loading = false;
      //       });
      //     }
      //     this.loading = false;
      //   });
    },
    handleButton(formName, id) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          var data = {
            workflow_id: this.workflow,
            transition_id: id
          };
          Object.assign(data, this.newForm);
          for (
            let i = 0;
            i < Object.keys(this.init_state.field_list).length;
            i++
          ) {
            if (
              [25, 30].includes(this.init_state.field_list[i].field_type_id)
            ) {
              data[this.init_state.field_list[i].field_key] = data[
                this.init_state.field_list[i].field_key
              ].format("yyyy-MM-dd hh:mm:ss");
            }
            if ([70].includes(this.init_state.field_list[i].field_type_id)) {
              data[this.init_state.field_list[i].field_key] = data[
                this.init_state.field_list[i].field_key
              ].join(",");
            }
          }
          this.$store
            .dispatch("api_post_ticket", data)
            .then(resp => {
              this.$Notice.success({ title: "创建成功" });
              this.$router.push({ name: "myself" });
            })
            .catch(error => {
              this.$Notice.error({ title: "创建失败" });
            });
        } else {
          return false;
        }
      });
    },
    handleReady(instance) {
      instance.setContent("");
      instance.addListener("contentChange", () => {
        for (let i = 0; i < this.init_state.field_list.length; i++) {
          if (this.init_state.field_list[i].field_type_id === 55) {
            this.newForm[
              this.init_state.field_list[i].field_key
            ] = instance.getContent();
          }
        }
      });
    },
    reset(formName) {
      this.$refs[formName].resetFields();
    }
  },
  computed: {
    fieldEmpty() {
      for (let i in this.init_state.field_list) {
        return false;
      }
      return true;
    },
    newFormRules() {
      let validators = {};
      this.init_state.field_list.map(item => {
        if (item.field_attribute === 2) {
          if ([5, 35, 45, 55, 60].includes(item.field_type_id)) {
            validators[item.field_key] = [
              { validator: Validators.string, type: "string", trigger: "blur" }
            ];
          } else if ([25, 30].includes(item.field_type_id)) {
            validators[item.field_key] = [
              { validator: Validators.datetime, type: "date", trigger: "blur" }
            ];
          } else if ([40, 50, 70].includes(item.field_type_id)) {
            validators[item.field_key] = [
              { required: true, type: "array", trigger: "blur" }
            ];
          } else if ([10, 15].includes(item.field_type_id)) {
            validators[item.field_key] = [
              { validator: Validators.number, type: "number", trigger: "blur" }
            ];
          } else if (item.field_type_id === 20) {
            validators[item.field_type_id] = [
              { required: true, type: "boolean", trigger: "blur" }
            ];
          }
        }
      });
      return validators;
    },
    newForm() {
      let form = {};
      for (let i = 0; i < this.init_state.field_list.length; i++) {
        if (
          [40, 50, 70].includes(this.init_state.field_list[i].field_type_id)
        ) {
          form[this.init_state.field_list[i].field_key] = [];
        } else if (
          [10, 15].includes(this.init_state.field_list[i].field_type_id)
        ) {
          form[this.init_state.field_list[i].field_key] = 0;
        } else {
          form[this.init_state.field_list[i].field_key] = "";
        }
      }
      return form;
    }
  },
  created() {
    this.init();
  }
};
</script>

<style lang="less" scoped>
.new-form-con {
  margin-top: 15px;
}
.card {
  margin-top: 1%;
}
</style>
