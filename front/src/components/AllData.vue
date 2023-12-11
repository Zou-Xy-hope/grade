<template>
  <v-card>
  <v-card class="overflow-y-auto">
    <v-app-bar>
      <v-toolbar-title>数据库信息表</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tooltip left>
      <template v-slot:activator="{ on, attrs }">
      <v-btn icon large v-bind="attrs"
          v-on="on" @click="show()"><v-icon dark>mdi-cog-outline</v-icon></v-btn>
      </template>
      <span>表头设置</span>
      </v-tooltip>
    </v-app-bar>
    <v-data-table :headers="headers" :items="desserts" :items-per-page="10" class="elevation-1">
    </v-data-table>
  </v-card>
  <Dialog :title="'选择表头'" :datas="dics"></Dialog>
</v-card>
</template>


<script>
import Dialog from './dialog';
import Event from '../assets/js/Event';
export default {
  data: () => ({
    headers: [
      {
        text: 'time',
        align: 'start',
        sortable: false,
        value: 'time',
      },
      { text: '证券名称', value: 'company' },
      { text: '证券代码', value: 'company_code' },
      { text: '评级', value: 'ratting' },
      { text: 'ROA', value: 'ROA' },
      { text: 'ROE', value: 'ROE' },
      { text: '资产总计', value: 'total_asset' },
      { text: '负债总计', value: 'total_liabilities' }
    ],
    desserts: [],
    dics: [
      { text: 'time', value: 'time', choose: true },
      { text: '证券名称', value: 'company', choose: true },
      { text: '证券代码', value: 'company_code', choose: true },
      { text: '证券类型', value: 'company_type', choose: true },
      { text: '评级', value: 'ratting', choose: true },
      { text: 'ROA', value: 'ROA', choose: true },
      { text: 'ROE', value: 'ROE', choose: true },
      { text: '资产总计', value: 'total_asset', choose: true },
      { text: '资产负债率', value: 'asset_liability_ratio', choose: true },
      { text: '流动比率', value: 'current_ratio', choose: false },
      { text: '有形净值债务率', value: 'tangible_equity_debt_ratio', choose: false },
      { text: '负债合计', value: 'total_liabilities', choose: false },
      { text: '单季度利润总额', value: 'total_profit_per_quarter', choose: false },
      { text: '单季度投资活动产生现金净额', value: 'sq_net_cash_flows', choose: false },
      { text: '单季度营业收入', value: 'sq._operating_income', choose: false },
      { text: '资本收益率', value: 'return_on_capital', choose: false }
    ],
    dialog: false,
  }),
  mounted() {
    this.load_data();
    Event.$on('header',(headers)=>{
      this.headers = headers;
    })
  },
  methods: {
    async load_data() {
      const url = "http://127.0.0.1:5000/showall";
      const re = await this.axios.get(url);
      this.parse(re.data)
    },
    parse(data) {
      let a = [];
      for (let d of data) {
        a.push(JSON.parse(d));
      }
      this.desserts = a
    },
    show(){
      Event.$emit('dialog',true)
    }
  },
  components:{
    Dialog,
  }
}
</script>