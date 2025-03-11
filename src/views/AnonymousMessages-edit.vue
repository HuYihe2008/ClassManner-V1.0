<script setup lang="ts">
import { ref, onMounted, shallowRef } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import GlobalHeader from '@/components/GlobalHeader.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import Editor from '@tinymce/tinymce-vue'
import Cookies from 'js-cookie'  // 添加这行导入
import 'tinymce/tinymce.min.js'
import 'tinymce/themes/silver/theme'
import 'tinymce/icons/default/icons'
import 'tinymce/skins/ui/oxide/skin.min.css'
import Footer from "@/components/Footer.vue";

const route = useRoute()
const router = useRouter()
const apiBase = import.meta.env.VITE_API_BASE
const form = ref({
  content: '',
  timestamp: ''
})
const isLoading = ref(false)
const editor = shallowRef()

/**
 * 用户权限验证及数据加载
 * @function 验证访问权限并加载留言数据
 * @throws {Error} 无权限访问时跳转首页
 */
onMounted(async () => {
  try {
    // 权限验证
    const { data } = await axios.post(
      `${apiBase}/api/users/userinfo`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${Cookies.get('userToken')}`
        }
      }
    );
    
    // 修改判断逻辑，与路由守卫保持一致
    if (data.status !== 'Success' || data.data.identity !== 'teacher') {
      router.push('/');
      return;
    }

    // 加载留言数据
    const response = await axios.get(`${apiBase}/api/anonymous-messages/get/${route.params.id}`);
    if (response.data.status === 'Success' && response.data.data) {
      form.value = {
        content: response.data.data.content,
        timestamp: response.data.data.timestamp
      }
      editor.value = Editor;
    } else {
      ElMessage.error(response.data.message || '获取留言数据格式错误');
    }
  } catch (error: any) {
    console.error('获取留言错误:', error);
    ElMessage.error(error.response?.data?.message || '获取留言失败，请检查网络连接');
  }
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    await axios.put(
      `${apiBase}/api/anonymous-messages/update/${route.params.id}`,
      { content: form.value.content },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    ElMessage.success('更新成功')
    router.push('/interaction')
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    isLoading.value = false
  }
}

</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">留言大厅</h1>
      <h2 class="hero-subtitle">编辑留言</h2>
    </div>
  </div>
  <Breadcrumb/>
  <div class="container">
    <el-form label-width="80px" class="edit-form">
      <el-form-item label="内容">
        <Editor
          v-model="form.content"
          :init="{
              height: 500,
              width: '100%',
              menubar: true,
              base_url: '/node_modules/tinymce',
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
        <el-button type="primary" @click="handleSubmit" :loading="isLoading">提交修改</el-button>
        <el-button @click="router.go(-1)">取消</el-button>
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
}
:deep(.ql-editor) {
  min-height: 250px;
  flex: 1;
}

.el-form-item__content {
  flex: 1;
  min-width: 0;
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
