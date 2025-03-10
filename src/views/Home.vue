<template>
  <div class="video-wrapper" :class="{ 'hide-video': isScrolled }">
    <div class="video-container">
      <video src="@/assets/bg.webm" loop autoplay muted class="vediostyle"></video>
    </div>
    <div class="video-text">
      <h1>欢迎来到班级文化服务栈</h1>
      <p>{{ hitokoto }}</p>
      <el-button 
  type="primary" 
  round 
  @click="scrollToContent"
  :class="{ 'dark-mode': isDark }"
  class="theme-button"
>
  开始使用
</el-button>
    </div>
  </div>
  <main class="content-container" ref="contentContainer">
    <el-carousel :interval="4000" type="card" height="400px" width="540px">
      <el-carousel-item :key="1">
        <img src="@/assets/zmd-3.png" alt="" width="100%">
      </el-carousel-item>
      <el-carousel-item :key="2">
        <img src="@/assets/zmd-1.png" alt="" width="100%">
      </el-carousel-item>
      <el-carousel-item :key="3">
        <img src="@/assets/zmd-2.png" alt="" width="100%"/>
      </el-carousel-item>
    </el-carousel>
    <div id="home">
      <div class="radius">
        <font-awesome-icon icon="fa-solid fa-bullhorn" class="icon-circle"/>
        <div>最新通知：<span v-html="noticeContent"></span></div>
      </div>
      <HomeRow></HomeRow>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useDark } from '@vueuse/core';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import HomeRow from "@/components/HomeRow.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";
import Footer from "@/components/Footer.vue";

const isScrolled = ref(false);
const isDark = useDark();
const hitokoto = ref('');
const noticeContent = ref('加载中...');
const apiBase = import.meta.env.VITE_API_BASE;

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10;
};

const fetchHitokoto = async () => {
  try {
    const response = await fetch('https://v1.hitokoto.cn/?c=d');
    const data = await response.json();
    hitokoto.value = data.hitokoto;
  } catch (error) {
    console.error('Error fetching hitokoto:', error);
    hitokoto.value = '在这里，我们致力于为您提供优质的服务和资源。';
  }
};

const contentContainer = ref<HTMLElement | null>(null)

const scrollToContent = () => {
  const target = document.getElementById('home');
  // 改用更可靠的选择器（对应GlobalHeader的class）
  const header = document.querySelector('.headfixed');
  
  if (target && header) {
    const headerHeight = header.offsetHeight;
    // 使用更精确的滚动位置计算
    const targetPosition = target.getBoundingClientRect().top + window.scrollY;
    
    window.scrollTo({
      top: 90,
      behavior: 'smooth'
    });
  } else {
    console.error('元素未找到:', { target, header });
  }
}

