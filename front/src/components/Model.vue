<template>
    <v-card>
        <v-app-bar>
            <v-toolbar-title>模型展示</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>
        <v-divider></v-divider>
        <v-card>
            <div class="flex_display">
                <v-card width="300" height="500" class="flex_display_col center_display">
                    <div style="width: 250px;height: 100px;">
                        <v-text-field label="训练次数" v-model="epochs"></v-text-field>
                    </div>
                    <div>
                        <v-btn color="success" class="mt-12" @click="train()">训练</v-btn>
                    </div>
                    <v-overlay :absolute=true :value="overlay">
                        <v-progress-circular :rotate="360" :size="100" :width="15" :value="value" :color="color">
                            {{ value }}
                        </v-progress-circular>
                    </v-overlay>
                </v-card>
                <v-divider vertical></v-divider>
                <v-sheet width="800" height="500" class="flex_display center_display" v-if="showChart">
                    <chart :width=600 :height=400 :graph="graph"></chart>
                </v-sheet>
            </div>
        </v-card>
    </v-card>
</template>

<script>
import chart from './chart';
const acc_url = "http://127.0.0.1:5000/accuracy";


export default {
    data: () => ({
        showChart: false,
        overlay: false,
        interval: {},
        value: 0,
        color: 'red',
        epochs: '',
        datas: [],
        graph: {
            title: '准确率',
            legend: 'accuracy',
            xname: '迭代次数',
            yname: '准确率',
            xAxis: [],
            data: []
        },
    }),
    components: {
        chart
    },
    methods: {
        isNumber(str) {
            if (!str) {
                return false
            }
            const num = Number(str)
            return !(isNaN(num) || num == 0)
        },
        async train() {
            if (!this.isNumber(this.epochs)) {
                console.log('a')
                return;
            }
            this.overlay = true;
            const url = "http://127.0.0.1:5000/model/" + this.epochs;
            const re = await this.axios.get(url);
            if (re.status != '200') {
                this.overlay = false;
                return;
            }
            this.datas = [];
            this.showChart = true;
            const epochs = Number(this.epochs);
            this.getAccuracy(epochs);
        },
        async getAccuracy(epochs) {
            if (this.datas.length == epochs) {
                setTimeout(() => {
                    this.overlay = false;
                    this.value = 0;
                }, 1000)
                return
            }
            const re = await this.axios.get(acc_url);
            this.parse(re.data);
            this.calcu_graph();
            this.calcu_rate(epochs);
            setTimeout(() => {
                this.getAccuracy(epochs);
            }, 100);
        },
        parse(data) {
            let a = [];
            for (let d of data) {
                a.push(JSON.parse(d));
            }
            this.datas = a
        },
        calcu_rate(epochs) {
            this.value = Math.floor(this.datas.length / epochs * 100);
            if (this.value > 20 && this.value <= 50) {
                this.color = 'pink';
                return
            }
            if (this.value > 50 && this.value <= 80) {
                this.color = 'primary';
                return
            }
            if (this.value > 80) {
                this.color = 'green';
                return
            }
        },
        calcu_graph() {
            const datas = this.datas;
            let graph = {
                title: '测试次数与准确率图',
                legend: 'accuracy', 
                xname: '迭代次数/次',
                yname: '准确率/%',
            }
            let xAxis = [];
            let data = [];
            for (let i = 0; i < datas.length; i++) {
                xAxis.push(i + 1);
                data.push(datas[i].accuracy)
            }
            graph.xAxis = xAxis;
            graph.data = data;
            this.graph = graph;
        },
    }
}
</script>

<style scoped>
.v-progress-circular {
    margin: 1rem;
}
</style>