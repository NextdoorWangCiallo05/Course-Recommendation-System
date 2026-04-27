<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button @click="goBack">返回</el-button>
            <span class="title">账户管理</span>
          </div>
          <div>
            <el-button type="info" @click="toggleDecrypt">{{ showRealInfo ? '隐藏信息' : '显示完整信息' }}</el-button>
            <el-button type="success" @click="showCreateDialog">新建账户</el-button>
            <el-button type="primary" @click="loadUsers">刷新</el-button>
          </div>
        </div>
      </template>
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="student_id" label="学号" width="150" />
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleName(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申请角色" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.requested_role" type="warning">
              {{ getRoleName(row.requested_role) }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" min-width="250">
          <template #default="{ row }">
            <el-button
              v-if="row.role === 'pending'"
              type="success"
              size="small"
              @click="handleApprove(row, 'student')"
            >
              通过为学生
            </el-button>
            <el-button
              v-if="row.role === 'pending'"
              type="primary"
              size="small"
              @click="handleApprove(row, 'admin')"
            >
              通过为管理员
            </el-button>
            <el-button
              v-if="row.role === 'pending'"
              type="danger"
              size="small"
              @click="handleReject(row)"
            >
              拒绝
            </el-button>
            <el-button
              v-if="row.role !== 'pending' && row.role !== 'superadmin'"
              type="warning"
              size="small"
              @click="handleChangeRole(row)"
            >
              修改角色
            </el-button>
            <el-button
              v-if="row.username !== currentUsername && row.role !== 'superadmin'"
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              注销
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 修改角色对话框 -->
    <el-dialog v-model="roleDialogVisible" title="修改角色" width="400px">
      <el-form :model="roleForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="roleForm.username" disabled />
        </el-form-item>
        <el-form-item label="新角色">
          <el-select v-model="roleForm.role" placeholder="请选择角色">
            <el-option label="学生" value="student" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRoleChange">确定</el-button>
      </template>
    </el-dialog>

    <!-- 新建账户对话框 -->
    <el-dialog v-model="createDialogVisible" title="新建账户" width="500px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="学号">
          <el-input v-model="createForm.student_id" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="createForm.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="createForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="createForm.password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="createForm.role" placeholder="请选择角色">
            <el-option label="学生" value="student" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import request from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  data() {
    return {
      users: [],
      showRealInfo: false,
      roleDialogVisible: false,
      createDialogVisible: false,
      roleForm: {
        id: null,
        username: '',
        role: 'student'
      },
      createForm: {
        student_id: '',
        real_name: '',
        username: '',
        password: '',
        role: 'student'
      },
      currentUsername: localStorage.getItem('username')
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
        ElMessage.error(e.response?.data?.msg || '加载失败')
      }
    },
    toggleDecrypt() {
      this.showRealInfo = !this.showRealInfo
      this.loadUsers()
    },
    getRoleName(role) {
      const map = {
        'student': '学生',
        'admin': '管理员',
        'superadmin': '超级管理员',
        'pending': '待审核'
      }
      return map[role] || role
    },
    getRoleType(role) {
      const map = {
        'student': 'info',
        'admin': 'primary',
        'superadmin': 'danger',
        'pending': 'warning'
      }
      return map[role] || 'info'
    },
    async handleApprove(row, role) {
      try {
        await ElMessageBox.confirm(`确定通过 ${row.username} 的注册申请，角色为${this.getRoleName(role)}？`, '确认')
        await request.put(`/users/${row.id}/approve`, { action: 'approve', role })
        ElMessage.success('审核通过')
        this.loadUsers()
      } catch (e) {
        if (e !== 'cancel') {
          ElMessage.error(e.response?.data?.msg || '操作失败')
        }
      }
    },
    async handleReject(row) {
      try {
        await ElMessageBox.confirm(`确定拒绝 ${row.username} 的注册申请？`, '确认')
        await request.put(`/users/${row.id}/approve`, { action: 'reject' })
        ElMessage.success('已拒绝')
        this.loadUsers()
      } catch (e) {
        if (e !== 'cancel') {
          ElMessage.error(e.response?.data?.msg || '操作失败')
        }
      }
    },
    handleChangeRole(row) {
      this.roleForm = {
        id: row.id,
        username: row.username,
        role: row.role
      }
      this.roleDialogVisible = true
    },
    async submitRoleChange() {
      try {
        await request.put(`/users/${this.roleForm.id}/role`, { role: this.roleForm.role })
        ElMessage.success('角色已更新')
        this.roleDialogVisible = false
        this.loadUsers()
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '操作失败')
      }
    },
    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(`确定注销用户 ${row.username}？此操作不可恢复！`, '确认', { type: 'warning' })
        await request.delete(`/users/${row.id}`)
        ElMessage.success('账户已注销')
        this.loadUsers()
      } catch (e) {
        if (e !== 'cancel') {
          ElMessage.error(e.response?.data?.msg || '操作失败')
        }
      }
    },
    showCreateDialog() {
      this.createForm = {
        student_id: '',
        real_name: '',
        username: '',
        password: '',
        role: 'student'
      }
      this.createDialogVisible = true
    },
    async submitCreate() {
      if (!this.createForm.student_id || !this.createForm.real_name || !this.createForm.username || !this.createForm.password) {
        ElMessage.warning('请填写完整信息')
        return
      }
      try {
        await request.post('/users', this.createForm)
        ElMessage.success('账户创建成功')
        this.createDialogVisible = false
        this.loadUsers()
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '创建失败')
      }
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

