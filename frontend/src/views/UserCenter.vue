<template>
  <div class="user-center">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button @click="goBack">返回</el-button>
          <span class="title">用户中心</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="个人信息" name="profile">
          <el-form :model="profileForm" label-width="100px" style="max-width: 500px;">
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="学号">
              <el-input v-model="profileForm.student_id" placeholder="请输入学号" />
            </el-form-item>
            <el-form-item label="真实姓名">
              <el-input v-model="profileForm.real_name" placeholder="请输入真实姓名" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updateProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="修改密码" name="password">
          <el-form :model="passwordForm" label-width="100px" style="max-width: 500px;">
            <el-form-item label="原密码">
              <el-input v-model="passwordForm.old_password" type="password" placeholder="请输入原密码" show-password />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码（至少6位）" show-password />
            </el-form-item>
            <el-form-item label="确认密码">
              <el-input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注销账号" name="delete">
          <div style="max-width: 500px;">
            <el-alert title="注销账号后，您的所有数据将被永久删除且无法恢复，请谨慎操作。" type="warning" :closable="false" style="margin-bottom: 20px;" />
            <el-button type="danger" @click="confirmDeleteAccount">注销账号</el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import request from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  data() {
    return {
      activeTab: 'profile',
      profileForm: {
        username: '',
        student_id: '',
        real_name: ''
      },
      passwordForm: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
  },
  async mounted() {
    await this.loadProfile()
    this.$el.style.cssText = `
      background-color: rgba(255, 255, 255, 0.4);
      background-image: url(/images/dashboard-bg.jpg);
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    `
  },
  methods: {
    goBack() {
      const role = localStorage.getItem('role')
      if (role === 'admin' || role === 'superadmin') {
        this.$router.push('/admin')
      } else {
        this.$router.push('/student')
      }
    },
    async loadProfile() {
      try {
        const res = await request.get('/user/profile')
        this.profileForm = {
          username: res.username,
          student_id: res.student_id || '',
          real_name: res.real_name || ''
        }
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '加载失败')
      }
    },
    async updateProfile() {
      try {
        await request.put('/user/profile', {
          student_id: this.profileForm.student_id,
          real_name: this.profileForm.real_name
        })
        ElMessage.success('信息更新成功')
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '更新失败')
      }
    },
    async changePassword() {
      if (!this.passwordForm.old_password || !this.passwordForm.new_password || !this.passwordForm.confirm_password) {
        ElMessage.warning('请填写完整信息')
        return
      }
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        ElMessage.warning('两次输入的密码不一致')
        return
      }
      if (this.passwordForm.new_password.length < 6) {
        ElMessage.warning('新密码长度不能少于6位')
        return
      }
      try {
        await request.put('/user/password', {
          old_password: this.passwordForm.old_password,
          new_password: this.passwordForm.new_password
        })
        ElMessage.success('密码修改成功，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        localStorage.removeItem('username')
        localStorage.removeItem('user_id')
        this.$router.push('/login')
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '修改失败')
      }
    },
    async confirmDeleteAccount() {
      try {
        await ElMessageBox.confirm('注销账号后所有数据将被永久删除，确定要注销吗？', '警告', {
          confirmButtonText: '确定注销',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete('/user/account')
        ElMessage.success('账号已注销')
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        localStorage.removeItem('username')
        localStorage.removeItem('user_id')
        this.$router.push('/login')
      } catch {
      }
    }
  }
}
</script>

<style scoped>
.user-center {
  padding: 20px;
  min-height: calc(100vh - 40px);
}

.user-center :deep(.el-card) {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

/* 标签页分段控制器样式 */
.user-center :deep(.el-tabs) {
  display: flex;
  justify-content: center;
  background: rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  padding: 4px;
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  margin-bottom: 20px;
}

.user-center :deep(.el-tabs__header) {
  margin: 0;
  border: none;
  display: flex;
  align-items: center;
}

.user-center :deep(.el-tabs__nav-wrap) {
  margin: 0;
  display: flex;
  align-items: center;
  border: none !important;
  padding: 0 !important;
}

.user-center :deep(.el-tabs__nav-wrap::after) {
  display: none !important;
}

.user-center :deep(.el-tabs__nav) {
  border: none;
  display: flex;
  gap: 2px;
  align-items: center;
  border-bottom: none !important;
}

.user-center :deep(.el-tabs__item) {
  border: none !important;
  border-radius: 20px;
  padding: 0 28px !important;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: inline-flex !important;
  justify-content: center !important;
  align-items: center !important;
  text-align: center !important;
  white-space: nowrap;
  min-width: 80px;
  height: 40px !important;
  line-height: 1 !important;
  width: auto !important;
}

.user-center :deep(.el-tabs__item:hover) {
  color: #333;
}

.user-center :deep(.el-tabs__item.is-active) {
  background: linear-gradient(135deg, #0091FF 0%, #1E6EF4 100%);
  color: #fff;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.35);
}

.user-center :deep(.el-tabs__active-bar) {
  display: none !important;
}

/* 输入框液态玻璃效果 */
.user-center :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.4) !important;
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 12px !important;
  height: 40px !important;
}

