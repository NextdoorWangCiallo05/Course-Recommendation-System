<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#f56c6c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
      <h3>页面加载异常</h3>
      <p>{{ errorMessage }}</p>
      <el-button type="primary" @click="handleRetry">重新加载</el-button>
    </div>
  </div>
  <slot v-else />
</template>

<script>
import { ref, onErrorCaptured } from 'vue'

export default {
  name: 'ErrorBoundary',
  setup() {
    const hasError = ref(false)
    const errorMessage = ref('')

    onErrorCaptured((err) => {
      hasError.value = true
      errorMessage.value = err.message || '未知错误'
      console.error('ErrorBoundary caught:', err)
      return false
    })

    const handleRetry = () => {
      hasError.value = false
      errorMessage.value = ''
      window.location.reload()
    }

    return { hasError, errorMessage, handleRetry }
  }
}
</script>

<style scoped>
.error-boundary {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.error-content {
  text-align: center;
  padding: 40px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}

.error-content h3 {
  margin: 16px 0 8px;
  color: #333;
  font-size: 18px;
}

.error-content p {
  color: #999;
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
