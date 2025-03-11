<template>
  <div id="page" class="site">
    <div class="container">
      <div class="login">
        <div class="hero">
          <h1>你好 世界<br>Hello World</h1>
          <p>已有账号？<router-link to="/login"><strong style="color: var(--el-color-primary);">立即登录</strong></router-link></p>
        </div>

        <!-- 表单部分添加Vue数据绑定 -->
        <div class="main">
          <template v-if="!isLoggedIn">
            <div class="glass-container">
              <form @submit.prevent="handleSubmit">
                <h2 class="login-title">用户注册</h2>
                <p>
                  <input
                      type="email"
                      placeholder="邮箱"
                      v-model="formData.email"
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
                  </p>
                  <!-- 在原有模板的email输入框下方添加 -->
                  <p>
                    <input
                      type="text"
                      placeholder="姓名"
                      v-model="formData.name"
                  >
                  </p>
                  <!-- 在密码输入框上方添加下拉选择 -->
                  <p>
                    <el-select
                      v-model="formData.identity"
                      placeholder="请选择身份"
                      style="width: 100%"
                      clearable
                    >
                      <el-option label="教师" value="teacher" />
                      <el-option label="学生" value="student" />
                    </el-select>
                  </p>
                  <!-- 修改提交按钮文字 -->
                  <input type="submit" class="submit" value="注册">
                </form>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Cookies from 'js-cookie';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import GlobalHeader from "@/components/GlobalHeader.vue";
import '@/assets/login_style.css';

const router = useRouter();
const formData = ref({
  name: '',
  email: '',
  password: '',
  identity: ''
});

const showPassword = ref(false);
const isSubmitting = ref(false);
const apiBase = import.meta.env.VITE_API_BASE;
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const verifyToken = async () => {
  try {
    const response = await axios.post(`${apiBase}/api/users/userinfo`, 
    {}, 
    {
      headers: {
        'Authorization': `Bearer ${Cookies.get('userToken')}`
      }
    });
    
    return response.data.status === 'Success';
  } catch (error) {
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录');
    } else if (error.response?.status === 404) {
      ElMessage.error('用户不存在');
    }
    return false;
  }
};

onMounted(async () => {
  if (Cookies.get('userToken')) {
    const isValid = await verifyToken();
    if (isValid) {
      ElMessage.warning('您已登录，即将跳转至首页');
      router.push('/');
    }
  }
});

const handleSubmit = async () => {
  try {
    // 清除可能的残留token
    Cookies.remove('userToken');
    isSubmitting.value = true;
    
    const response = await axios.post(`${apiBase}/api/users/create`, {
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
      identity: formData.value.identity
    });

    if (response.data.status === 'Success') {
      ElMessage.success('注册成功');
      router.push('/login');
    } else {
      ElMessage.error(response.data.message || '注册失败');
    }
  } catch (error) {
    ElMessage.error('请求异常：' + error.response.data.message);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.password {
  position: relative;
}

.fa-eye {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #999;
}
</style>