:deep(.el-button) {
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

:deep(.el-button--primary) {
  background: rgba(0, 136, 255, 0.7) !important;
}

:deep(.el-button--primary:hover:not(:disabled)) {
  background: rgba(0, 136, 255, 0.9) !important;
}

:deep(.el-button--success) {
  background: rgba(52, 199, 89, 0.7) !important;
}

:deep(.el-button--success:hover:not(:disabled)) {
  background: rgba(152, 199, 89, 0.9) !important;
}

:deep(.el-button--warning) {
  background: rgba(255, 204, 0, 0.7) !important;
}

:deep(.el-button--warning:hover:not(:disabled)) {
  background: rgba(255, 204, 0, 0.9) !important;
}

:deep(.el-button--danger) {
  background: rgba(255, 56, 50, 0.7) !important;
}

:deep(.el-button--danger:hover:not(:disabled)) {
  background: rgba(255, 56, 50, 0.9) !important;
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
  .user-management {
    padding: 10px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .header-left {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .header-left .el-button {
    font-size: 12px;
    padding: 6px 12px;
  }
  
  .title {
    font-size: 18px;
  }
  
  .card-header > div {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .card-header .el-button {
    font-size: 12px;
    padding: 6px 12px;
  }
  
  .el-table {
    font-size: 12px;
  }
  
  .el-table th,
  .el-table td {
    padding: 8px !important;
  }
  
  .el-table-column {
    width: auto !important;
    min-width: 80px !important;
  }
  
  .el-tag {
    font-size: 11px;
    padding: 2px 8px;
  }
  
  .el-button {
    font-size: 11px;
    padding: 4px 8px;
    margin-right: 4px;
    margin-bottom: 4px;
  }
  
  .el-dialog {
    width: 90% !important;
    max-width: 400px;
  }
  
  .el-dialog__header {
    padding: 15px;
  }
  
  .el-dialog__title {
    font-size: 16px;
  }
  
  .el-dialog__body {
    padding: 15px;
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
  
  .el-dialog__footer {
    padding: 15px;
    flex-direction: column;
    gap: 8px;
  }
  
  .el-dialog__footer .el-button {
    font-size: 14px;
    padding: 8px 16px;
    width: 100%;
  }
}
</style>
