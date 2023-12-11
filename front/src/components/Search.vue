<template>
    <v-card>
        <v-card>
            <v-app-bar elevation="9" flat>
                <v-toolbar-title>
                    企业信息
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-text-field hide-details label="输入企业名" v-model="companyname"></v-text-field>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-bind="attrs" v-on="on" outlined @click="search">
                            <v-icon>mdi-magnify</v-icon>
                        </v-btn>
                    </template>
                    <span>搜索</span>
                </v-tooltip>
                <v-divider class="mx-4" vertical></v-divider>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-bind="attrs" v-on="on" :color="color" outlined @click="translateColor">
                            <v-icon>mdi-check-circle</v-icon>
                        </v-btn>
                    </template>
                    <span>图表显示</span>
                </v-tooltip>
                <v-spacer></v-spacer>
            </v-app-bar>
        </v-card>
        <v-divider></v-divider>
        <v-card elevation="0">
            <v-toolbar elevation="0">
                <v-icon color="blue darken-2">
                    {{ icon }}
                </v-icon>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>
            <v-divider></v-divider>
            <v-sheet>
                <ChartMain v-if="showChart" :data="this.datas" :x="'time'" :y="y"></ChartMain>
                <OneData v-if="showTable" :data="this.datas"></OneData>
            </v-sheet>
        </v-card>
    </v-card>
</template>

<script>
import ChartMain from './ChartMain'
import OneData from './OneData'

export default {
    data: () => ({
        graph: false,
        collapseOnScroll: true,
        color: '',
        colors: ['', 'green'],
        companyname: '',
        haveData: false,
        showChart: false,
        showTable: false,
        title: '信息表',
        icon: '',
        title: '信息表',
        icon: 'mdi-table-large',
        datas: [],
        y: ['ratting', 'ROA', 'ROE']
    }),
    methods: {
        translateColor() {
            this.graph = !this.graph;
            const index = this.graph ? 1 : 0;
            this.color = this.colors[index];
            this.handleshow();
        },
        async search() {
            if (!this.companyname) {
                return
            }
            const url = "http://127.0.0.1:5000/search/" + this.companyname
            const re = await this.axios.get(url);
            this.haveData = true;
            this.parse(re.data);
            this.handleshow();
        },
        parse(data) {
            let a = [];
            for (let d of data) {
                a.push(JSON.parse(d));
            }
            this.datas = a
        },
        handleshow() {
            const title = ['信息表', '图表'];
            const icon = ['mdi-table-large', 'mdi-chart-bar'];
            if (!this.haveData) {
                this.title = title[((title.indexOf(this.title) + 1) % title.length)];
                this.icon = icon[((icon.indexOf(this.icon) + 1) % icon.length)];
                return;
            }
            if (this.graph) {
                this.showTable = false;
                this.showChart = true;
                this.title = title[1];
                this.icon = icon[1];
                return
            }
            this.showChart = false;
            this.showTable = true;
            this.title = title[0];
            this.icon = icon[0];
        }
    },
    components: {
        ChartMain,
        OneData
    }
}
</script>