const fetchLatestNotice = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/notice/get`, {
      params: {
        page: 1,
        page_size: 1,
        order_by: '-timestamp'
      }
    });

    if (response.data.status === 'Success' && response.data.data.length > 0) {
      // 按时间戳降序排列后取最新通知
      const latestNotice = response.data.data.reduce((prev, current) => {
        return new Date(current.timestamp) > new Date(prev.timestamp) ? current : prev;
      });
      noticeContent.value = latestNotice.content;
    } else {
      noticeContent.value = '暂无通知';
    }
  } catch (error) {
    console.error('通知获取失败:', error);
    ElMessage.error('通知加载失败');
    noticeContent.value = '暂无通知';
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  fetchHitokoto();
  fetchLatestNotice();
  nextTick(() => {
    const header = document.querySelector('.headfixed');
    console.log('Header元素:', header);
    console.log('Header高度:', header?.offsetHeight);
  });
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
#home {
  scroll-margin-top: 80px;
}
.el-carousel {
  margin: 20px 0;
  border-radius: 16px;
  overflow: hidden;
  background: rgba(var(--el-bg-color), 0.6);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.el-carousel__item img {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
}

.el-carousel__item:hover img {
  transform: scale(1.03);
}

.radius {
  padding: 24px;
  margin: 10px 0;
  background: var(--card-gradient-light, linear-gradient(145deg, rgba(255,255,255,0.95), rgba(245,245,245,0.85)));
  backdrop-filter: blur(16px) saturate(160%);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.15);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.08),
    inset 0 0 12px rgba(255,255,255,0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.dark .radius {
  background: var(--card-gradient-dark);
  border-color: var(--card-border-dark);
  box-shadow: 
    0 4px 20px rgba(0,0,0,0.2),
    inset 0 0 15px rgba(255,255,255,0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dark .radius:hover {
  background: linear-gradient(135deg, rgba(26,26,47,0.9) 0%, rgba(45,26,62,0.9) 100%);
  backdrop-filter: brightness(1.1) saturate(130%);
  box-shadow: 
    0 6px 8px -1px rgba(0, 0, 0, 0.4),
    0 0 25px rgba(80, 80, 255, 0.3),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.radius > div {
  color: var(--el-text-color-primary);
  text-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.dark .radius:hover {
  background: linear-gradient(135deg, rgba(26,26,47,0.9) 0%, rgba(45,26,62,0.9) 100%);
  backdrop-filter: brightness(1.1) saturate(130%);
  box-shadow: 
    0 6px 8px -1px rgba(0, 0, 0, 0.4),
    0 0 25px rgba(80, 80, 255, 0.3),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.dark .radius > div {
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}



.icon-circle {
  --icon-size: 25px;
  width: var(--icon-size);
  height: var(--icon-size);
  padding: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.radius:hover .icon-circle {
  transform: translateY(-2px);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.15));
}

body[data-theme="dark"] .icon-circle {
  background: var(--icon-bg-dark, linear-gradient(145deg, rgba(80, 80, 255, 0.15), rgba(120, 120, 255, 0.1)));
  color: var(--icon-color-dark, #c1c1ff);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(163, 163, 255, 0.15);
  flex-shrink: 0;
  backdrop-filter: saturate(160%) blur(4px);
}

body[data-theme="light"] .icon-circle {
  background: var(--icon-bg-light, linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 245, 0.85)));
  color: var(--icon-color-light, var(--el-color-primary));
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  backdrop-filter: saturate(180%) blur(3px);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}
.radius > div {
  flex-shrink: 1;
  flex-grow: 1;
}
.video-wrapper {
  position: fixed;
  width: 100%;
  height: 100vh;
  transition: all 0.8s ease;
  z-index: 2;
  /* 移除此处的模糊效果 */
}
/* 调整视频容器的尺寸 */
.video-container {
  width: 110%;
  height: 110%;
  position: absolute;
  left: -5%;
  top: -5%;
  filter: blur(8px); /* 模糊转移到此处 */
  overflow: hidden;
  pointer-events: none;
}


.video-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  font-size: 2em;
}

/* 修正选择器语法错误和单位缺失 */
.video-wrapper.hide-video + .content-container {
  padding-top: 0;
  margin-top: 180px; /* 与Header高度保持一致 */
}

/* 添加全局布局调整 */
.content-container {
  position: relative;
  z-index: 1;
  padding-top: 100vh;
  transition: all 0.5s ease; /* 包含所有属性过渡 */
  min-height: calc(85vh + 1px);
  margin-top: 0;
}

/* 确保Header层级 */
.GlobalHeader {
  z-index: 100; /* 与Header组件保持一致 */
}

.hide-video {
  opacity: 0;
  transform: translateY(-100%);
}

.vediostyle {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.theme-button {
  --btn-bg-light: linear-gradient(145deg, #409eff, #3375b9);
  --btn-border-light: 1px solid rgba(255,255,255,0.15);
  --btn-shadow-light: 0 4px 20px rgba(64,158,255,0.15);
  padding: 15px 30px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  transform: translateY(0);
}

.theme-button:not(.dark-mode) {
  padding: 15px 30px;
  background: linear-gradient(145deg, rgba(26,26,47,0.9), rgba(45,26,62,0.9));
  border: 1px solid rgba(80,80,255,0.3);
  box-shadow: 0 0 15px rgba(80,80,255,0.2);
  color: rgba(255,255,255,0.92);
}

.theme-button.dark-mode {
  background: var(--btn-bg-light);
  border: var(--btn-border-light);
  box-shadow: var(--btn-shadow-light);
  color: rgba(255,255,255,0.95);
  padding: 15px 30px;
}

.theme-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(64,158,255,0.25);
}

.theme-button.dark-mode:hover {
  box-shadow: 0 0 25px rgba(80,80,255,0.4);
  filter: brightness(1.1);
}
</style>
