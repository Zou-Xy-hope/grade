<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>{{ title }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 500px;">
          <v-container fluid v-for="data in dialogm" :key="data.value" column>
            <v-checkbox v-model="selected" :label="data.text" :value="data.value"></v-checkbox>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text v-if="show" @click="chooseAll()">
            全部勾选
          </v-btn>
          <v-btn color="blue darken-1" text v-if="!show" @click="cancelchooseAll()">
            取消全选
          </v-btn>
          <v-btn color="grey darken-1" text  @click="reset()">
            撤销
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close()">
            关闭
          </v-btn>
          <v-btn color="blue darken-1" text @click="save()">
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import Event from '../assets/js/Event';

export default {
  data() {
    return {
      dialogm: [],
      selected: [],
      init: [],
      dialog: false,
      show:true,
    }
  },
  methods: {
    do() {
      this.dialogm = this.datas;
      for (let data of this.datas) {
        if (data.choose) {
          this.selected.push(data.value);
        }
      }
      this.init = this.selected;
    },
    chooseAll(){
      const datas = this.datas;
      let select = [];
      for(let data of datas){
        select.push(data.value)
      }
      this.selected = select;
      this.show = false;
    },
    cancelchooseAll(){
      this.selected = [];
      this.show = true;
    },
    reset(){
      this.selected = this.init;
      this.show=true;
    },
    close() {
      this.selected = this.init;
      this.dialog = false;
    },
    save() {
      const datas = this.datas;
      const select = [];
      for (let data of datas) {
        if (this.selected.includes(data.value)) {
          select.push(data);
        }
      }
      this.init = this.selected;
      Event.$emit('header', select);
      this.dialog = false;
    }

  },
  mounted() {
    Event.$on('dialog', () => {
      this.dialog = true;
    });
    this.do()
  },
  props: {
    title: {
      type: String,
      defualt: '',
    },
    datas: {
      type: Array,
      default: () => []
    },
  },
}
</script>