<template>
  <div class="login-container" :style="bgStyle">
    <div class="login-box">
      <h2>选课推荐系统</h2>
      <el-form :model="form" label-position="left" label-width="60px">
        <el-form-item label="账号">
          <el-input v-model="form.username" placeholder="" @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="" show-password @keyup.enter="handleLogin" />
        </el-form-item>
      </el-form>
      <div class="btn-row">
        <button class="glass-btn glass-btn-primary" :disabled="isLogging" @click="handleLogin">
          <span v-if="isLogging" class="btn-loading"></span>
          {{ isLogging ? '登录中...' : '登录' }}
        </button>
        <button class="glass-btn glass-btn-primary" @click="$router.push('/register')">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../api'
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      isLogging: false
    }
  },
  computed: {
    bgStyle() {
      return {
        backgroundImage: "url('/images/login-bg.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }
    }
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        ElMessage.warning('请输入账号和密码')
        return
      }
      if (this.isLogging) return
      this.isLogging = true
      try {
        const res = await request.post('/login', this.form)
        localStorage.setItem('token', res.access_token)
        localStorage.setItem('role', res.role)
        localStorage.setItem('username', res.username)
        localStorage.setItem('user_id', res.user_id)
        ElMessage.success('登录成功')
        if (res.role === 'superadmin' || res.role === 'admin') {
          this.$router.push('/admin')
        } else {
          this.$router.push('/student')
        }
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '登录失败')
      } finally {
        this.isLogging = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-box {
  width: 480px;
  padding: 50px 45px;
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 24px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 2px rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 2px;
}

:deep(.el-form-item__label) {
  color: #333;
  font-size: 15px;
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(8px);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.06),
    inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 8px;
  padding: 4px 12px;
}

:deep(.el-input__wrapper:hover) {
  box-shadow:
    0 1px 6px rgba(0, 0, 0, 0.08),
    inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow:
    0 0 0 2px rgba(0, 136, 255, 0.3),
    inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
}

.btn-row {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 35px;
}

.glass-btn {
  padding: 12px 50px;
  font-size: 15px;
  cursor: pointer;
  border-radius: 20px;
  border: none;
  color: #fff;
  transition: all 0.25s ease;
  font-weight: 500;
  letter-spacing: 2px;
}

.glass-btn-primary {
  background: rgba(0, 136, 255, 0.8);
  backdrop-filter: blur(16px) saturate(150%);
  box-shadow:
    0 2px 8px rgba(0, 136, 255, 0.2),
    inset 0 1px 2px rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.glass-btn-primary:hover {
  background: rgba(0, 136, 255, 0.95);
  transform: translateY(-1px);
  box-shadow:
    0 4px 16px rgba(0, 136, 255, 0.35),
    inset 0 1px 2px rgba(255, 255, 255, 0.3);
}

.glass-btn-primary:active {
  transform: translateY(0);
}

.glass-btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.btn-loading {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: btn-spin 0.6s linear infinite;
  margin-right: 6px;
  vertical-align: middle;
}

@keyframes btn-spin {
  to { transform: rotate(360deg); }
}

/* 手机端适配 (1080P竖屏) */
@media screen and (max-width: 768px) {
  .login-container {
    padding: 20px;
  }
  
  .login-box {
    width: 100%;
    max-width: 400px;
    padding: 30px 25px;
    border-radius: 20px;
  }
  
  .login-box h2 {
    font-size: 20px;
    margin-bottom: 30px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
    width: 60px !important;
  }
  
  :deep(.el-input__wrapper) {
    height: 40px !important;
  }
  
  :deep(.el-input__inner) {
    font-size: 14px;
  }
  
  .btn-row {
    flex-direction: column;
    gap: 15px;
    margin-top: 25px;
  }
  
  .glass-btn {
    padding: 12px 30px;
    font-size: 14px;
    width: 100%;
    text-align: center;
  }
}
</style>