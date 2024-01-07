<template>
    <v-card>
        <v-toolbar class="wbw_back">
            <v-toolbar-title>数据上传</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-divider></v-divider>
        <v-sheet class="flex_display center_display">
            <div class="box">
                <v-file-input v-model="file" accept=".csv,.xlsx,.xls" show-size counter
                    label="选择csv/xlsx/xls文件"></v-file-input>
                <v-btn color="success" class="mt-12" @click="validate">上传</v-btn>
                <div class="space"></div>
                <v-tooltip bottom :color="procolor">
                    <template v-slot:activator="{ on, attrs }">
                        <v-progress-linear :color="procolor" height="10" :value="progress" v-bind="attrs" v-on="on"
                            striped></v-progress-linear>
                    </template>
                    <span>上传进度:{{ progress }}%</span>
                </v-tooltip>

            </div>
        </v-sheet>
        <v-divider></v-divider>

        <div class="float">
            <v-expand-transition>
                <div v-show="show">
                    <v-alert width="300" :type="type">{{ message }}</v-alert>
                </div>
            </v-expand-transition>
        </div>
        <div class="flex_display center_display">
            <v-sheet width="48%" height="300">
                <div style="width:100%;margin-top: 20px;gap: 20px;" class="flex_display_col center_display">
                    <h2>评级结果</h2>
                    <v-tooltip bottom :color="color">
                        <template v-slot:activator="{ on, attrs }">
                            <v-sheet width="150" height="150" v-bind="attrs" v-on="on">
                                <v-progress-circular :rotate="360" :size="120" :width="15" :value="value" :color="color">{{
                                    grade ?
                                    grade
                                    : '请上传数据' }}</v-progress-circular>
                            </v-sheet>
                        </template>
                        <span>{{ ratting == 0 ? '暂无评级' : ratting }}</span>
                    </v-tooltip>
                </div>
            </v-sheet>
        </div>
    </v-card>
</template>

<style>
.box {
    width: 600px;
    height: 250px;
    padding: 10px;
}

.space {
    width: 100%;
    height: 30px;
}

.float {
    position: absolute;
    top: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>

<script>


export default {
    data() {
        return {
            message: 'asdf',
            type: 'success',
            ratting: 0,
            color: 'grey',
            procolor: 'grey',
            progress: 0,
            show: false,
            value: 0,
            grade: '',
            file: null,
            pre: '0',
            dic: {
                1: 'C', 2: 'CC',
                3: 'CCC', 4: 'B-',
                5: 'B', 6: 'B+',
                7: 'BB-', 8: 'BB',
                9: 'BB+', 10: 'BBB-',
                11: 'BBB', 12: 'BBB+',
                13: 'A-', 14: 'A',
                15: 'A+', 16: 'AA-',
                17: 'AA', 18: 'AA+',
                19: 'AAA'
            },
        }
    },
    mounted() {
    },
    methods: {
        notice(msg, type = 'success', duration = 1000) {
            this.type = type;
            this.message = msg;
            this.show = true;
            setTimeout(() => {
                this.show = false;
            }, duration)
        },
        get_color(rate) {
            //红：rgb(255,0,0) 绿：rgb(0,255,0)
            const r = Math.floor(255 * (1 - rate))
            const g = Math.floor(255 * rate)
            return 'rgb(' + r + ',' + g + ',0)'
        },
        validate() {
            if (!this.file) {
                this.notice('请选择文件', 'warning');
                return
            }
            const accept = ["csv", "xlsx", "xls"];
            const name = this.file.name.split('.').pop();
            if (!accept.includes(name)) {
                this.notice('文件格式不对', 'warning');
            }
            this.submit()

        },
        async submit() {
            const url = this.port + "file";
            const that = this;
            const form = new FormData();
            form.append("file", this.file);
            const re = await this.axios.post(url, form, {
                onUploadProgress: e => {
                    that.progress = Math.floor(e.loaded / e.total * 100);
                    that.procolor = that.get_color(that.progress / 100);
                }
            })
            if (re.status == 200) {
                this.notice('上传成功')
                const token = re.data;
                this.result(token);
            }
        },
        async result(token) {
            const url = this.port + "/predict/" + token;
            const re = await this.axios.get(url)
            if (re.data.code == 200) {
                const a = Number(re.data.data);
                this.ratting = a;
                this.grade = this.dic[a];
                this.value = (a - 1) / 18 * 100;
                this.color = this.get_color(this.value / 100)
                return;
            }
            setTimeout(() => {
                this.result(token);
            }, 2000)
        }
    }
}
</script>