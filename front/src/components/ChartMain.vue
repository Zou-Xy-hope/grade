<template>
    <div class="graph_container">
        <div v-for="graph in graphs" :key="graph.index" class="graph_main">
            <chart :width=500 :height=500 :graph=graph></chart>
        </div>
    </div>
</template>

<script>
import chart from './chart';

export default {
    components: {
        chart
    },
    props: {
        data: {
            type: Array
        },
        x: {
            type: String
        },
        y: {
            type: Array
        }
    },
    data() {
        return {
            xAxis: [],
            yAxis: [],
            graphs: [],
        }
    },
    mounted() {
        this.graph()
        this.getRot()
    },
    methods: {
        calcuX() {
            const datas = this.data;
            let xAxis = []
            for (let data of datas) {
                xAxis.push(data[this.x])
            }
            this.xAxis = xAxis
        },
        calcuY() {
            const datas = this.data;
            let total_y = [];
            for (let cols of this.y) {
                let y = []
                for (let data of datas) {
                    y.push(data[cols])
                }
                total_y.push(y)
            }
            this.yAxis = total_y
        },
        graph() {
            this.calcuX();
            this.calcuY();
            let graphs = []
            for (let i = 0; i < this.y.length; i++) {
                const x = this.x;
                const y = this.y[i];
                const x_val = this.xAxis;
                const y_val = this.yAxis[i]
                const title = x + "与" + y + '图'
                let graph = {
                    index: i+1,
                    title: title,
                    xAxis: x_val,
                    xname:x,
                    yname:y,
                    data: y_val,
                    legend: y
                }
                graphs.push(graph)
            }
            this.graphs = graphs
        },
        getRot(){
            const datas = this.data;
            const name = "ratting"
            let freq = {}
            for(let data of datas){
                const num = data[name]
                if(freq[num]){
                    freq[num]++;
                    continue;
                }
                else{
                    freq[num] = 1;
                }
            }
            const x = Object.keys(freq)
            const y = Object.values(freq)
            let graph = {
                    index: 0,
                    title: "评级分布图",
                    xAxis: x,
                    data: y,
                    legend: 'ratting'
                }
            this.graphs.push(graph)
        }
    }
}


</script>