<script setup lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, watch } from 'vue';
import GlobalHeader from "@/components/GlobalHeader.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";
import { useDark } from '@vueuse/core';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Cookies from 'js-cookie';

/**
 * 用户权限验证
 * @function 验证教师身份权限
 * @throws {Error} 无权限访问时跳转首页
 */
const isDark = useDark();
const form = ref({
  title: '',
  content: '',
  images: [] as string[]
});
const fileList = ref<File[]>([]);
const isLoading = ref(false);
const uploadRef = ref();
const router = useRouter();

const beforeUpload = (file: File) => {
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件');
    return false;
  }
  return true;
};

const handleSuccess = (response: any, uploadFile: UploadFile) => {
  if (response.status === 'Success') {
    form.value.images.push(response.data);
  }
};

const submitForm = async () => {
  try {
    isLoading.value = true;
    // 检查是否存在未上传完成的文件
    if (fileList.value.some(file => file.status !== 'success')) {
      ElMessage.warning('请等待所有图片上传完成');
      return;
    }
    // 确保至少上传一张图片
    if (form.value.images.length === 0) {
      ElMessage.warning('请至少上传一张活动照片');
      return;
    }
    const { data } = await axios.post('http://127.0.0.1:8000/api/active-images/create', {
      title: form.value.title,
      content: form.value.content,
      images: form.value.images
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    ElMessage.success('提交成功');
    form.value = { title: '', content: '', images: [] };
    fileList.value = [];
    uploadRef.value.clearFiles();
    router.push('/activeimages/');
    
  } catch (error) {
    ElMessage.error('提交失败');
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
<div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">活动影像库</h1>
      <h2 class="hero-subtitle">上传活动</h2>
    </div>
  </div>
<Breadcrumb />
  <div class="container">
    <div class="content">
      <el-form label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        
        <el-form-item label="内容">
          <el-input 
            v-model="form.content"
            type="textarea"
            :rows="4"
            placeholder="请输入活动描述"
          />
        </el-form-item>

        <el-form-item label="图片">
          <el-upload
            ref="uploadRef"
            v-model:file-list="fileList"
            multiple
            list-type="picture-card"
            action="http://127.0.0.1:8000/api/active-images/upload"
            :before-upload="beforeUpload"
            :on-success="handleSuccess"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitForm"
            :loading="isLoading"
          >
            提交
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
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
.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.el-form-item {
  margin-bottom: 22px;
}

:deep(.el-upload-list__item) {
  transition: all 0.3s ease;
}
</style>