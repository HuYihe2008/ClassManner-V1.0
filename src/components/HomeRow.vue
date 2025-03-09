<template>
  <el-row :gutter="10" class="el-row-me">
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" @click="router.push('/activeimages')">
        <font-awesome-icon icon="fa-solid fa-image fa-3x" class="iconsize"/>
        <div class="divsize">
          <h2>
            活动影像库
          </h2>
          <p>记录美好校园日常</p>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" @click="router.push('/excellentworks')">
        <font-awesome-icon :icon="['far', 'pen-to-square']" class="iconsize"/>
        <div class="divsize">
          <h2>
            优秀作业库
          </h2>
          <p>展示优秀作业</p>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" @click="router.push('/interaction')">
        <font-awesome-icon :icon="['fas', 'user-secret']" class="iconsize"/>
        <div class="divsize">
          <h2>
            留言大厅
          </h2>
          <p>匿名互动</p>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" @click="router.push('/notice')">
        <font-awesome-icon icon="fa-solid fa-bullhorn" class="iconsize"/>
        <div class="divsize">
          <h2>
            通知大厅
          </h2>
          <p>日常消息通知</p>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, watch } from 'vue';
import { useDark } from '@vueuse/core';
import { useRouter, useRoute } from 'vue-router';

export default defineComponent({
  setup() {
    const isDark = useDark();
    const route = useRoute();
    const router = useRouter();

    const setTheme = (dark: boolean) => {
      document.body.setAttribute('data-theme', dark ? 'dark' : 'light');
    };

    onMounted(() => {
      setTheme(isDark.value);
    });

    watch(isDark, (dark) => {
      setTheme(dark);
    });

    onUnmounted(() => {
      document.body.removeAttribute('data-theme');
    });

    return {
      router
    };
  }
});
</script>

<style>
:root {
  --card-gradient-light: linear-gradient(135deg, rgba(204,235,255,0.85) 0%, rgba(229,204,255,0.85) 100%);
  --card-gradient-dark: linear-gradient(135deg, rgba(15,15,45,0.9) 0%, rgba(60,20,80,0.9) 100%);
  --card-border-light: rgba(0, 0, 0, 0.08);
  --card-border-dark: rgba(255, 255, 255, 0.08);
}

body[data-theme="dark"] {
  --homerowbackground-color: var(--homerowbackground-color-dark);
}

body[data-theme="light"] {
  --homerowbackground-color: var(--homerowbackground-color-light);
}

.el-row {
  margin-top: 10px !important;
}

.el-col {
  border-radius: 4px;
  margin: 0;
}
.el-row-me {
  margin: 20px 0;
}

.grid-content {
  padding: 20px;
  border-radius: 12px;
  background: 
    var(--card-gradient-light),
    rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(150, 150, 150, 0.15);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 20px;
}

body[data-theme="dark"] .grid-content {
  background:
    var(--card-gradient-dark),
    rgba(42, 42, 42, 0.85);
  border-color: var(--card-border-dark);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

body[data-theme="dark"] .grid-content:hover {
  background:
    linear-gradient(135deg, rgba(26,26,47,0.9) 0%, rgba(45,26,62,0.9) 100%),
    rgba(70, 70, 90, 0.95);
  backdrop-filter: brightness(1.1) saturate(130%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.grid-content:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  background: 
    var(--card-gradient-light),
    rgba(255, 255, 255, 0.85);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease;
}

.iconsize {
  color: var(--el-color-primary);
  margin-bottom: 10px;
}

.divsize h2 {
  color: #2c3e50;
  margin-bottom: 8px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

body[data-theme="dark"] .divsize h2 {
  color: #f0f0f0;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.1);
}

.divsize p {
  color: var(--el-text-color-secondary);
  font-size: 0.9em;
}

/* 暗黑模式适配 */
.dark .grid-content {
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 30, 30, 0.6);
}

.dark .grid-content:hover {
  background: rgba(30, 30, 30, 0.8);
}
.iconsize{
  --icon-size: 30px;
  width: var(--icon-size);
  height: var(--icon-size);
  margin-bottom: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.grid-content {
  gap: 15px;
}

.grid-content:hover .iconsize {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.15));
}

body[data-theme="dark"] .iconsize {
  color: var(--icon-color-dark, #a3a3ff);
}

body[data-theme="light"] .iconsize {
  color: var(--icon-color-light, var(--el-color-primary));
  font-size: 30px;
  margin-left: 0;
  flex-shrink: 0;
}
.divsize{
  margin-left: 0;
}
</style>