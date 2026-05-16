<template>
  <div class="user-center">
    <n-card>
      <template #header>
        <div class="card-header">
          <n-button @click="goBack">返回</n-button>
          <span class="title">用户中心</span>
        </div>
      </template>
      <n-tabs v-model:value="activeTab" type="segment" animated>
        <n-tab-pane name="profile" tab="个人信息">
          <n-form :model="profileForm" label-placement="left" label-width="100px" style="max-width: 500px;">
            <n-form-item label="用户名">
              <n-input v-model:value="profileForm.username" disabled />
            </n-form-item>
            <n-form-item label="学号">
              <n-input v-model:value="profileForm.student_id" placeholder="请输入学号" />
            </n-form-item>
            <n-form-item label="真实姓名">
              <n-input v-model:value="profileForm.real_name" placeholder="请输入真实姓名" />
            </n-form-item>
            <n-form-item>
              <n-button type="primary" @click="updateProfile">保存</n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>
        <n-tab-pane name="password" tab="修改密码">
          <n-form :model="passwordForm" label-placement="left" label-width="100px" style="max-width: 500px;">
            <n-form-item label="原密码">
              <n-input v-model:value="passwordForm.old_password" type="password" placeholder="请输入原密码" show-password-on="click" />
            </n-form-item>
            <n-form-item label="新密码">
              <n-input v-model:value="passwordForm.new_password" type="password" placeholder="请输入新密码（至少6位）" show-password-on="click" />
            </n-form-item>
            <n-form-item label="确认密码">
              <n-input v-model:value="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password-on="click" />
            </n-form-item>
            <n-form-item>
              <n-button type="primary" @click="changePassword">修改密码</n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>
        <n-tab-pane name="delete" tab="注销账号">
          <div style="max-width: 500px;">
            <n-alert title="注销账号后，您的所有数据将被永久删除且无法恢复，请谨慎操作。" type="warning" :closable="false" style="margin-bottom: 20px;" />
            <n-button type="error" @click="confirmDeleteAccount">注销账号</n-button>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import request from '../api'

export default defineComponent({
  setup() {
    const message = useMessage()
    const dialog = useDialog()
    return { message, dialog }
  },
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
  },
  methods: {
    goBack() {
      const role = localStorage.getItem('role')
      this.$router.push(role === 'admin' || role === 'superadmin' ? '/admin' : '/student')
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
        this.message.error(e.response?.data?.msg || '加载失败')
      }
    },
    async updateProfile() {
      try {
        await request.put('/user/profile', {
          student_id: this.profileForm.student_id,
          real_name: this.profileForm.real_name
        })
        this.message.success('信息更新成功')
      } catch (e) {
        this.message.error(e.response?.data?.msg || '更新失败')
      }
    },
    async changePassword() {
      const f = this.passwordForm
      if (!f.old_password || !f.new_password || !f.confirm_password) {
        this.message.warning('请填写完整信息')
        return
      }
      if (f.new_password !== f.confirm_password) {
        this.message.warning('两次输入的密码不一致')
        return
      }
      if (f.new_password.length < 6) {
        this.message.warning('新密码长度不能少于6位')
        return
      }
      try {
        await request.put('/user/password', {
          old_password: f.old_password,
          new_password: f.new_password
        })
        this.message.success('密码修改成功，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        localStorage.removeItem('username')
        localStorage.removeItem('user_id')
        this.$router.push('/login')
      } catch (e) {
        this.message.error(e.response?.data?.msg || '修改失败')
      }
    },
    confirmDeleteAccount() {
      this.dialog.warning({
        title: '警告',
        content: '注销账号后所有数据将被永久删除，确定要注销吗？',
        positiveText: '确定注销',
        negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.delete('/user/account')
            this.message.success('账号已注销')
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            localStorage.removeItem('username')
            localStorage.removeItem('user_id')
            this.$router.push('/login')
          } catch {
            this.message.error('注销失败')
          }
        }
      })
    }
  }
})
</script>

<style scoped>
.user-center {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
  min-height: calc(100vh - 48px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

@media screen and (max-width: 768px) {
  .user-center {
    padding: 12px;
  }
}
</style>
