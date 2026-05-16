<template>
  <div class="user-management">
    <n-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <n-button @click="goBack">返回</n-button>
            <span class="title">账户管理</span>
          </div>
          <n-space>
            <n-button @click="toggleDecrypt">{{ showRealInfo ? '隐藏信息' : '显示完整信息' }}</n-button>
            <n-button type="success" @click="showCreateDialog">新建账户</n-button>
            <n-button type="primary" @click="loadUsers">刷新</n-button>
          </n-space>
        </div>
      </template>

      <n-data-table
        :columns="columns"
        :data="users"
        :bordered="false"
        :single-line="false"
        :row-key="row => row.id"
      />

      <n-modal v-model:show="roleDialogVisible" title="修改角色" preset="card" :style="{ maxWidth: '420px' }" :mask-closable="false">
        <n-form :model="roleForm" label-placement="left" label-width="80px">
          <n-form-item label="用户名">
            <n-input v-model:value="roleForm.username" disabled />
          </n-form-item>
          <n-form-item label="新角色">
            <n-select v-model:value="roleForm.role" :options="roleOptions" />
          </n-form-item>
        </n-form>
        <template #footer>
          <n-space justify="end">
            <n-button @click="roleDialogVisible = false">取消</n-button>
            <n-button type="primary" @click="submitRoleChange">确定</n-button>
          </n-space>
        </template>
      </n-modal>

      <n-modal v-model:show="createDialogVisible" title="新建账户" preset="card" :style="{ maxWidth: '500px' }" :mask-closable="false">
        <n-form :model="createForm" label-placement="left" label-width="100px">
          <n-form-item label="学号">
            <n-input v-model:value="createForm.student_id" placeholder="请输入学号" />
          </n-form-item>
          <n-form-item label="真实姓名">
            <n-input v-model:value="createForm.real_name" placeholder="请输入真实姓名" />
          </n-form-item>
          <n-form-item label="用户名">
            <n-input v-model:value="createForm.username" placeholder="请输入用户名" />
          </n-form-item>
          <n-form-item label="密码">
            <n-input v-model:value="createForm.password" type="password" placeholder="请输入密码" show-password-on="click" />
          </n-form-item>
          <n-form-item label="角色">
            <n-select v-model:value="createForm.role" :options="roleOptions" />
          </n-form-item>
        </n-form>
        <template #footer>
          <n-space justify="end">
            <n-button @click="createDialogVisible = false">取消</n-button>
            <n-button type="primary" @click="submitCreate">确定</n-button>
          </n-space>
        </template>
      </n-modal>
    </n-card>
  </div>
</template>

