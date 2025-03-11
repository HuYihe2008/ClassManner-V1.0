<script setup lang="ts">
import { useDark, useWindowSize } from '@vueuse/core'
import { watch, onUnmounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import { debounce } from 'lodash'
import Footer from "@/components/Footer.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";

const isDark = useDark()
const { width: windowWidth } = useWindowSize()

const checkWindowSize = () => {
  if (windowWidth.value < 1200) {
    ElMessageBox.alert('当前窗口宽度不足1200px，部分内容可能显示异常', '屏幕宽度提示', {
      confirmButtonText: '确认',
      callback: () => {},
    })
  }
}

const stopWatch = watch(windowWidth, debounce(() => {
  checkWindowSize()
}, 300), { immediate: true })

onUnmounted(() => {
  stopWatch()
})
</script>

<template>
  <GlobalHeader/>
  <div :class="isDark ? 'dark' : 'light'">
    <router-view></router-view>
    <Footer/>
  </div>
</template>

<style scoped>
.dark {
  background-color: #121212;
  color: #ffffff;
}
.light {
  background-color: #ffffff;
  color: #000000;
}
</style>