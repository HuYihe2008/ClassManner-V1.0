<template>
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo headfixed"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
  >
    <el-menu-item>
      <img
        style="width: 50px"
        src="@/assets/1.png"
        alt="Element logo"
      />
    </el-menu-item>
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/login">用户中心</el-menu-item>
    <el-menu-item v-if="userEmail">
      <el-avatar 
        :size="40"
        :src="qqAvatarUrl || defaultAvatar"
        @error="handleAvatarError"
      />
      <!--<span class="user-email">{{ userEmail }}</span>-->
    </el-menu-item>
    <el-menu-item v-if="userEmail" @click="handleLogout">
      退出登录
    </el-menu-item>
    <el-menu-item @click="toggleDarkMode">
      <el-icon>
        <component :is="isDark ? Moon : Sunny" />
      </el-icon>
      {{ isDark ? '暗黑模式' : '明亮模式' }}
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import {defineComponent, onMounted, onUnmounted, ref, watch} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDark } from '@vueuse/core'
import { Moon, Sunny } from '@element-plus/icons-vue' // 新增图标导入
import axios from 'axios';
import Cookies from 'js-cookie';
import { ElMessage } from 'element-plus';

const defaultAvatar = ref('@/assets/default-avatar.png');
const userEmail = ref('');
const userRole = ref('');
const qqAvatarUrl = ref('');

const handleLogout = () => {
  Cookies.remove('userToken');
  userEmail.value = '';
  qqAvatarUrl.value = '';
  ElMessage.success('已退出登录');
};

const fetchUserInfo = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/users/userinfo', 
    {}, 
    {
      headers: {
        'Authorization': `Bearer ${Cookies.get('userToken')}`
      }
    });

    if (response.data.status === 'Success') {
      userEmail.value = response.data.data.email || '';
      userRole.value = response.data.data.identity || 'student';
      console.log('用户信息响应:', response.data);
      console.log('用户信息获取成功', userEmail.value);
      if (userEmail.value.endsWith('@qq.com')) {
        const qqNumber = userEmail.value.split('@')[0];
        await fetchQQAvatar(qqNumber);
        console.log('QQ头像获取成功',qqNumber);
      }
    }
  } catch (error) {
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录');
      handleLogout();
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      ElMessage.error('获取用户信息失败');
    }
  }
};

const fetchQQAvatar = async (qq: string) => {
  try {
    const response = await axios.get(`/api/proxy/api/qqname?qq=${qq}`);
    if (response.data.code === 200) {
      qqAvatarUrl.value = response.data.data.imgurl;
    }
  } catch (error) {
    ElMessage.warning('QQ头像获取失败，使用默认头像');
  }
};

const handleAvatarError = () => {
  qqAvatarUrl.value = defaultAvatar.value;
};

// 在组件挂载时获取用户信息
const watchToken = watch(() => Cookies.get('userToken'), () => {
  if (Cookies.get('userToken')) {
    fetchUserInfo();
  }
});

onMounted(() => {
  if (Cookies.get('userToken')) {
    fetchUserInfo();
  }
});

onUnmounted(() => {
  watchToken();
});

const activeIndex = ref('/')
const router = useRouter()
const route = useRoute()
const isDark = useDark()


// 监听路由变化，更新 activeIndex
watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
}, { immediate: true })

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
  router.push(key)
}

const toggleDarkMode = () => {
  isDark.value = !isDark.value
}

const get_user_avatar = async () => {
  
}
</script>

<style>/* 全局定义变量 */
:root {
  --header-bg-light: #ffffff;
  --header-bg-dark: #1a1a1a;
}
</style>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
a {
  text-decoration: none;
}
.headfixed {
  position: fixed;
  height: 60px;
  background: rgba(var(--el-bg-color), 0.8);
  transition: background 0.3s cubic-bezier(0.4, 0, 0.2, 1), backdrop-filter 0.3s;
  backdrop-filter: blur(10px) saturate(180%);
  -webkit-backdrop-filter: blur(10px) saturate(180%);
  z-index: 1000;
  left: 0;
  top: 0;
  right: 0;
  width: 100%;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.el-menu--horizontal {
  --el-menu-active-color: #6366f1;
  --el-menu-hover-bg-color: rgba(99, 102, 241, 0.1);
}

.el-menu-item {
  transition: all 0.2s ease-in-out;
  margin: 0 8px;
  border-radius: 8px;
}

.el-menu-item:not(.is-active):hover {
  background: linear-gradient(to right, rgba(99, 102, 241, 0.1), rgba(165, 180, 252, 0.1));
  transform: translateY(-2px);
}
</style>