<!--
公告创建组件
功能：
- 新建公告表单提交
- 富文本编辑器集成
- 权限验证与状态管理
-->
<script setup lang="ts">
import { reactive, ref, onMounted, shallowRef } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie';
import GlobalHeader from '@/components/GlobalHeader.vue';
import Breadcrumb from '@/components/Breadcrumb.vue';

import Editor from '@tinymce/tinymce-vue';
import 'tinymce/tinymce.min.js';
import 'tinymce/themes/silver/theme';
import 'tinymce/icons/default/icons';
import 'tinymce/skins/ui/oxide/skin.min.css';
import Footer from "@/components/Footer.vue";

const router = useRouter();
const apiBase = import.meta.env.VITE_API_BASE;

// 表单数据
const form = reactive({
  content: ''
});

// 加载状态
const isLoading = ref(false);
const editor = shallowRef()

// 表单验证
const validateForm = () => {
  if (!form.content.trim()) {
    ElMessage.error('通知内容不能为空');
    return false;
  }
  return true;
};

// 提交表单
/**
 * 提交公告内容
 * @returns {Promise<void>} 无返回值
 */
const handleSubmit = async () => {
  if (!validateForm()) return;

  isLoading.value = true;
  try {
    await axios.post(`${apiBase}/api/notice/create`, form, {
      headers: { 'Content-Type': 'application/json' }
    });
    ElMessage.success('通知创建成功');
    router.push('/notice');
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '创建失败，请稍后重试');
  } finally {
    isLoading.value = false;
  }
};
const userRole = ref('');

onMounted(async () => {
  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/users/userinfo',
      {},
      {
        headers: {
          'Authorization': `Bearer ${Cookies.get('userToken')}`
        }
      }
    );

    if (response.data.data.identity === 'student') {
      ElMessage.error('无权限访问');
      router.replace('/');
    } else {
      userRole.value = response.data.data.identity;
    }
  } catch (error) {
    console.error('权限验证失败');
    router.replace('/');
  }
});
</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">通知大厅</h1>
      <h2 class="hero-subtitle">新建通知</h2>
    </div>
  </div>
  <Breadcrumb/>
  <div class="container">
    <el-form label-width="80px" class="create-form">
      <el-form-item label="内容">
        <Editor
            v-model="form.content"
            :init="{
              height: 500,
              width: '100%',
              menubar: true,
              base_url: '/tinymce',
    suffix: '.min',
              language: 'zh_CN',
              plugins: 'advlist autolink lists link charmap code help',
              toolbar: 'undo redo | bold italic | alignleft aligncenter alignright | bullist numlist | code help',
              skin_url: '/tinymce/skins/ui/oxide',
              language_url: '/tinymce/langs/zh_CN.js',
              content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
          }"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          @click="handleSubmit"
          :loading="isLoading"
          :disabled="isLoading"
          class="submit-btn"
        >
          提交通知
        </el-button>
        <el-button @click="router.go(-1)" :disabled="isLoading" class="cancel-btn">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 120px);
  flex: 1;
}

.el-form-item__content {
  flex: 1;
  min-width: 0;
  display: flex;
  width: 100%;
}
:deep(.ql-editor) {
  min-height: 250px;
  flex: 1;
}

.create-form {
  margin-top: 20px;
}

.submit-btn {
  background-color: #409eff;
  border-color: #409eff;
  transition: all 0.3s;
}
.submit-btn:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.cancel-btn {
  background-color: #f5f7fa;
  color: #606266;
  border-color: #dcdfe6;
  transition: all 0.3s;
}
.cancel-btn:hover {
  background-color: #ebedf0;
  border-color: #c0c4cc;
}
.hero-container {
  height: 300px;
  position: relative;
  overflow: hidden;
  padding-top: 60px
}

.hero-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('https://www.loliapi.com/acg/') center/cover;
  filter: blur(5px);
  z-index: 1;
}
.hero-content {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  z-index: 2;
}
.hero-title {
  color: white;
  font-size: 3.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
}
.hero-subtitle {
  color: white;
  font-size: 1.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  position: relative;
}

.hero-content::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: -1;
}
</style>
