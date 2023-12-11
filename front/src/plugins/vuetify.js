import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css'

import '@mdi/font/css/materialdesignicons.css'
// import '@mdi/font/css/materialdesignicons.css'
// import 'vuetify/src/styles'

Vue.use(Vuetify);

export default new Vuetify({
    icons: {
      iconfont: "mdi" // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
      }
});
