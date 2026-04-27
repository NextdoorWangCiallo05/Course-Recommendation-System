<template>
  <div class="feedback-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户反馈</span>
          <div>
            <el-button type="primary" @click="showFeedbackDialog = true">提交反馈</el-button>
            <el-button @click="$router.push(isSuperAdmin ? '/admin' : '/student')">返回</el-button>
          </div>
        </div>
      </template>
      <el-table v-if="isSuperAdmin" :data="feedbacks" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户" width="150" />
        <el-table-column prop="content" label="反馈内容" />
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" size="small" @click="handleDeleteFeedback(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-else>
        <el-alert title="提交您的建议或问题，我们将尽快处理" type="info" :closable="false" style="margin-bottom: 20px;" />
        <el-card v-for="fb in myFeedbacks" :key="fb.id" style="margin-bottom: 15px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <p style="margin: 0 0 8px 0; white-space: pre-wrap;">{{ fb.content }}</p>
              <span style="font-size: 12px; color: #909399;">{{ fb.created_at }}</span>
            </div>
            <el-button type="danger" size="small" @click="handleDeleteFeedback(fb)">删除</el-button>
          </div>
        </el-card>
        <el-empty v-if="myFeedbacks.length === 0" description="暂无反馈记录" />
      </div>
    </el-card>

    <el-dialog v-model="showFeedbackDialog" title="提交反馈" width="500px">
      <el-form :model="feedbackForm" label-width="80px">
        <el-form-item label="反馈内容">
          <el-input v-model="feedbackForm.content" type="textarea" :rows="5" placeholder="请输入您的反馈内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showFeedbackDialog = false">取消</el-button>
        <el-button type="primary" @click="submitFeedback">提交</el-button>
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
      feedbacks: [],
      myFeedbacks: [],
      showFeedbackDialog: false,
      feedbackForm: { content: '' }
    }
  },
  computed: {
    isSuperAdmin() {
      return localStorage.getItem('role') === 'superadmin'
    },
    isAdmin() {
      return localStorage.getItem('role') === 'admin'
    }
  },
  async mounted() {
    if (this.isSuperAdmin || this.isAdmin) {
      await this.loadFeedbacks()
    } else {
      await this.loadMyFeedbacks()
    }
  },
  methods: {
    async loadFeedbacks() {
      this.feedbacks = await request.get('/feedbacks')
    },
    async loadMyFeedbacks() {
      const all = await request.get('/feedbacks')
      this.myFeedbacks = all.filter(f => f.user_id === parseInt(localStorage.getItem('user_id')))
    },
    async submitFeedback() {
      if (!this.feedbackForm.content.trim()) {
        ElMessage.warning('请填写反馈内容')
        return
      }
      try {
        await request.post('/feedbacks', { content: this.feedbackForm.content })
        ElMessage.success('反馈提交成功')
        this.showFeedbackDialog = false
        this.feedbackForm = { content: '' }
        if (this.isSuperAdmin || this.isAdmin) {
          await this.loadFeedbacks()
        } else {
          await this.loadMyFeedbacks()
        }
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '提交失败')
      }
    },
    async handleDeleteFeedback(row) {
      try {
        await ElMessageBox.confirm('确定要删除这条反馈吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete(`/feedbacks/${row.id}`)
        ElMessage.success('删除成功')
        if (this.isSuperAdmin || this.isAdmin) {
          await this.loadFeedbacks()
        } else {
          await this.loadMyFeedbacks()
        }
      } catch {
      }
    }
  }
}
</script>

<style scoped>
.feedback-page {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
