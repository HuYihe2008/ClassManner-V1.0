<template>
  <footer class="footer">
    <!-- 左侧内容 -->
    <div class="footer-left">
      <div class="bilibili-links">
        <span>JamYido</span>
        <a href="#">关于我们</a>
        <a href="#">联系我们</a>
        <a href="#">用户协议</a>
        <a href="#">加入我们</a>
        <a href="#">友情链接</a>
        <a href="#">隐私协议</a>
      </div>
      <div class="transmission-door">
        <span>传送门</span>
        <a href="/">首页</a>
        <a href="/activeimages/upload">活动上传</a>
        <a href="/activeimages">活动影像库</a>
        <a href="/excellentworks">优秀作业库</a>
        <a href="/notice">通知大厅</a>
        <a href="/login">登录与用户中心</a>
        <a href="/register">注册</a>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="footer-right">
      <el-button type="primary">
        <el-icon><Download /></el-icon>下载APP
      </el-button>
      <el-button type="info">
        <el-icon><Sunny /></el-icon>公益
      </el-button>
      <el-button type="danger">
        <el-icon><ChatDotRound /></el-icon>官方微博
      </el-button>
      <el-button type="success">
        <el-icon><ChatLineRound /></el-icon>官方微信
      </el-button>
    </div>

    <!-- 底部信息 -->
    <div class="footer-bottom">
      <div class="team-info">
        <el-icon><ChatLineRound /></el-icon>
        <span>由 JamYido 个人倾情打造</span>
      </div>
    <!-- 社交链接 -->  
      <!--<div class="social-links">
        <a href="https://weibo.com" target="_blank" class="weibo">
          <el-icon><ChatDotRound /></el-icon>
          关注微博
        </a>
        <a href="https://weixin.qq.com" target="_blank" class="wechat">
          <el-icon><ChatLineRound /></el-icon>
          添加微信
        </a>
      </div>-->

      <p class="blessing">
        <el-icon><Sunny /></el-icon>
        愿每个校园记忆都温暖如初
      </p>

      <p class="copyright">
        ©2024 ClassManer 让校园生活更美好
      </p>
    </div>
  </footer>
</template>

<script>
import { ElIcon } from 'element-plus';
import { Download, Sunny, ChatDotRound, ChatLineRound } from '@element-plus/icons';

export default {
  name: 'Footer',
  components: {
    ElIcon,
    Download,
    Sunny,
    ChatDotRound,
    ChatLineRound,
  }
}
</script>

<style scoped>
.footer {
  background: linear-gradient(150deg, var(--el-color-primary-light-9) 0%, var(--el-bg-color) 100%);
  display: grid;
  grid-template-columns: 3fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
  padding: 30px 5%;
  background-color: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-light);
}

.footer-left {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
}

.bilibili-links,
.transmission-door {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-left span {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.footer-left a {
  position: relative;
  color: var(--el-text-color-regular);
  transition: all 0.3s var(--el-transition-function-ease-in-out-bezier);
  text-decoration: none;
  background: var(--el-color-primary-light-9);
  border: 1px solid var(--el-color-primary-light-7);
  border-radius: 6px;
  padding: 8px 12px !important;
}

.footer-left a:hover {
  color: var(--el-color-primary);
  transform: translateX(4px);
}

.footer-left a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0%;
  height: 1px;
  background: linear-gradient(90deg, var(--el-color-primary), transparent);
  transition: width 0.3s var(--el-transition-function-ease-in-out-bezier);
}

.footer-left a:hover::after {
  width: 100%;
}

.footer-right {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: flex-start;
  margin-left: 0;
}

.footer-right .el-button {
  width: 100%;
  justify-content: flex-start;
  padding: 14px 20px;
  margin-left: 0;
}

.footer-right .el-button {
  flex: 0 0 18%;
  padding: 12px;
  border-radius: 8px;
  margin-left: 0;
}

.footer-right .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.footer-bottom {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 15px 0;
  margin-top: 20px;
  border-top: 1px solid var(--el-border-color-light);
}

.team-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.blessing {
  display: flex;
  align-items: center;
  gap: 6px;
}

@media (max-width: 768px) {
  .footer-bottom {
    padding: 20px 15px;
    gap: 12px;
  }
}

.footer-bottom p {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.social-links {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  justify-content: center;
}

.social-links a {
  padding: 8px 20px;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--el-color-primary-light-9);
  box-shadow: 0 3px 8px var(--el-color-primary-light-7);
  transition: all 0.2s ease-in-out;
}

.social-links a:hover {
  box-shadow: 0 5px 15px var(--el-color-primary-light-5);
  transform: translateY(-2px);
}

.social-links a:active {
  transform: scale(0.98);
}

.social-links .el-icon {
  margin-right: 6px;
  font-size: 18px;
}


@media (max-width: 768px) {
  .social-links a {
    padding: 6px 10px;
  }
  .social-links .el-icon {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .footer {
    grid-template-columns: 1fr;
    padding: 20px 5%;
    grid-template-rows: auto auto;
    gap: 15px;
  }
  
  .footer-right .el-button {
    flex: 0 0 100%;
    padding: 10px;
  }

  .transmission-door {
    display: none;
  }
}
</style>