<script>
import { defineComponent, h } from 'vue'
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
      users: [],
      showRealInfo: false,
      roleDialogVisible: false,
      createDialogVisible: false,
      roleForm: { id: null, username: '', role: 'student' },
      createForm: { student_id: '', real_name: '', username: '', password: '', role: 'student' },
      currentUsername: localStorage.getItem('username'),
      roleOptions: [
        { label: '学生', value: 'student' },
        { label: '管理员', value: 'admin' }
      ]
    }
  },
  computed: {
    columns() {
      return [
        { title: 'ID', key: 'id', width: 80 },
        { title: '学号', key: 'student_id', width: 150 },
        { title: '真实姓名', key: 'real_name', width: 120 },
        { title: '用户名', key: 'username', width: 150 },
        {
          title: '角色',
          key: 'role',
          width: 120,
          render: (row) => {
            const typeMap = {
              student: 'info',
              admin: 'primary',
              superadmin: 'error',
              pending: 'warning'
            }
            const labelMap = {
              student: '学生',
              admin: '管理员',
              superadmin: '超级管理员',
              pending: '待审核'
            }
            return h('n-tag', { type: typeMap[row.role] || 'info', size: 'small' }, () => labelMap[row.role] || row.role)
          }
        },
        {
          title: '申请角色',
          key: 'requested_role',
          width: 120,
          render: (row) => {
            if (row.requested_role) {
              const labelMap = { student: '学生', admin: '管理员' }
              return h('n-tag', { type: 'warning', size: 'small' }, () => labelMap[row.requested_role] || row.requested_role)
            }
            return h('span', '-')
          }
        },
        { title: '创建时间', key: 'created_at', width: 180 },
        {
          title: '操作',
          key: 'actions',
          minWidth: 300,
          render: (row) => {
            const btns = []
            if (row.role === 'pending') {
              btns.push(h('n-button', { type: 'success', size: 'small', style: 'margin-right:6px', onClick: () => this.handleApprove(row, 'student') }, () => '通过为学生'))
              btns.push(h('n-button', { type: 'primary', size: 'small', style: 'margin-right:6px', onClick: () => this.handleApprove(row, 'admin') }, () => '通过为管理员'))
              btns.push(h('n-button', { type: 'error', size: 'small', style: 'margin-right:6px', onClick: () => this.handleReject(row) }, () => '拒绝'))
            }
            if (row.role !== 'pending' && row.role !== 'superadmin') {
              btns.push(h('n-button', { type: 'warning', size: 'small', style: 'margin-right:6px', onClick: () => this.handleChangeRole(row) }, () => '修改角色'))
            }
            if (row.username !== this.currentUsername && row.role !== 'superadmin') {
              btns.push(h('n-button', { type: 'error', size: 'small', style: 'margin-right:6px', onClick: () => this.handleDelete(row) }, () => '注销'))
            }
            return h('span', null, btns)
          }
        }
      ]
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    goBack() {
      localStorage.setItem('adminMode', 'true')
      this.$router.push('/admin')
    },
    async loadUsers() {
      try {
        this.users = await request.get('/users', { params: { decrypt: this.showRealInfo } })
      } catch (e) {
        this.message.error(e.response?.data?.msg || '加载失败')
      }
    },
    toggleDecrypt() {
      this.showRealInfo = !this.showRealInfo
      this.loadUsers()
    },
    handleApprove(row, role) {
      const roleName = role === 'student' ? '学生' : '管理员'
      this.dialog.info({
        title: '确认',
        content: `确定通过 ${row.username} 的注册申请，角色为${roleName}？`,
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.put(`/users/${row.id}/approve`, { action: 'approve', role })
            this.message.success('审核通过')
            this.loadUsers()
          } catch (e) {
            this.message.error(e.response?.data?.msg || '操作失败')
          }
        }
      })
    },
    handleReject(row) {
      this.dialog.info({
        title: '确认',
        content: `确定拒绝 ${row.username} 的注册申请？`,
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.put(`/users/${row.id}/approve`, { action: 'reject' })
            this.message.success('已拒绝')
            this.loadUsers()
          } catch (e) {
            this.message.error(e.response?.data?.msg || '操作失败')
          }
        }
      })
    },
    handleChangeRole(row) {
      this.roleForm = { id: row.id, username: row.username, role: row.role }
      this.roleDialogVisible = true
    },
    async submitRoleChange() {
      try {
        await request.put(`/users/${this.roleForm.id}/role`, { role: this.roleForm.role })
        this.message.success('角色已更新')
        this.roleDialogVisible = false
        this.loadUsers()
      } catch (e) {
        this.message.error(e.response?.data?.msg || '操作失败')
      }
    },
    handleDelete(row) {
      this.dialog.warning({
        title: '确认',
        content: `确定注销用户 ${row.username}？此操作不可恢复！`,
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.delete(`/users/${row.id}`)
            this.message.success('账户已注销')
            this.loadUsers()
          } catch (e) {
            this.message.error(e.response?.data?.msg || '操作失败')
          }
        }
      })
    },
    showCreateDialog() {
      this.createForm = { student_id: '', real_name: '', username: '', password: '', role: 'student' }
      this.createDialogVisible = true
    },
    async submitCreate() {
      const f = this.createForm
      if (!f.student_id || !f.real_name || !f.username || !f.password) {
        this.message.warning('请填写完整信息')
        return
      }
      try {
        await request.post('/users', this.createForm)
        this.message.success('账户创建成功')
        this.createDialogVisible = false
        this.loadUsers()
      } catch (e) {
        this.message.error(e.response?.data?.msg || '创建失败')
      }
    }
  }
})
</script>

<style scoped>
.user-management {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

@media screen and (max-width: 768px) {
  .user-management {
    padding: 12px;
  }
  .card-header {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
