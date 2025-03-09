<template>
  <div id="page" class="site">
    <div class="container">
      <div class="login">
        <!-- 原有hero部分保持不变 -->
        <div class="hero">
          <h1>你好 世界<br>Hello World</h1>
          <p>如果你没有账号<br>可以<a href="/register">点击这里</a>进行注册.</p>
        </div>

        <!-- 表单部分添加Vue数据绑定 -->
        <div class="main">
          <template v-if="!isLoggedIn">
            <form @submit.prevent="handleSubmit">
            <p>
              <input
                  type="email"
                  placeholder="邮箱"
                  v-model="formData.email"
              >
            </p>
            <!-- 修改密码输入部分 -->
            <p class="password">
              <input
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="密码"
                  v-model="formData.password"
                  @focus="handleFocus"
                  @blur="handleBlur"
                  ref="passwordInput"
              >
              <i
                  class="fa-solid fa-eye"
                  @click.stop="togglePasswordVisibility"
                  :class="{ 'fa-eye-slash': showPassword }"
                  v-show="shouldShowIcon"
              ></i>
              <a href="#">找回密码</a>
            </p>
            <p>
              <input type="submit" class="submit" value="登录">
            </p>
          </form>
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
      console.log('用户信息获取成功', userInfo.value);
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
  router.push('/');
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
      router.push(fromRoute);
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
  margin: 20px 0;
  padding: 20px;
  border-radius: 4px;
}

.el-descriptions__title {
  font-size: 18px;
  color: #303133;
}

.login-wrapper {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px) saturate(180%);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.login-wrapper::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  z-index: -1;
  animation: gradientBG 8s ease infinite;
  background-size: 200% 200%;
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