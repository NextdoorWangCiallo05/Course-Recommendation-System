<template>
  <div id="app">
    <error-boundary>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </error-boundary>
    <div class="icp-footer">
      <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">
        鲁ICP备2026021969号
      </a>
    </div>
  </div>
</template>

<script>
import ErrorBoundary from './components/ErrorBoundary.vue'

export default {
  name: 'App',
  components: { ErrorBoundary },
  mounted() {
    const isDark = localStorage.getItem('darkMode') === 'true'
    if (isDark) {
      document.documentElement.classList.add('dark-mode')
    }
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

  .course-card {
    margin: 0 !important;
  }

  .course-card .el-card__body {
    padding: 10px !important;
  }

  .el-table {
    font-size: 12px !important;
  }

  .el-table__header th {
    padding: 8px 5px !important;
  }

  .el-table__body td {
    padding: 8px 5px !important;
  }

  .el-button {
    padding: 15px 20px !important;
    font-size: 12px !important;
    border-radius: 20px !important;
  }

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

  .el-form-item {
    margin-bottom: 15px !important;
  }

  .el-form-item__label {
    font-size: 13px !important;
  }

  .el-tag {
    font-size: 11px !important;
    padding: 0 6px !important;
  }

  .rating-info {
    font-size: 12px !important;
  }

  .el-collapse-item__header {
    font-size: 13px !important;
    padding: 10px !important;
  }

  .el-collapse-item__content {
    font-size: 12px !important;
    padding: 10px !important;
  }
}

@media screen and (max-width: 480px) {
  .el-card {
    border-radius: 4px !important;
  }

  .el-pagination {
    font-size: 11px !important;
    white-space: nowrap !important;
  }
}

.el-button--large {
  border-radius: 20px !important;
  font-size: 15px !important;
  padding: 18px 20px !important;
}

.el-button:not(.el-button--small):not(.el-button--large) {
  border-radius: 18px !important;
  font-size: 14px !important;
  padding: 10px 18px !important;
}

.el-table .el-button--small {
  padding: 6px 12px !important;
  font-size: 12px !important;
  border-radius: 12px !important;
}

.el-button--small {
  padding: 10px 18px !important;
  font-size: 14px !important;
  border-radius: 8px !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

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

.el-popper.is-light .el-select-dropdown {
  margin-top: 4px !important;
}

.el-dialog {
  border-radius: 20px !important;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.92) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow:
    0 16px 48px rgba(0, 0, 0, 0.15),
    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
}

.el-dialog__header {
  padding: 18px 22px 12px !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

.el-dialog__title {
  font-size: 17px !important;
  font-weight: 600 !important;
  color: #333 !important;
}

.el-dialog__body {
  padding: 20px 22px !important;
}

.el-dialog__footer {
  padding: 14px 22px 20px !important;
  border-top: 1px solid rgba(0, 0, 0, 0.05) !important;
}

.el-dialog__headerbtn .el-dialog__close {
  color: #999 !important;
  font-size: 18px !important;
  transition: all 0.2s ease !important;
}

.el-dialog__headerbtn:hover .el-dialog__close {
  color: #333 !important;
  transform: rotate(90deg);
}

.el-tag {
  border-radius: 8px !important;
  border: none !important;
  backdrop-filter: blur(8px);
  font-size: 12px !important;
  padding: 0 10px !important;
  height: 24px !important;
  line-height: 24px !important;
}

.el-tag--info {
  background: rgba(144, 147, 153, 0.15) !important;
  color: #666 !important;
}

.el-tag--success {
  background: rgba(103, 194, 58, 0.15) !important;
  color: #52c41a !important;
}

.el-tag--danger {
  background: rgba(255, 77, 79, 0.15) !important;
  color: #f5222d !important;
}

.el-tag--warning {
  background: rgba(250, 173, 20, 0.15) !important;
  color: #faad14 !important;
}

.el-descriptions {
  border-radius: 12px !important;
  overflow: hidden;
}

.el-descriptions__label {
  background: linear-gradient(135deg, #f8f9fb 0%, #eef1f5 100%) !important;
  color: #555 !important;
  font-weight: 500 !important;
  width: 110px !important;
}

.el-descriptions__content {
  color: #333 !important;
}

.el-empty__description p {
  color: #999 !important;
}

.el-form-item__label {
  color: #555 !important;
  font-weight: 500 !important;
}

.el-card {
  border-radius: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.4) !important;
  background: rgba(255, 255, 255, 0.65) !important;
  backdrop-filter: blur(12px);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

html.dark-mode {
  background: #0f0f1a;
}

html.dark-mode body {
  background-color: rgba(0, 0, 0, 0.55) !important;
}

html.dark-mode #app {
  background: transparent;
}

html.dark-mode .el-card {
  background: rgba(30, 30, 50, 0.85) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: blur(16px);
}

html.dark-mode .el-dialog {
  background: rgba(25, 25, 45, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(24px);
}

html.dark-mode .el-dialog__title {
  color: #e8e8e8 !important;
}

html.dark-mode .el-dialog__header {
  border-bottom-color: rgba(255, 255, 255, 0.06) !important;
}

html.dark-mode .el-dialog__footer {
  border-top-color: rgba(255, 255, 255, 0.06) !important;
}

html.dark-mode .el-dialog__headerbtn .el-dialog__close {
  color: #888 !important;
}

html.dark-mode .el-dialog__headerbtn:hover .el-dialog__close {
  color: #fff !important;
}

html.dark-mode .el-descriptions__label {
  background: linear-gradient(135deg, rgba(40, 40, 65, 0.9), rgba(30, 30, 50, 0.9)) !important;
  color: #aaa !important;
}

html.dark-mode .el-descriptions__content {
  color: #e0e0e0 !important;
  background: rgba(20, 20, 35, 0.4) !important;
}

html.dark-mode .el-table th.el-table__cell {
  background: linear-gradient(135deg, rgba(40, 40, 65, 0.9), rgba(30, 30, 50, 0.9)) !important;
  color: #ccc !important;
  border-bottom-color: rgba(255, 255, 255, 0.06) !important;
}

html.dark-mode .el-table td.el-table__cell {
  border-bottom-color: rgba(255, 255, 255, 0.04) !important;
  color: #ccc !important;
  background: rgba(20, 20, 35, 0.3) !important;
}

html.dark-mode .el-table .el-table__row--striped td.el-table__cell {
  background: rgba(30, 30, 50, 0.4) !important;
}

html.dark-mode .el-table__body tr:hover > td {
  background: rgba(50, 50, 80, 0.3) !important;
}

html.dark-mode .el-input__wrapper {
  background: rgba(30, 30, 55, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255, 255, 255, 0.05) !important;
}

html.dark-mode .el-input__wrapper:hover {
  border-color: rgba(0, 136, 255, 0.3) !important;
}

html.dark-mode .el-input__inner {
  color: #e0e0e0 !important;
}

html.dark-mode .el-select .el-input__wrapper,
html.dark-mode .el-select .el-select__wrapper {
  background: rgba(30, 30, 55, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

html.dark-mode .el-form-item__label {
  color: #bbb !important;
}

html.dark-mode .el-tag--info {
  background: rgba(144, 147, 153, 0.2) !important;
  color: #aaa !important;
}

html.dark-mode .el-tag--success {
  background: rgba(103, 194, 58, 0.2) !important;
  color: #7ecf5a !important;
}

html.dark-mode .el-tag--danger {
  background: rgba(255, 77, 79, 0.2) !important;
  color: #ff6b6b !important;
}

html.dark-mode .el-tag--warning {
  background: rgba(250, 173, 20, 0.2) !important;
  color: #f5c542 !important;
}

html.dark-mode .el-empty__description p {
  color: #888 !important;
}

html.dark-mode .el-select-dropdown {
  background: rgba(25, 25, 50, 0.98) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
}

html.dark-mode .el-select-dropdown__item {
  color: #ccc !important;
}

html.dark-mode .el-select-dropdown__item.hover,
html.dark-mode .el-select-dropdown__item:hover {
  background: rgba(0, 136, 255, 0.15) !important;
  color: #66b5ff !important;
}

html.dark-mode .el-select-dropdown__item.is-selected {
  background: rgba(0, 136, 255, 0.3) !important;
  color: #fff !important;
}

html.dark-mode .search-form {
  background: rgba(20, 20, 40, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
  border-radius: 16px;
}

html.dark-mode .el-button--default {
  background: rgba(40, 40, 65, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #ccc !important;
}

html.dark-mode .el-button--default:hover {
  background: rgba(50, 50, 80, 0.9) !important;
  border-color: rgba(0, 136, 255, 0.3) !important;
}

html.dark-mode .el-form-item__label {
  color: #aaa !important;
}

html.dark-mode .el-rate__icon {
  color: #555 !important;
}

html.dark-mode .el-rate__icon.is-active {
  color: #f5a623 !important;
}

html.dark-mode .el-pagination {
  color: #bbb !important;
}

html.dark-mode .el-pagination button:disabled {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #555 !important;
}

html.dark-mode .el-pagination .el-pager li {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #bbb !important;
}

html.dark-mode .el-pagination .el-pager li.is-active {
  background: rgba(0, 136, 255, 0.3) !important;
  color: #66b5ff !important;
}

html.dark-mode .el-pagination .el-pagination__jump {
  color: #bbb !important;
}

html.dark-mode .el-pagination .el-pagination__jump .el-input__wrapper {
  background: rgba(30, 30, 55, 0.8) !important;
}

html.dark-mode .el-dropdown-menu {
  background: rgba(25, 25, 50, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

html.dark-mode .el-dropdown-menu__item {
  color: #ccc !important;
}

html.dark-mode .el-dropdown-menu__item:hover {
  background: rgba(0, 136, 255, 0.15) !important;
  color: #66b5ff !important;
}

html.dark-mode .el-dropdown-menu__item.is-divided {
  border-top-color: rgba(255, 255, 255, 0.08) !important;
}

html.dark-mode .el-menu {
  background: rgba(20, 20, 40, 0.6) !important;
}

html.dark-mode .el-menu-item {
  color: #bbb !important;
}

html.dark-mode .el-menu-item.is-active {
  color: #66b5ff !important;
}

html.dark-mode .el-menu-item:hover {
  background: rgba(0, 136, 255, 0.1) !important;
}

html.dark-mode .el-tabs__item {
  color: #bbb !important;
}

html.dark-mode .el-tabs__item.is-active {
  color: #66b5ff !important;
}

html.dark-mode .el-tabs__active-bar {
  background: #66b5ff !important;
}

html.dark-mode .card-header-tabs .el-tabs {
  background: rgba(0, 0, 0, 0.2) !important;
}

html.dark-mode .el-badge__content {
  background: #ff4757 !important;
}

html.dark-mode button.el-button--default {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #ccc !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

html.dark-mode button.el-button--default:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15) !important;
  color: #fff !important;
}

html.dark-mode button.el-button--primary {
  background: rgba(0, 136, 255, 0.6) !important;
}

html.dark-mode button.el-button--primary:hover:not(:disabled) {
  background: rgba(0, 136, 255, 0.8) !important;
}

html.dark-mode button.el-button--danger {
  background: rgba(255, 77, 79, 0.5) !important;
}

html.dark-mode button.el-button--danger:hover:not(:disabled) {
  background: rgba(255, 77, 79, 0.7) !important;
}

html.dark-mode .el-alert--info {
  background: rgba(0, 136, 255, 0.1) !important;
  color: #bbb !important;
}

html.dark-mode .icp-footer a {
  color: rgba(255, 255, 255, 0.2) !important;
}

html.dark-mode,
html.dark-mode *,
html.dark-mode *::before,
html.dark-mode *::after {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
}

.icp-footer {
  text-align: center;
  padding: 16px 0 12px;
  z-index: 9999;
}

.icp-footer a {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  text-decoration: none;
  transition: color 0.2s;
}

.icp-footer a:hover {
  color: rgba(255, 255, 255, 0.8);
}
</style>
