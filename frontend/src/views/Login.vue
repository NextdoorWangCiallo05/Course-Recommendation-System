<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="/images/logo.png" class="login-logo" alt="logo">
        <h2>选课推荐系统</h2>
        <p class="login-subtitle">课程智能推荐与模拟选课平台</p>
      </div>
      <n-form :model="form" label-placement="top" :show-label="false">
        <n-form-item>
          <n-input v-model:value="form.username" placeholder="请输入账号" size="large" @keyup.enter="handleLogin">
            <template #prefix>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </template>
          </n-input>
        </n-form-item>
        <n-form-item>
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" size="large" show-password-on="click" @keyup.enter="handleLogin">
            <template #prefix>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </template>
          </n-input>
        </n-form-item>
      </n-form>
      <div class="login-actions">
        <n-button type="primary" size="large" block :loading="isLogging" :disabled="isLogging" @click="handleLogin">
          {{ isLogging ? '登录中...' : '登录' }}
        </n-button>
        <n-button size="large" block class="register-btn" @click="$router.push('/register')">
          注册
        </n-button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useMessage } from 'naive-ui'
import request from '../api'

export default defineComponent({
  setup() {
    const message = useMessage()
    return { message }
  },
  data() {
    return {
      form: { username: '', password: '' },
      isLogging: false
    }
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        this.message.warning('请输入账号和密码')
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
        this.message.success('登录成功')
        if (res.role === 'superadmin' || res.role === 'admin') {
          this.$router.push('/admin')
        } else {
          this.$router.push('/student')
        }
      } catch (e) {
        this.message.error(e.response?.data?.msg || '登录失败')
      } finally {
        this.isLogging = false
      }
    }
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-card {
  width: 420px;
  padding: 48px 40px 40px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.login-logo {
  width: 72px;
  height: 72px;
  object-fit: contain;
  margin-bottom: 12px;
}

.login-header h2 {
  color: #1a1a2e;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
}

.login-subtitle {
  color: #999;
  font-size: 13px;
  margin-top: 6px;
}

.login-actions {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.register-btn {
  --n-color: transparent !important;
  --n-border-color: #d9d9d9 !important;
  --n-color-hover: rgba(0, 0, 0, 0.02) !important;
  --n-border-color-hover: #2080F0 !important;
  --n-text-color-hover: #2080F0 !important;
}

html.dark-mode .login-card {
  background: rgba(30, 30, 50, 0.85);
  border-color: rgba(255, 255, 255, 0.08);
}

html.dark-mode .login-header h2 {
  color: #e8e8e8;
}

html.dark-mode .login-subtitle {
  color: #888;
}

@media screen and (max-width: 768px) {
  .login-card {
    width: 100%;
    max-width: 400px;
    padding: 32px 24px;
  }
  .login-header h2 {
    font-size: 20px;
  }
}
</style>
