<!--
活动图片详情组件
功能：
- 展示单张活动图片详细信息
- 支持用户权限验证
- 提供删除/编辑操作入口
-->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { ElMessage, ElMessageBox } from 'element-plus';
import GlobalHeader from '@/components/GlobalHeader.vue';
import { useRoute, useRouter } from 'vue-router';
import Breadcrumb from '@/components/Breadcrumb.vue';

const userRole = ref('');

const apiBase = import.meta.env.VITE_API_BASE

/**
 * 获取用户身份信息
 * @returns {Promise<void>} 无返回值
 */
const fetchUserInfo = async () => {
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

    if (response.data.status === 'Success') {
      userRole.value = response.data.data.identity || 'student';
      console.log('用户信息响应:', response.data);
      console.log(userRole.value);
    }
  } catch (error) {
    console.error('获取用户信息失败');
  }
};

onMounted(() => {
  fetchUserInfo();
});

const route = useRoute();
const router = useRouter();
const activeDetail = ref<any>({});
const loading = ref(true);

/**
 * 组件挂载时加载数据
 * @returns {Promise<void>} 无返回值
 */
onMounted(async () => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:8000/api/active-images/${route.params.id}`);
    
    if (data.status === 'Success') {
      activeDetail.value = data.data;
    }
  } catch (error) {
    ElMessage.error('数据加载失败');
  } finally {
    loading.value = false;
  }
});

const handleEdit = () => {
  router.push(`/activeimages/edit/${route.params.id}`);
};

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该活动吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await axios.delete(`http://127.0.0.1:8000/api/active-images/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer ${Cookies.get('userToken')}`
      }
    });
    ElMessage.success('删除成功');
    router.push('/activeimages');
  } catch (error) {
    ElMessage.error('删除失败');
  }
};
</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">活动影像库</h1>
      <h2 class="hero-subtitle">活动详情</h2>
    </div>
  </div>
  <Breadcrumb />
  <div class="container">
    <el-button @click="router.go(-1)" class="back-btn">返回列表</el-button>
    
    <el-card v-loading="loading" class="detail-card">
      <template #header>
        <div class="card-header">
          <h2>{{ activeDetail.title }}</h2>
          <div class="button-group">
          <el-button 
            v-if="userRole === 'teacher'"
            type="primary"
            @click.stop="handleEdit"
          >
            编辑活动
          </el-button>
          <el-button 
            v-if="userRole === 'teacher'"
            type="danger" 
            @click.stop="handleDelete"
          >
            删除活动
          </el-button>
        </div>
        </div>
      </template>

      <el-carousel v-if="activeDetail.images?.length > 0" indicator-position="outside">
        <el-carousel-item v-for="(img, index) in activeDetail.images" :key="index">
          <el-image 
  :src="`${apiBase}/${img}`" 
  fit="contain" 
  class="carousel-image"
  :preview-src-list="activeDetail.images.map(img => `${apiBase}/${img}`)"
  :preview-teleported="true"
/>
        </el-carousel-item>
      </el-carousel>

      <div class="content-section">
        <p>{{ activeDetail.content }}</p>
      </div>
    </el-card>
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
  padding: 0px 20px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.back-btn {
  margin-bottom: 20px;
}

.detail-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button-group {
  display: flex;
  gap: 12px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.el-carousel-item {
  height: 600px;
}

.content-section {
  margin-top: 30px;
  font-size: 16px;
  line-height: 1.8;
}

</style>
