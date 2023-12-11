<template>
  <v-card height="100%" width="256" class="mx-auto">
    <v-navigation-drawer permanent>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            可视化
          </v-list-item-title>
          <v-list-item-subtitle>
            小组
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item v-for="item in items" :key="item.title" link @click="click(item)">
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn block>
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      selectedItem: 0,
      items: [
        { title: '数据库', icon: 'mdi-database-eye-outline', router: '/all' },
        { title: '企业信息', icon: 'mdi-magnify-expand', router: '/search' },
        { title: '模型使用', icon: 'mdi-alpha-m-circle-outline', router: '/model' },
      ],
    }
  },
  methods: {
    click: function (item) {
      this.selectedItem = this.items.indexOf(item);
      if (this.$route.path != item.router) {
        this.$router.replace(item.router)
      }
    }
  }
}
</script>