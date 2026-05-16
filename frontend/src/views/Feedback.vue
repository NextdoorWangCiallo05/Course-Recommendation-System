<template>
  <div class="feedback-page">
    <n-card>
      <template #header>
        <div class="card-header">
          <span style="font-size: 18px; font-weight: 600;">用户反馈</span>
          <n-space>
            <n-button type="primary" @click="showFeedbackDialog = true">提交反馈</n-button>
            <n-button @click="$router.push(isSuperAdmin ? '/admin' : '/student')">返回</n-button>
          </n-space>
        </div>
      </template>

      <n-data-table v-if="isSuperAdmin" :columns="adminColumns" :data="feedbacks" :bordered="false" :single-line="false" />

      <div v-else>
        <n-alert title="提交您的建议或问题，我们将尽快处理" type="info" :closable="false" style="margin-bottom: 20px;" />
        <n-card v-for="fb in myFeedbacks" :key="fb.id" size="small" style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
              <p style="margin: 0 0 6px 0; white-space: pre-wrap;">{{ fb.content }}</p>
              <n-text depth="3" style="font-size: 12px;">{{ fb.created_at }}</n-text>
            </div>
            <n-button type="error" size="small" @click="handleDeleteFeedback(fb)">删除</n-button>
          </div>
        </n-card>
        <n-empty v-if="myFeedbacks.length === 0" description="暂无反馈记录" />
      </div>
    </n-card>

    <n-modal v-model:show="showFeedbackDialog" title="提交反馈" preset="card" :style="{ maxWidth: '500px' }" :mask-closable="false">
      <n-form :model="feedbackForm">
        <n-form-item label="反馈内容">
          <n-input v-model:value="feedbackForm.content" type="textarea" :rows="5" placeholder="请输入您的反馈内容" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showFeedbackDialog = false">取消</n-button>
          <n-button type="primary" @click="submitFeedback">提交</n-button>
        </n-space>
      </template>
    </n-modal>
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
    },
    adminColumns() {
      return [
        { title: 'ID', key: 'id', width: 80 },
        { title: '用户', key: 'username', width: 150 },
        { title: '反馈内容', key: 'content' },
        { title: '提交时间', key: 'created_at', width: 180 },
        {
          title: '操作',
          key: 'actions',
          width: 100,
          render: (row) => h('span', null, [
            h('n-button', {
              type: 'error',
              size: 'small',
              onClick: () => this.handleDeleteFeedback(row)
            }, () => '删除')
          ])
        }
      ]
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
        this.message.warning('请填写反馈内容')
        return
      }
      try {
        await request.post('/feedbacks', { content: this.feedbackForm.content })
        this.message.success('反馈提交成功')
        this.showFeedbackDialog = false
        this.feedbackForm = { content: '' }
        if (this.isSuperAdmin || this.isAdmin) {
          await this.loadFeedbacks()
        } else {
          await this.loadMyFeedbacks()
        }
      } catch (e) {
        this.message.error(e.response?.data?.msg || '提交失败')
      }
    },
    async handleDeleteFeedback(row) {
      this.dialog.warning({
        title: '提示',
        content: '确定要删除这条反馈吗？',
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.delete(`/feedbacks/${row.id}`)
            this.message.success('删除成功')
            if (this.isSuperAdmin || this.isAdmin) {
              await this.loadFeedbacks()
            } else {
              await this.loadMyFeedbacks()
            }
          } catch {
            this.message.error('删除失败')
          }
        }
      })
    }
  }
})
</script>

<style scoped>
.feedback-page {
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
