<script setup lang="ts">
</script>

<template>
  <a-layout id="container">
      <a-layout-sider v-if="hasMenu" width="200" style="background: #fff">
        <!-- <Menu /> -->
        <div></div>
      </a-layout-sider>
      <a-layout-content :style="{ margin: '16px 16px 0', overflow: 'initial' }">
        <a-card class="view-wrapper">
          <router-view v-if="isRouterAlive" />
        </a-card>
      </a-layout-content>
    </a-layout>
    <a-layout-footer id="footer" v-if="hasFooter" :style="{ textAlign: 'center' }">
      ArtonCtrl ©2023
    </a-layout-footer>
</template>

<script lang="ts">
export default {
  components: {
  },
  computed: {
    hasFooter(): boolean {
      const name = this.$router.currentRoute.value.name as string;
      return ["Index", "Overview", "Editor"].indexOf(name) > -1;
    },
    hasMainHeader(): boolean {
      const name = this.$router.currentRoute.value.name as string;
      return ["Index", "Overview", "Editor"].indexOf(name) > -1;
    },
    hasMenu(): boolean {
      const name = this.$router.currentRoute.value.name as string;
      return [""].indexOf(name) > -1;
    },
  },
  data() {
    return {
      isRouterAlive: true,
    }
  },
  methods: {
    reload() {
      const vm = this;
      vm.isRouterAlive = false;
      vm.$nextTick(() => {
        vm.isRouterAlive = true;
      });
    }
  },
  provide() {
    return {
      reload: this.reload,
    }
  },
};
</script>

<style scoped>
#container {
  height: 100%;
  max-height: calc(100vh - 24px);
}
#footer {
  height: 24px;
  background-color: #f5f5f5;
}
.view-wrapper {
  height: calc(100% - 5px);
}
</style>