.user-center :deep(.el-input__wrapper:hover) {
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

.user-center :deep(.el-input__wrapper.is-focus) {
  box-shadow:
    0 0 0 2px rgba(0, 145, 255, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

.user-center :deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.4) !important;
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 12px !important;
  height: 40px !important;
}

.user-center :deep(.el-select .el-input__wrapper:hover) {
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

.user-center :deep(.el-select .el-input__wrapper.is-focus) {
  box-shadow:
    0 0 0 2px rgba(0, 145, 255, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

/* 下拉菜单液态玻璃效果 */
.user-center :deep(.el-select-dropdown) {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.12),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 12px !important;
}

.user-center :deep(.el-select-dropdown__item) {
  border-radius: 8px !important;
  margin: 4px 8px !important;
  transition: all 0.3s ease !important;
}

.user-center :deep(.el-select-dropdown__item:hover) {
  background: rgba(0, 145, 255, 0.1) !important;
}

.user-center :deep(.el-select-dropdown__item.selected) {
  background: linear-gradient(135deg, #0091FF 0%, #1E6EF4 100%) !important;
  color: #fff !important;
  font-weight: 500 !important;
}

/* 按钮液态玻璃效果 */
:deep(.el-button) {
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 20px !important;
  padding: 10px 20px !important;
}

:deep(.el-button--primary) {
  background: rgba(64, 158, 255, 0.75) !important;
}

:deep(.el-button--primary:hover:not(:disabled)) {
  background: rgba(64, 158, 255, 0.9) !important;
}

:deep(.el-button--success) {
  background: rgba(103, 194, 58, 0.75) !important;
}

:deep(.el-button--success:hover:not(:disabled)) {
  background: rgba(103, 194, 58, 0.9) !important;
}

:deep(.el-button--warning) {
  background: rgba(230, 162, 60, 0.75) !important;
}

:deep(.el-button--warning:hover:not(:disabled)) {
  background: rgba(230, 162, 60, 0.9) !important;
}

:deep(.el-button--danger) {
  background: rgba(245, 108, 108, 0.75) !important;
}

:deep(.el-button--danger:hover:not(:disabled)) {
  background: rgba(245, 108, 108, 0.9) !important;
}

:deep(.el-button--info) {
  background: rgba(144, 147, 153, 0.5) !important;
}

:deep(.el-button--info:hover:not(:disabled)) {
  background: rgba(144, 147, 153, 0.7) !important;
}

:deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.4) !important;
}

:deep(.el-button--default:hover:not(:disabled)) {
  background: rgba(255, 255, 255, 0.6) !important;
}

/* 手机端适配 (1080P竖屏) */
@media screen and (max-width: 768px) {
  .user-center {
    padding: 10px;
    min-height: calc(100vh - 20px);
  }
  
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .card-header .el-button {
    font-size: 12px;
    padding: 6px 12px !important;
  }
  
  .title {
    font-size: 18px;
  }
  
  .el-tabs {
    margin-top: 10px;
  }
  
  .user-center :deep(.el-tabs__item) {
    padding: 0 16px !important;
    font-size: 13px;
    min-width: 60px;
  }
  
  .el-form {
    max-width: 100% !important;
  }
  
  .el-form-item__label {
    width: 80px !important;
    font-size: 14px;
  }
  
  .el-input__wrapper {
    height: 40px !important;
  }
  
  .el-input__inner {
    font-size: 14px;
  }
  
  .el-button {
    font-size: 14px;
    padding: 8px 16px !important;
  }
  
  .el-alert {
    font-size: 14px;
  }
}
</style>
