<template>
  <div class="breadcrumb-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item
        v-for="(item, index) in breadcrumbList"
        :key="index"
        :to="item.path"
      >
        {{ item.title }}
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// 路由名称与中文标题映射表
const routeTitles = {
  'Home': '首页',
  'ActiveImages': '活动影像库',
  'ActiveImages-detail': '活动详情',
  'ActiveImages-edit': '编辑活动',
  'ActiveImages-upload': '上传活动',
  'ExcellentWorks': '优秀作业库',
  'ExcellentWorks-detail': '优秀作业详情',
  'ExcellentWorks-edit': '编辑作业',
  'ExcellentWorks-upload': '上传作业',
  'Interaction': '留言大厅',
  'AnonymousMessages-edit': '编辑留言',
  'AnonymousMessages-create': '上传留言',
  'Notice': '通知大厅',
  'Notice-edit': '编辑通知',
  'Notice-create': '上传通知',
  'Login': '用户登录',
  'Register': '用户注册'
} as Record<string, string>;

// 生成面包屑导航数据
const breadcrumbList = computed(() => {
  const pathSegments = route.path.split('/').filter(p => p);
  
  const items = [
    {
      title: routeTitles['Home'],
      path: '/'
    }
  ];

  pathSegments.forEach((segment, index) => {
    const fullPath = '/' + pathSegments.slice(0, index + 1).join('/');
    const matchedRoute = router.resolve(fullPath);
    
    if (matchedRoute.name === 'ActiveImages-detail') {
      items.push({
        title: routeTitles[matchedRoute.name as string],
        path: ''
      });
    } else if (routeTitles[matchedRoute.name as string]) {
      items.push({
        title: routeTitles[matchedRoute.name as string],
        path: index === pathSegments.length - 1 ? '' : fullPath
      });
    }
  });

  return items.filter(item => item.title);
});
</script>

<style scoped>
.breadcrumb-container {
  margin: 20px auto;
  max-width: 1200px;
  padding: 0 20px;
  padding-top: 60px;
  position: relative;
  z-index: 2;
}

.el-breadcrumb {
  --blur-intensity: 8px;
  --bg-opacity: 0.8;
  --item-spacing: 12px;
  font-size: 14px;
  font-weight: 500;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif;
  padding: 14px 24px;
  border-radius: 8px;
  backdrop-filter: blur(var(--blur-intensity));
  background: linear-gradient(
    135deg,
    rgba(134, 143, 255, 0.1) 0%,
    rgba(168, 129, 255, 0.1) 100%
  ),
  rgba(var(--el-bg-color-page), var(--bg-opacity));
  border: 1px solid var(--el-border-color-light);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.el-breadcrumb:hover {
  --bg-opacity: 0.9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.el-breadcrumb__item {
  display: inline-flex;
  align-items: center;
  transition: transform 0.2s ease;
}

.el-breadcrumb__item:not(:last-child)::after {
  margin: 0 var(--item-spacing);
  color: var(--el-text-color-placeholder);
  transition: opacity 0.3s;
}

.el-breadcrumb__item:hover {
  transform: translateY(-1px);
}

.el-breadcrumb__item:hover .el-breadcrumb__inner {
  color: var(--el-color-primary);
}

.el-breadcrumb__item:last-child .el-breadcrumb__inner {
  color: var(--el-text-color-regular);
  cursor: default;
  font-weight: 500;
}

/* 暗黑主题适配 */
.dark .el-breadcrumb {
  --bg-opacity: 0.6;
  border-color: var(--el-border-color);
  background: linear-gradient(
    135deg,
    rgba(94, 92, 230, 0.15) 0%,
    rgba(128, 81, 214, 0.15) 100%
  ),
  rgba(var(--el-bg-color-page), 0.6);
}

.dark .el-breadcrumb__item:last-child .el-breadcrumb__inner {
  color: var(--el-color-primary-light-5);
}

.dark .el-breadcrumb:hover {
  background: rgba(var(--el-bg-color-page), 0.7);
}
</style>