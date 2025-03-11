<!--
优秀作品详情组件
功能：
- 展示单件作品详细信息
- 支持多图轮播展示
- 提供作品元数据查看

Excellent Work Detail Component
Features:
- Display single work details
- Support multi-image carousel
- Show work metadata
-->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { ElMessage, ElMessageBox } from 'element-plus';
import GlobalHeader from '@/components/GlobalHeader.vue';
import { useRoute, useRouter } from 'vue-router';
import Breadcrumb from '@/components/Breadcrumb.vue';
import Footer from "@/components/Footer.vue";

const userRole = ref('');

const apiBase = import.meta.env.VITE_API_BASE

const fetchUserInfo = async () => {
  try {
    const response = await axios.post(
      `${apiBase}/api/users/userinfo`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${Cookies.get('userToken')}`
        }
      }
    );

    if (response.data.status === 'Success') {
      userRole.value = response.data.data.identity || 'student';
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
const ExcellentWorksDetail = ref<any>({});
const loading = ref(true);

/**
 * 获取作品详细信息
 * @param {string} workId - 作品ID
 * @returns {Promise<void>} 无返回值
 */
const fetchWorkDetail = async () => {
  try {
    const { data } = await axios.get(`${apiBase}/api/excellent-works/${route.params.id}`);
    
    if (data.status === 'Success') {
      ExcellentWorksDetail.value = data.data;
    }
  } catch (error) {
    ElMessage.error('数据加载失败');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchWorkDetail();
});

const handleEdit = () => {
  router.push(`/excellentworks/edit/${route.params.id}`);
};

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该作业吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await axios.delete(`${apiBase}/api/excellent-works/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer ${Cookies.get('userToken')}`
      }
    });
    ElMessage.success('删除成功');
    router.push('/excellentworks');
  } catch (error) {
    ElMessage.error('删除失败');
  }
};
</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">优秀作业库</h1>
      <h2 class="hero-subtitle">作业详情</h2>
    </div>
  </div>
  <Breadcrumb />
  <div class="container">
    <el-button @click="router.go(-1)" class="back-btn">返回列表</el-button>
    
    <el-card v-loading="loading" class="detail-card">
      <template #header>
        <div class="card-header">
          <h2>{{ ExcellentWorksDetail.title }}</h2>
          <div class="button-group">
          <el-button 
            v-if="userRole === 'teacher'"
            type="primary"
            @click.stop="handleEdit"
          >
            编辑作业
          </el-button>
          <el-button 
            v-if="userRole === 'teacher'"
            type="danger" 
            @click.stop="handleDelete"
          >
            删除左右
          </el-button>
        </div>
        </div>
      </template>

      <el-carousel v-if="ExcellentWorksDetail.images?.length > 0" indicator-position="outside">
        <el-carousel-item v-for="(img, index) in ExcellentWorksDetail.images" :key="index">
          <el-image 
  :src="`${apiBase}/${img}`" 
  fit="contain" 
  class="carousel-image"
  :preview-src-list="ExcellentWorksDetail.images.map(img => `${apiBase}/${img}`)"
  :preview-teleported="true"
/>
        </el-carousel-item>
      </el-carousel>

      <div class="content-section">
        <p>{{ ExcellentWorksDetail.content }}</p>
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
