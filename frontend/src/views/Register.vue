<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>注册账号</h2>
        <p class="register-subtitle">填写信息注册后等待管理员审核</p>
      </div>
      <n-form :model="form" label-placement="top" label-width="80px">
        <n-form-item label="用户名">
          <n-input v-model:value="form.username" placeholder="3-20位字母/数字/下划线" />
        </n-form-item>
        <n-form-item label="密码">
          <n-input v-model:value="form.password" type="password" placeholder="至少8位，包含字母和数字" show-password-on="click" />
        </n-form-item>
        <n-form-item label="确认密码">
          <n-input v-model:value="form.confirmPassword" type="password" placeholder="再次输入密码" show-password-on="click" @keyup.enter="handleRegister" />
        </n-form-item>
        <n-form-item label="真实姓名">
          <n-input v-model:value="form.real_name" placeholder="请输入真实姓名" />
        </n-form-item>
        <n-form-item label="学号">
          <n-input v-model:value="form.student_id" placeholder="请输入学号" />
        </n-form-item>
        <n-form-item label="申请角色">
          <n-select v-model:value="form.role" :options="roleOptions" />
        </n-form-item>
      </n-form>
      <n-button type="primary" size="large" block :loading="isRegistering" :disabled="isRegistering" @click="handleRegister">
        {{ isRegistering ? '注册中...' : '提交注册' }}
      </n-button>
      <div class="tips">
        <p>注册后需要等待超级管理员审核</p>
        <p class="tip-rule">密码：至少8位，包含字母和数字</p>
        <p class="back-link" @click="$router.push('/login')">已有账号？返回登录</p>
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
      form: {
        username: '',
        password: '',
        confirmPassword: '',
        real_name: '',
        student_id: '',
        role: 'student'
      },
      isRegistering: false,
      roleOptions: [
        { label: '学生', value: 'student' },
        { label: '管理员', value: 'admin' }
      ]
    }
  },
  methods: {
    async handleRegister() {
      const f = this.form
      if (!f.username || !f.password || !f.confirmPassword || !f.real_name || !f.student_id) {
        this.message.warning('请填写完整信息')
        return
      }
      if (f.password !== f.confirmPassword) {
        this.message.warning('两次密码输入不一致')
        return
      }
      if (f.password.length < 8) {
        this.message.warning('密码长度至少8位')
        return
      }
      if (!/[a-zA-Z]/.test(f.password) || !/[0-9]/.test(f.password)) {
        this.message.warning('密码必须包含字母和数字')
        return
      }
      if (!/^[a-zA-Z0-9_]+$/.test(f.username)) {
        this.message.warning('用户名只能包含字母、数字和下划线')
        return
      }
      if (f.username.length < 3 || f.username.length > 20) {
        this.message.warning('用户名长度需在3-20位之间')
        return
      }
      if (this.isRegistering) return
      this.isRegistering = true
      try {
        await request.post('/register', {
          username: f.username,
          password: f.password,
          real_name: f.real_name,
          student_id: f.student_id,
          role: f.role
        })
        this.message.success('注册成功，等待超级管理员审核')
        this.$router.push('/login')
      } catch (e) {
        this.message.error(e.response?.data?.msg || '注册失败')
      } finally {
        this.isRegistering = false
      }
    }
  }
})
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.register-card {
  width: 480px;
  padding: 40px 40px 36px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
}

.register-header {
  text-align: center;
  margin-bottom: 28px;
}

.register-header h2 {
  color: #1a1a2e;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
}

.register-subtitle {
  color: #999;
  font-size: 13px;
  margin-top: 6px;
}

.tips {
  margin-top: 20px;
  font-size: 13px;
  color: #888;
  text-align: center;
  line-height: 1.8;
}

.tip-rule {
  color: #aaa;
  font-size: 12px;
}

.back-link {
  color: #2080F0;
  cursor: pointer;
  font-size: 13px;
  margin-top: 8px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #4098FC;
}

html.dark-mode .register-card {
  background: rgba(30, 30, 50, 0.85);
  border-color: rgba(255, 255, 255, 0.08);
}

html.dark-mode .register-header h2 {
  color: #e8e8e8;
}

@media screen and (max-width: 768px) {
  .register-card {
    width: 100%;
    max-width: 400px;
    padding: 28px 20px;
  }
}
</style>
