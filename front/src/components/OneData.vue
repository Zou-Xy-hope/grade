<template>
    <v-card class="overflow-y-auto">
    <v-data-table :headers="headers" :items="desserts" :items-per-page="10" class="elevation-1"></v-data-table>
  </v-card>
  </template>
  
  
  <script>
  export default {
    data: () => ({
      headers: [
        {
          text: 'time',
          align: 'start',
          sortable: false,
          value: 'time',
        },
        { text: '公司名称', value: 'company' },
        { text: '证券代码', value: 'company_code' },
        { text: '评级', value: 'ratting' },
        { text: 'ROA', value: 'ROA' },
        { text: 'ROE', value: 'ROE' },
        { text: '总资产', value: 'total_asset' },
        { text: '总负债', value: 'total_liabilities' }
      ],
      desserts: []
    }),
    mounted() {
      this.load_data()
    },
    methods: {
      load_data(){
        this.desserts = this.data;
      }
    },
    props:{
        data:{
            type:Array,
            default:()=>[]
        }
    }
  }
  </script>