<template>
  <div class="register-container" :style="bgStyle">
    <div class="register-box">
      <h2>注册账号</h2>
      <el-form :model="form" label-position="left" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirmPassword" type="password" placeholder="" show-password @keyup.enter="handleRegister" />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="form.real_name" placeholder="" />
        </el-form-item>
        <el-form-item label="学号">
          <el-input v-model="form.student_id" placeholder="" />
        </el-form-item>
        <el-form-item label="申请角色">
          <el-select v-model="form.role" placeholder="" style="width: 100%;">
            <el-option label="学生" value="student" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="btn-row">
        <button class="glass-btn glass-btn-primary" :disabled="isRegistering" @click="handleRegister">
          <span v-if="isRegistering" class="btn-loading"></span>
          {{ isRegistering ? '注册中...' : '提交注册' }}
        </button>
      </div>
      <div class="tips">
        <p>注册后需要等待超级管理员审核</p>
        <p style="margin-top: 10px;">
          <span class="back-link" @click="$router.push('/login')">已有账号？返回登录</span>
        </p>
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
        password: '',
        confirmPassword: '',
        real_name: '',
        student_id: '',
        role: 'student'
      },
      isRegistering: false
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
    async handleRegister() {
      if (!this.form.username || !this.form.password || !this.form.confirmPassword || !this.form.real_name || !this.form.student_id) {
        ElMessage.warning('请填写完整信息')
        return
      }
      if (this.form.password !== this.form.confirmPassword) {
        ElMessage.warning('两次密码输入不一致')
        return
      }
      if (this.form.password.length < 6) {
        ElMessage.warning('密码长度不能少于6位')
        return
      }
      if (this.isRegistering) return
      this.isRegistering = true
      try {
        await request.post('/register', {
          username: this.form.username,
          password: this.form.password,
          real_name: this.form.real_name,
          student_id: this.form.student_id,
          role: this.form.role
        })
        ElMessage.success('注册成功，等待超级管理员审核')
        this.$router.push('/login')
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '注册失败')
      } finally {
        this.isRegistering = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.register-box {
  width: 480px;
  padding: 40px 45px;
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 24px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 2px rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.register-box h2 {
  text-align: center;
  margin-bottom: 30px;
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
    0 0 0 2px rgba(64, 158, 255, 0.3),
    inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
}

:deep(.el-select .el-select__wrapper) {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(8px);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.06),
    inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 8px;
}

.btn-row {
  display: flex;
  justify-content: center;
  margin-top: 25px;
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
  background: rgba(0, 136, 255, 0.75);
  backdrop-filter: blur(16px) saturate(150%);
  box-shadow:
    0 2px 8px rgba(60, 136, 255, 0.2),
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

.tips {
  margin-top: 20px;
  font-size: 13px;
  color: #666;
  text-align: center;
}

.tips p {
  margin: 5px 0;
}

.back-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
}

.back-link:hover {
  color: #337ecc;
}

/* 手机端适配 (1080P竖屏) */
@media screen and (max-width: 768px) {
  .register-container {
    padding: 20px;
  }
  
  .register-box {
    width: 100%;
    max-width: 400px;
    padding: 30px 25px;
    border-radius: 20px;
  }
  
  .register-box h2 {
    font-size: 20px;
    margin-bottom: 30px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
    width: 80px !important;
  }
  
  :deep(.el-input__wrapper),
  :deep(.el-select__wrapper) {
    height: 40px !important;
  }
  
  :deep(.el-input__inner),
  :deep(.el-select__inner) {
    font-size: 14px;
  }
  
  .btn-row {
    margin-top: 25px;
  }
  
  .glass-btn {
    padding: 12px 30px;
    font-size: 14px;
    width: 100%;
    text-align: center;
  }
  
  .tips {
    font-size: 12px;
    margin-top: 15px;
  }
}
</style>