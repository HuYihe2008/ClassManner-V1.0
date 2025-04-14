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

// 评论相关
const comments = ref([]);
const commentForm = ref({
  content: '',
});
const submitting = ref(false);
const currentUser = ref(null);

// 获取评论列表
const fetchComments = async () => {
  try {
    const { data } = await axios.get(
      `${apiBase}/api/comments/list/excellent_work/${route.params.id}`
    );
    if (data.status === 'Success') {
      comments.value = data.data;
    }
  } catch (error) {
    console.error('获取评论失败:', error);
  }
};

// 提交评论
const handleCommentSubmit = async () => {
  if (!commentForm.value.content.trim()) {
    ElMessage.warning('请输入评论内容');
    return;
  }
  
  try {
    submitting.value = true;
    const response = await axios.post(
      `${apiBase}/api/comments/create`,
      {
        content: commentForm.value.content,
        target_id: route.params.id,
        target_type: 'excellent_work',
        user_id: currentUser.value?.id,
        user_name: currentUser.value?.name
      },
      {
        headers: {
          'Authorization': `Bearer ${Cookies.get('userToken')}`
        }
      }
    );
    
    if (response.data.status === 'Success') {
      ElMessage.success('评论发表成功');
      commentForm.value.content = '';
      await fetchComments();
    }
  } catch (error) {
    ElMessage.error('评论发表失败');
  } finally {
    submitting.value = false;
  }
};

// 删除评论
const handleDeleteComment = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    const response = await axios.delete(
      `${apiBase}/api/comments/${commentId}`,
      {
        headers: {
          'Authorization': `Bearer ${Cookies.get('userToken')}`
        }
      }
    );
    
    if (response.data.status === 'Success') {
      ElMessage.success('评论已删除');
      await fetchComments();
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

// 权限检查
const canDeleteComment = (comment) => {
  return userRole.value === 'teacher' || 
         comment.user_email === currentUser.value?.email;
};

// 获取头像URL
const getAvatarUrl = (email) => {
  if (email?.endsWith('@qq.com')) {
    const qq = email.split('@')[0];
    return `https://q1.qlogo.cn/g?b=qq&nk=${qq}&s=100`;
  }
  return 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';
};

// 格式化时间
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

// 获取当前用户信息
const getCurrentUser = async () => {
  if (!Cookies.get('userToken')) return;
  
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
      currentUser.value = response.data.data;
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
};

/**
 * 获取作品详细信息
 * @returns {Promise<void>} 无返回值
 */
const fetchDetail = async () => {
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

onMounted(async () => {
  await fetchUserInfo();
  await getCurrentUser();
  await fetchDetail();  // 修改这里，将 fetchWorkDetail 改为 fetchDetail
  await fetchComments();
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

    <el-card class="comments-section">
      <template #header>
        <div class="comments-header">
          <h3>评论区</h3>
        </div>
      </template>

      <el-form v-if="!!Cookies.get('userToken')" @submit.prevent="handleCommentSubmit">
        <el-input
          v-model="commentForm.content"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
        />
        <el-button 
          type="primary"
          @click="handleCommentSubmit"
          :loading="submitting"
          style="margin-top: 10px"
        >
          发表评论
        </el-button>
      </el-form>
      
      <div v-else class="login-prompt">
        请<router-link to="/login">登录</router-link>后发表评论
      </div>

      <div class="comments-list">
        <template v-if="comments.length > 0">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <el-avatar 
              :size="40" 
              :src="getAvatarUrl(comment.user_email)"
            />
            <div class="comment-content">
              <div class="comment-header">
                <span class="username">{{ comment.user_name }}</span>
                <span class="time">{{ formatTime(comment.created_at) }}</span>
                <el-button
                  v-if="canDeleteComment(comment)"
                  type="danger"
                  link
                  @click="handleDeleteComment(comment.id)"
                >
                  删除
                </el-button>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
            </div>
          </div>
        </template>
        <el-empty v-else description="暂无评论" />
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

.comments-section {
  margin-top: 30px;
}

.comments-header {
  margin-bottom: 20px;
}

.login-prompt {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.login-prompt a {
  color: #409EFF;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #EBEEF5;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.username {
  font-weight: 500;
  margin-right: 12px;
}

.time {
  color: #909399;
  font-size: 12px;
}

.comment-text {
  margin: 0;
  line-height: 1.6;
}
</style>
