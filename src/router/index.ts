import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Cookies from 'js-cookie';
import axios from 'axios';

// 检查路径是否正确，确保 Home.vue 文件存在于 @/views 目录下
import Home from '@/views/Home.vue';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: { title: '首页' }
    },
    {
        path: '/activeimages/upload',
        name: 'ActiveImages-upload',
        component: () => import('@/views/ActiveImages-upload.vue'),
    meta: { title: '上传活动' },
    },
    {
        path: '/activeimages',
        name: 'ActiveImages',
        component: () => import('@/views/ActiveImages.vue'),
    meta: { title: '活动影像库' },
    },
    {
        path: '/activeimages/:id',
        name: 'ActiveImages-detail',
        component: () => import('@/views/ActiveImages-detail.vue'),
    meta: { title: '活动详情' },
    },
    {
        path: '/activeimages/edit/:id',
        name: 'ActiveImages-edit',
        component: () => import('@/views/ActiveImages-edit.vue'),
    meta: { title: '编辑活动' },
    },
    {
        path: '/excellentworks',
        name: 'ExcellentWorks',
        component: () => import('@/views/ExcellentWorks.vue'),
    meta: { title: '优秀作业库' },
    },
    {
        path: '/excellentworks/:id',
        name: 'ExcellentWorks-detail',
        component: () => import('@/views/ExcellentWorks-detail.vue'),
    meta: { title: '优秀作业详情' },
    },
    {
        path: '/excellentworks/edit/:id',
        name: 'ExcellentWorks-edit',
        component: () => import('@/views/ExcellentWorks-edit.vue'),
    meta: { title: '编辑作业' },
    },
    {
        path: '/excellentworks/upload',
        name: 'ExcellentWorks-upload',
        component: () => import('@/views/ExcellentWorks-upload.vue'),
    meta: { title: '上传作业' },
    },
    {
        path: '/interaction',
        name: 'Interaction',
        component: () => import('@/views/AnonymousMessages.vue'),
    meta: { title: '留言大厅' },
    },
    {
        path: '/interaction/create',
        name: 'AnonymousMessages-create',
        component: () => import('@/views/AnonymousMessages-create.vue'),
    meta: { title: '上传留言' },
    },
    {
        path: '/interaction/edit/:id',
        name: 'AnonymousMessages-edit',
        component: () => import('@/views/AnonymousMessages-edit.vue'),
    meta: { title: '编辑留言' },
    },
    {
        path: '/notice',
        name: 'Notice',
        component: () => import('@/views/Notice.vue'),
    meta: { title: '通知大厅' },
    },
    {
        path: '/notice/create',
        name: 'Notice-create',
        component: () => import('@/views/Notice-create.vue'),
    meta: { title: '上传通知' },
    },
    {
        path: '/notice/edit/:id',
        name: 'Notice-edit',
        component: () => import('@/views/Notice-edit.vue'),
    meta: { title: '编辑通知' },
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
    meta: { title: '用户登录' },
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Register.vue'),
    meta: { title: '用户注册' },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 需要权限验证的路由路径
const protectedPaths = [
  /^\/activeimages\/edit\/\d+$/,
  /^\/excellentworks\/edit\/\d+$/,
  /^\/excellentworks\/upload$/,
  /^\/notice\/create$/,
  /^\/notice\/edit\/\d+$/,
  /^\/interaction\/edit\/\d+$/
];

router.beforeEach(async (to, from, next) => {
    document.title = to.meta?.title ? `${to.meta.title}  |  班级文化服务栈` : '班级文化服务栈';

  // 公开路径直接放行
  if (!protectedPaths.some(regex => regex.test(to.path))) {
    next();
    return;
  }

  const token = Cookies.get('userToken');
  if (!token) {
    next('/');
    return;
  }

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/users/userinfo',
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (response.data.data.identity !== 'teacher') {
      next('/');
    } else {
      next();
    }
  } catch (error) {
    console.error('权限验证失败');
    next('/');
  }
});

export default router;