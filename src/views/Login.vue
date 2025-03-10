<!-- 
登录页面组件
功能：
- 用户登录表单提交及状态管理
- Token验证及用户信息展示
- 退出登录功能
-->
<template>
  <div id="page" class="site">
    <div class="container">
      <div class="login">
        <!-- 原有hero部分保持不变 -->
        <div class="hero">
          <h1>你好 世界<br>Hello World</h1>
          <p>如果你没有账号<br>可以<a href="/register"><strong style="color: var(--el-color-primary);">点击这里</strong></a>进行注册.</p>
        </div>

        <!-- 表单部分添加Vue数据绑定 -->
        <div class="main">
          <template v-if="!isLoggedIn">
            <!-- 在表单外部添加玻璃容器 -->
            <div class="glass-container">
              <h2 class="login-title">用户登录</h2>
              <form @submit.prevent="handleSubmit">
                <!-- 修改邮箱输入框结构 -->
                <div class="input-group">
                  <input
                    type="email"
                    placeholder=" "
                    v-model="formData.email"
                  >
                  <label>邮箱</label>
                </div>

                <!-- 修改密码输入框结构 -->
                <div class="input-group password">
                  <input
                    :type="showPassword ? 'text' : 'password'"
                    placeholder=" "
                    v-model="formData.password"
                    @focus="handleFocus"
                    @blur="handleBlur"
                    ref="passwordInput"
                  >
                  <label>密码</label>
                  <i
                    class="fa-solid fa-eye"
                    @click.stop="togglePasswordVisibility"
                    :class="{ 'fa-eye-slash': showPassword }"
                    v-show="shouldShowIcon"
                  ></i>
                </div>

                <!-- 保持原有提交按钮 -->
                <p>
                  <input type="submit" class="submit" value="登录">
                </p>
              </form>
            </div>
          </template>
          <template v-else>
            <div class="user-info">
              <el-descriptions title="用户信息" :column="1" border>
                <el-descriptions-item label="用户ID">{{ userInfo?.id }}</el-descriptions-item>
                <el-descriptions-item label="邮箱">{{ userInfo?.email }}</el-descriptions-item>
                <el-descriptions-item label="姓名">{{ userInfo?.name }}</el-descriptions-item>
                <el-descriptions-item label="身份">{{ userInfo?.identity === 'teacher' ? '教师' : '学生' }}</el-descriptions-item>
              </el-descriptions>
            </div>
            <form>
              <p class="logout-wrapper">
                <input 
                  type="button"
                  class="submit"
                  value="退出登录"
                  @click="handleLogout"
                >
              </p>
            </form>
          </template>
          <!-- 其他部分保持不变 -->
        </div>
      </div>
    </div>
  </div>
</template>

<!--
登录页面组件
功能：
- 用户登录表单提交及状态管理
- Token验证及用户信息展示
- 退出登录功能
-->
<script setup>
import Cookies from 'js-cookie';
import GlobalHeader from "@/components/GlobalHeader.vue";
import '@/assets/login_style.css'
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import Footer from "@/components/Footer.vue";

// 新增逻辑
// 密码输入框DOM引用
const passwordInput = ref(null)
const isFocused = ref(false)

const handleFocus = () => {
  isFocused.value = true
}

const handleBlur = () => {
  isFocused.value = false
}

const shouldShowIcon = computed(() => {
  return formData.value.password.length > 0 || isFocused.value
})

const isLoggedIn = ref(!!Cookies.get('userToken'));
const userInfo = ref(null);

const formData = ref({
  email: '',
  password: ''
})

/**
 * 验证用户Token有效性并获取用户信息
 * @returns {Promise<boolean>} 表示Token是否有效
 */
const verifyToken = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/users/userinfo', 
    {}, 
    {
      headers: {
        'Authorization': `Bearer ${Cookies.get('userToken')}`
      }
    });
    
    if (response.data.status === 'Success') {
      userInfo.value = response.data.data;
      // 成功获取用户信息后更新响应式对象
      return true;
    }
    return false;
  } catch (error) {
    if (error.response?.status === 401) {
      const message = error.response.data?.message || '认证失败';
      ElMessage.error(message.includes('过期') ? '登录已过期' : '无效的Token');
    } else if (error.response?.status === 404) {
      ElMessage.error('用户不存在');
    } else if (error.response?.status === 500) {
      ElMessage.error(`服务器错误: ${error.response.data?.message}`);
    }
    Cookies.remove('userToken');
    isLoggedIn.value = false;
    return false;
  }
};



const handleLogout = () => {
  Cookies.remove('userToken');
  isLoggedIn.value = false;
  ElMessage.success('已退出登录');
  router.push('/').then(() => {
    // 退出登录后刷新页面
    router.go(0);
  });
};

onMounted(async () => {
  if (isLoggedIn.value) {
    const isValid = await verifyToken();
    if (!isValid) {
      router.push('/login');
    }
  }
});

const showPassword = ref(false)

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const router = useRouter();
const route = useRoute();

/**
 * 处理登录表单提交
 * @param {Event} e - 表单提交事件对象
 * @returns {Promise<void>} 无返回值
 */
const handleSubmit = (e) => {
  e.preventDefault()
  // 发送登录请求
  axios.post('http://127.0.0.1:8000/api/users/login', {
    email: formData.value.email,
    password: formData.value.password
  })
  .then(response => {
    if (response.data.status === 'Success') {
      // 登录成功，设置cookie并显示成功消息
      Cookies.set('userToken', response.data.token);
      ElMessage.success('登录成功！');
      const fromRoute = route.query.from || '/';
      router.push(fromRoute).then(() => {
        // 使用路由刷新替代整页刷新
        router.go(0);
      });
    } else {
      // 根据不同的状态码显示不同的错误消息
      if (response.status === 401) {
        ElMessage.error(response.data.message);
      } else if (response.status === 404) {
        ElMessage.error(response.data.message);
      } else if (response.status === 400) {
        ElMessage.error(response.data.message);
      } else {
        ElMessage.error(response.data.message);
      }
    }
  })
  .catch(error => {
    // 显示错误消息
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        ElMessage.error(error.response.data.message);
      } else if (status === 404) {
        ElMessage.error(error.response.data.message);
      } else if (status === 400) {
        ElMessage.error(error.response.data.message);
      } else {
        ElMessage.error('登录失败，请稍后再试。');
      }
    } else {
      ElMessage.error('登录失败，请稍后再试。');
    }
  });
}
</script>

<style scoped>
/* 新增vue组件专用样式 */
#page {
  height: 100vh;
}

.user-info {
  position: relative;
  margin: 20px 0;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
  overflow: hidden;
}

.user-info::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid transparent;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

.el-descriptions__title {
  font-size: 18px;
  color: #303133;
}

.glass-container {
  position: relative;
  margin: 20px 0;
  padding: 30px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-container::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #6366f180 0%, #8b5cf680 50%, #ec489980 100%);
  z-index: -1;
  border-radius: 18px;
  animation: gradientBorder 8s ease infinite;
}

.user-info::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #6366f180 0%, #8b5cf680 50%, #ec489980 100%);
  z-index: -1;
  animation: gradientBG 8s ease infinite;
}

.login-title {
  text-align: center;
  margin: 20px 0 40px;
  font-size: 2.2em;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  /*color: transparent;*/
  animation: titleGlow 2s ease-in-out infinite alternate;
}

@keyframes gradientBorder {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes titleGlow {
  from { text-shadow: 0 0 10px rgba(99, 102, 241, 0.3); }
  to { text-shadow: 0 0 20px rgba(99, 102, 241, 0.6); }
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.submit {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
}
</style>