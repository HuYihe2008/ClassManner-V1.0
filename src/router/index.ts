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
    },
    {
        path: '/activeimages/upload',
        name: 'ActiveImages-upload',
        component: () => import('@/views/ActiveImages-upload.vue'),
    },
    {
        path: '/activeimages',
        name: 'ActiveImages',
        component: () => import('@/views/ActiveImages.vue'),
    },
    {
        path: '/activeimages/:id',
        name: 'ActiveImages-detail',
        component: () => import('@/views/ActiveImages-detail.vue'),
    },
    {
        path: '/activeimages/edit/:id',
        name: 'ActiveImages-edit',
        component: () => import('@/views/ActiveImages-edit.vue'),
    },
    {
        path: '/excellentworks',
        name: 'ExcellentWorks',
        component: () => import('@/views/ExcellentWorks.vue'),
    },
    {
        path: '/excellentworks/:id',
        name: 'ExcellentWorks-detail',
        component: () => import('@/views/ExcellentWorks-detail.vue'),
    },
    {
        path: '/excellentworks/edit/:id',
        name: 'ExcellentWorks-edit',
        component: () => import('@/views/ExcellentWorks-edit.vue'),
    },
    {
        path: '/excellentworks/upload',
        name: 'ExcellentWorks-upload',
        component: () => import('@/views/ExcellentWorks-upload.vue'),
    },
    {
        path: '/interaction',
        name: 'Interaction',
        component: () => import('@/views/AnonymousMessages.vue'),
    },
    {
        path: '/interaction/create',
        name: 'AnonymousMessages-create',
        component: () => import('@/views/AnonymousMessages-create.vue'),
    },
    {
        path: '/interaction/edit/:id',
        name: 'AnonymousMessages-edit',
        component: () => import('@/views/AnonymousMessages-edit.vue'),
    },
    {
        path: '/notice',
        name: 'Notice',
        component: () => import('@/views/Notice.vue'),
    },
    {
        path: '/notice/create',
        name: 'Notice-create',
        component: () => import('@/views/Notice-create.vue'),
    },
    {
        path: '/notice/edit/:id',
        name: 'Notice-edit',
        component: () => import('@/views/Notice-edit.vue'),
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Register.vue'),
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