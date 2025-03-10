<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import GlobalHeader from '@/components/GlobalHeader.vue';
import { useRoute } from 'vue-router';
import Cookies from 'js-cookie';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import Breadcrumb from '@/components/Breadcrumb.vue';

const userRole = ref('');
const apiBase = import.meta.env.VITE_API_BASE;

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
      console.log('完整用户响应:', response.data);
      console.log(userRole.value);
    }
  } catch (error) {
    console.error('获取用户信息失败');
  }
};

onMounted(() => {
  fetchUserInfo();
  fetchData();
});

import { useRouter } from 'vue-router';
import Footer from "@/components/Footer.vue";

const router = useRouter();
const ExcellentWorksList = ref<any[]>([]);

const handleCardClick = (item: any) => {
  router.push({
    name: 'ExcellentWorks-detail',
    params: { id: item.id }
  });
};
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const loading = ref(false);

const fetchData = async () => {
  try {
    loading.value = true;
    const { data } = await axios.get('http://127.0.0.1:8000/api/excellent-works/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    });
    
    if (data.status === 'Success') {
      ExcellentWorksList.value = data.data;
      total.value = data.pagination.total;
    }
  } catch (error) {
    ElMessage.error('数据加载失败');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});

const handleEditClick = async (item: any) => {
  try {
    await router.push({
      name: 'ExcellentWorks-edit',
      params: { 
        id: item.id,
        currentImages: JSON.stringify(item.images) // 新增当前图片数据传递
      }
    });
  } catch (error) {
    ElMessage.error('导航到编辑页失败');
  }
};

const handleAddClick = async (item: any) => {
  try {
    await router.push({
      name: 'ExcellentWorks-upload',
    });
  } catch (error) {
    ElMessage.error('导航到编辑页失败');
  }
};

</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">优秀作业库</h1>
    </div>
  </div>

  <Breadcrumb />

  <div class="container">
    <div class="button-container">
        <el-button 
            type="primary" 
            @click="handleAddClick({})"
            v-if="userRole === 'teacher'"
        >
          <FontAwesomeIcon :icon="['fas', 'plus']" />
          添加优秀作业
        </el-button>
    </div>
    <el-row :gutter="20" class="image-list">
      <el-col 
        v-for="item in ExcellentWorksList"
        :key="item.id" 
        :xs="24" 
        :sm="12" 
        :md="8"
        :lg="6"
      >
        <el-card class="image-card" @click="handleCardClick(item)">
          <template #header>
            <div class="card-header">
              <span>{{ item.title }}</span>
              <el-button 
                v-if="userRole === 'teacher'"
                type="text" 
                class="edit-btn"
                @click.stop="handleEditClick(item)"
              >
                <FontAwesomeIcon :icon="['fas', 'edit']" />
              </el-button>
            </div>
          </template>
          
          <el-image
            v-if="item.images?.length > 0"
            :src="apiBase + '/' + item.images[0]"
            fit="cover"
            class="card-image"
            :lazy="true"
          />
          
          <div class="card-content">
            {{ item.content }}
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-pagination
      background
      layout="prev, pager, next"
      :total="total"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      @current-change="fetchData"
      class="pagination"
    />
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
  max-width: 1200px;
  margin: 0 auto;
}

.image-list {
  margin-bottom: 20px;
}

.image-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.image-card:hover {
  transform: translateY(-5px);
}

.card-image {
  width: 100%;
  height: 200px;
  border-radius: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
  height: 40px;
}

.edit-btn {
  position: relative;
  margin-left: 10px;
  padding: 8px 12px;
  font-size: 18px !important;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 6px;
  color: white;
  transition: all 0.3s;
}

.edit-btn:hover {
  opacity: 0.9;
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.4);
  color: white !important;
}

.card-content {
  padding: 15px 0;
  color: #666;
}

.pagination {
  justify-content: center;
  margin-top: 20px;
}

.breadcrumb-container {
  margin: 40px auto 20px;
  max-width: 1200px;
  padding: 0 20px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.el-button--primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 8px;
  padding: 12px 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}

.el-button--primary .svg-inline--fa {
  margin-right: 8px;
}
</style>