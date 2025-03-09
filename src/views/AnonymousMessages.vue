<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import GlobalHeader from '@/components/GlobalHeader.vue';
import Breadcrumb from '@/components/Breadcrumb.vue';
import Cookies from 'js-cookie';
import Footer from "@/components/Footer.vue";

const apiBase = import.meta.env.VITE_API_BASE;
const messages = ref<any[]>([]);
const currentPage = ref(1);
const total = ref(0);
const pageSize = ref(10);
const userRole = ref('');

const fetchMessages = async () => {
  try {
    const response = await axios.get(`${apiBase}/api/anonymous-messages/get`, {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    });

    if (response.data.status === 'Success') {
      messages.value = response.data.data;
      total.value = response.data.pagination.total;
      console.log(messages.value);
    }
  } catch (error) {
    ElMessage.error('获取留言失败');
  }
};

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
    }
  } catch (error) {
    console.error('获取用户信息失败');
  }
};

const handlePageChange = (val: number) => {
  currentPage.value = val;
  fetchMessages();
};

onMounted(() => {
  fetchUserInfo();
  fetchMessages();
});
</script>

<template>
  <div class="hero-container">
    <div class="hero-content">
      <h1 class="hero-title">留言大厅</h1>
    </div>
  </div>
  <Breadcrumb/>

  <div class="container">
    <div class="create-btn">
      <el-button
          type="primary"
          @click="$router.push('/interaction/create')"
      >
        新建留言
      </el-button>
    </div>
    <el-table :data="messages" style="width: 100%" border>
      <el-table-column label="留言内容" >
        <template #default="scope">
          <div v-html="scope.row.content"></div>
        </template>
      </el-table-column>
      <el-table-column prop="timestamp" label="留言时间" width="300"/>
      
      <el-table-column v-if="userRole === 'teacher'" label="操作" width="120">
        <template #default="scope">
          <el-button
            type="primary"
            link
            @click="$router.push(`/interaction/edit/${scope.row.id}`)"
          >
            编辑
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      @current-change="handlePageChange"
    />
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  transition: all 0.3s ease;
}
.create-btn {
  margin-bottom: 20px;
  text-align: right;
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
  background: url('https://imgapi.jinghuashang.cn/random') center/cover;
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
