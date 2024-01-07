import Vue from 'vue'
import Router from 'vue-router'
import AllData from '@/components/AllData'
import ChartMain from '@/components/ChartMain'
import Search from '@/components/Search'
import Model from '@/components/Model'
import Predict from '@/components/Predict'
import Upload from '@/components/UploadFile'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/all',
      name: 'AllData',
      component: AllData
    },
    {
      path:'/search',
      name:'Search',
      component:Search
    },
    {
      path:'/chart',
      name: 'Chart',
      component: ChartMain
    },
    {
      path:'/model',
      name:'Model',
      component:Model
    },
    {
      path:'/predict',
      name:'Predict',
      component:Predict
    },
    {
      path:'/upload',
      name:'Upload',
      component:Upload
    }
  ]
})
