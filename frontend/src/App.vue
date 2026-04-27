<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    document.body.style.cssText = `
      font-family: 'Microsoft YaHei', Arial, sans-serif;
      background-color: rgba(255, 255, 255, 0.4);
      background-image: url(/images/dashboard-bg.jpg);
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    `
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
}

#app {
  min-height: 100vh;
}

/* 手机端适配 */
@media screen and (max-width: 768px) {
  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
  }

  #app {
    min-height: 100vh;
  }

  /* 导航栏适配 */
  .navbar {
    padding: 10px 15px !important;
    flex-wrap: wrap;
  }

  .navbar h1 {
    font-size: 16px !important;
    margin: 0 !important;
  }

  .navbar .user-info {
    font-size: 12px;
  }

  /* 搜索表单适配 */
  .search-form {
    padding: 15px !important;
    margin: 10px !important;
  }

  .search-form .el-form {
    flex-direction: column !important;
    gap: 10px !important;
  }

  .search-form .el-select,
  .search-form .el-input {
    width: 100% !important;
    margin-bottom: 5px !important;
  }

  /* 课程卡片适配 */
  .course-grid {
    grid-template-columns: 1fr !important;
    padding: 10px !important;
    gap: 10px !important;
  }

  .course-card {
    margin: 0 !important;
  }

  .course-card .el-card__body {
    padding: 10px !important;
  }

  /* 课程详情适配 */
  .course-detail {
    padding: 15px !important;
    margin: 10px !important;
  }

  /* 表格适配 */
  .el-table {
    font-size: 12px !important;
  }

  .el-table__header th {
    padding: 8px 5px !important;
  }

  .el-table__body td {
    padding: 8px 5px !important;
  }

  /* 按钮适配 */
  .el-button {
    padding: 15px 20px !important;
    font-size: 12px !important;
    border-radius: 20px !important;
  }

  /* 对话框适配 */
  .el-dialog {
    width: 95% !important;
    margin: 10px auto !important;
  }

  .el-dialog__header {
    padding: 10px 15px !important;
  }

  .el-dialog__body {
    padding: 15px !important;
  }

  /* 表单项适配 */
  .el-form-item {
    margin-bottom: 15px !important;
  }

  .el-form-item__label {
    font-size: 13px !important;
  }

  /* 标签适配 */
  .el-tag {
    font-size: 11px !important;
    padding: 0 6px !important;
  }

  /* 评分适配 */
  .rating-info {
    font-size: 12px !important;
  }

  /* 折叠菜单适配 */
  .el-collapse-item__header {
    font-size: 13px !important;
    padding: 10px !important;
  }

  .el-collapse-item__content {
    font-size: 12px !important;
    padding: 10px !important;
  }
}

/* 超小屏幕适配 */
@media screen and (max-width: 480px) {
  .navbar h1 {
    font-size: 14px !important;
  }

  .el-card {
    border-radius: 4px !important;
  }

  .course-title {
    font-size: 14px !important;
  }

  .el-pagination {
    font-size: 11px !important;
    white-space: nowrap !important;
  }
}

/* 全局按钮圆角样式 - 大按钮用于表单提交等主要操作 */
.el-button--large {
  border-radius: 20px !important;
  font-size: 15px !important;
  padding: 18px 20px !important;
}

/* 默认按钮适中 */
.el-button:not(.el-button--small):not(.el-button--large) {
  border-radius: 18px !important;
  font-size: 14px !important;
  padding: 10px 18px !important;
}

/* 表格内小按钮样式优化 */
.el-table .el-button--small {
  padding: 6px 12px !important;
  font-size: 12px !important;
  border-radius: 12px !important;
}

/* 全局小按钮样式 - 适用于课程卡片等 */
.el-button--small {
  padding: 10px 18px !important;
  font-size: 14px !important;
  border-radius: 8px !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

/* 页面切换过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 卡片渐入动画 */
@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 全局输入框和选择框液态玻璃效果 */
.el-input__wrapper {
  background: rgba(255, 255, 255, 0.8) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 10px !important;
  padding: 6px 12px !important;
  height: 40px !important;
  transition: all 0.3s ease !important;
}

.el-input__wrapper:hover {
  box-shadow:
    0 2px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
  border-color: rgba(0, 136, 255, 0.3) !important;
}

.el-input__wrapper.is-focus {
  box-shadow:
    0 0 0 2px rgba(0, 136, 255, 0.25),
    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
  border-color: #0088ff !important;
}

/* 选择框触发器液态玻璃效果 */
.el-select .el-input__wrapper,
.el-select .el-select__wrapper {
  background: rgba(255, 255, 255, 0.8) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 10px !important;
  height: 40px !important;
}

.el-select .el-input__wrapper:hover,
.el-select .el-select__wrapper:hover {
  box-shadow:
    0 2px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
  border-color: rgba(0, 136, 255, 0.3) !important;
}

/* 全局对话框按钮液态玻璃效果 */
.el-message-box .el-button,
.el-dialog .el-dialog__footer .el-button {
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 20px !important;
}

.el-message-box .el-button--primary,
.el-dialog .el-dialog__footer .el-button--primary {
  background: rgba(0, 136, 255, 0.7) !important;
  color: #fff !important;
  border-radius: 20px !important;
}

.el-message-box .el-button--primary:hover:not(:disabled),
.el-dialog .el-dialog__footer .el-button--primary:hover:not(:disabled) {
  background: rgba(0, 136, 255, 0.9) !important;
  border-radius: 20px !important;
}

.el-message-box .el-button--default,
.el-dialog .el-dialog__footer .el-button--default {
  background: rgba(255, 255, 255, 0.4) !important;
  border-radius: 20px !important;
}

.el-message-box .el-button--default:hover:not(:disabled),
.el-dialog .el-dialog__footer .el-button--default:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.6) !important;
  border-radius: 20px !important;
}

/* 全局下拉菜单液态玻璃效果 */
.el-select-dropdown {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border-radius: 12px !important;
  overflow: hidden;
}

.el-select-dropdown__item {
  color: #333 !important;
  transition: all 0.2s ease;
  border-radius: 8px !important;
  margin: 2px 8px !important;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background: rgba(0, 136, 255, 0.12) !important;
  color: #0088ff !important;
  border-radius: 8px !important;
}

.el-select-dropdown__item.is-selected {
  background: rgba(0, 136, 255, 0.9) !important;
  color: #fff !important;
  font-weight: 600;
  border-radius: 8px !important;
  margin: 2px 8px !important;
}

.el-popper.is-light {
  border: none !important;
  box-shadow: none !important;
}

/* 全局弹出框（popper）毛玻璃效果 */
.el-popper.is-light .el-select-dropdown {
  margin-top: 4px !important;
}
</style>
