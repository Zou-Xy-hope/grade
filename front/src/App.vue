<template>
    <v-app>
      <v-navigation-drawer app>
        <Menu></Menu>
      </v-navigation-drawer>

      <v-app-bar app>
        <!-- -->
      </v-app-bar>

      <!-- 根据应用组件来调整你的内容 -->
      <v-main>
        <!-- 给应用提供合适的间距 -->
        <v-container fluid>
          <!-- 如果使用 vue-router -->
          <router-view></router-view>
        </v-container>
      </v-main>

      <!-- <v-footer app>
        
      </v-footer> -->
    </v-app>
</template>

<script>
import Menu from './components/Menu';

export default {
  name: 'App',
  components:{
    Menu
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
