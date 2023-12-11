<template>
    <v-card>
        <div ref="main">
        </div>
        <v-card-text>
            <v-chip-group v-model="index" active-class="deep-purple accent-4 white--text" column>
                <v-chip @click="change(0)">line</v-chip>

                <v-chip @click="change(1)">bar</v-chip>

                <v-chip @click="change(2)">pie</v-chip>

                <v-chip @click="change(3)">scatter</v-chip>
            </v-chip-group>
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    data() {
        return {
            type: 'bar',
            index:1,
            myChart: {}
        }
    },
    mounted() {
        this.draw()
    },
    methods: {
        draw() {
            const dom = this.$refs.main;
            dom.style.width = this.width + 'px';
            dom.style.height = this.height + 'px'
            this.myChart = this.$echarts.init(dom);
            const option = {
                title: {
                    text: this.graph.title
                },
                tooltip: {},
                legend: {
                    data: [this.graph.legend]
                },
                xAxis: {
                    data: this.graph.xAxis,
                    name: this.graph.xname
                },
                yAxis: {
                    name: this.graph.yname
                },
                series: [{
                    name: this.graph.legend,
                    type: this.type,
                    data: this.graph.data
                }]
            };
            this.myChart.setOption(option);
        },
        redraw(){
            const option = {
                title: {
                    text: this.graph.title
                },
                tooltip: {},
                legend: {
                    data: [this.graph.legend]
                },
                xAxis: {
                    data: this.graph.xAxis,
                    show: this.type !='pie'
                },
                yAxis: {
                    show: this.type !='pie'
                },
                series: [{
                    name: this.graph.legend,
                    type: this.type,
                    data: this.graph.data
                }]
            };
            this.myChart.setOption(option);

        },
        change(index){
            const types =['line','bar','pie','scatter']
            this.type= types[index]
            this.redraw()
        }

    },
    props: {
        width: {
            type: Number,
            default: 200
        },
        height: {
            type: Number,
            default: 200
        },
        graph: {
            type: Object,
            default: () => { }
        },

    },
    watch:{
        graph(newval,oldval){
            this.graph = newval;
            this.redraw();
        }
    }
}
</script>