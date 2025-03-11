<!--
活动图片编辑组件
Features:
- 图片信息编辑与更新
- 图片预览与删除操作
- 权限验证与状态管理
-->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import GlobalHeader from '@/components/GlobalHeader.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import Cookies from 'js-cookie';
import Footer from "@/components/Footer.vue";

const route = useRoute()
const router = useRouter()
const apiBase = import.meta.env.VITE_API_BASE
const form = ref({
  title: '',
  content: '',
  images: [] as string[]
})
const fileList = ref<any[]>([])
const isLoading = ref(false)
const previewVisible = ref(false)
const previewImageUrl = ref('')
const originalImages = ref<string[]>([])

// 加载现有数据
onMounted(async () => {
  try {
    /**
 * 用户权限验证
 * @function 验证教师身份权限
 * @throws {Error} 无权限访问时跳转首页
 */
const userRes = await axios.post(`${apiBase}/api/users/userinfo`, {}, {
      headers: { 'Authorization': `Bearer ${Cookies.get('userToken')}` }
    });
    
    if (userRes.data.data.identity !== 'teacher') {
      ElMessage.error('无权限访问');
      router.push('/');
      return;
    }

const { data } = await axios.get(`${apiBase}/api/active-images/${route.params.id}`)
    originalImages.value = data.data.images // 保存原始图片路径
    if (data.status === 'Success') {
      form.value = {
        title: data.data.title,
        content: data.data.content,
        images: data.data.images.map((item: any) => {
          const urlArray = Array.isArray(item) ? item : [item];
          return urlArray[0]?.startsWith('http') ? urlArray[0] : `${apiBase}/${urlArray[0]}`;
        })
      }
      
      // 将现有图片转换为 fileList 格式
      fileList.value = form.value.images.map((url: string, index: number) => ({
        name: `image-${index}`,
        url: url,
        status: 'success'
      }))
    }
  } catch (error) {
    console.error('数据加载失败');
    ElMessage.error('获取数据失败');
    router.push('/activeimages');
  }
});

const handleSubmit = async () => {
  try {
    isLoading.value = true
    const payload = {
      title: form.value.title,
      content: form.value.content,
      images: form.value.images.length > 0 
        ? form.value.images.map(url => url.replace(apiBase, '').replace(/^\/+/, '')) 
        : originalImages.value // 保留原始图片当未上传新内容时
    }
    await axios.put(`${apiBase}/api/active-images/${route.params.id}`, payload)
    ElMessage.success('更新成功')
    router.push('/activeimages/')
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    isLoading.value = false
  }
}

const handleRemove = async (file: any) => {
  try {
    const imagePath = encodeURIComponent(new URL(file.url).pathname.split('/').pop() || '');
    await axios.delete(`${apiBase}/api/active-images/image/${encodeURIComponent(imagePath)}`)
    form.value.images = form.value.images.filter(url => {
  const relativeUrl = url.replace(apiBase, '').replace(/^\/+/, '');
  // 精确匹配图片文件名
  return !relativeUrl.includes(imagePath);
})
    ElMessage.success('图片删除成功')
  } catch (error) {
    ElMessage.error('图片删除失败')
  }
};

const handleDelete = () => {
  ElMessageBox.confirm('确定删除该活动？此操作不可恢复！', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await axios.delete(`${apiBase}/api/active-images/${route.params.id}`)
    ElMessage.success('删除成功')
    router.push('/activeimages')
  }).catch(() => {})
}

// 添加预览相关的函数
const handlePreview = (file: any) => {
  previewImageUrl.value = file.url
  previewVisible.value = true
}
</script>

<template>
<div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">活动影像库</h1>
      <h2 class="hero-subtitle">编辑活动</h2>
    </div>
  </div>
<Breadcrumb />
<div class="container">
  <el-button @click="router.go(-1)">返回</el-button>
  <el-form label-width="80px" class="edit-form">
    <!-- 复用上传组件 -->
    <el-form-item label="标题">
      <el-input v-model="form.title" />
    </el-form-item>
    <el-form-item label="内容">
      <el-input v-model="form.content" type="textarea" :rows="4" />
    </el-form-item>
    <el-form-item label="图片">
      <el-upload
        v-model:file-list="fileList"
        multiple
        list-type="picture-card"
        :action="apiBase + '/api/active-images/upload'"
        :on-success="(res: any) => { console.log('上传响应数据:', res); form.images.push(res.data[0]); }"
        :on-remove="handleRemove"
        :on-preview="handlePreview"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
    </el-form-item>
    
    <el-form-item>
      <el-button type="primary" @click="handleSubmit" :loading="isLoading">提交修改</el-button>
      <el-button type="danger" @click="handleDelete">删除活动</el-button>
    </el-form-item>
  </el-form>
</div>

<!-- 添加预览对话框 -->
<el-dialog v-model="previewVisible" title="图片预览">
  <img :src="previewImageUrl" alt="Preview" style="width: 100%">
</el-dialog>

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
  padding: 0px 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.edit-form {
  margin-top: 20px;
}
</style>
