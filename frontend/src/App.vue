<template>
  <n-config-provider :theme="naiveTheme" :theme-overrides="themeOverrides" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <div id="app">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
            <div class="icp-footer">
              <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">
                鲁ICP备2026021969号
              </a>
            </div>
          </div>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script>
import { computed } from 'vue'
import { zhCN, dateZhCN } from 'naive-ui'
import { themeOverrides, darkThemeOverrides } from './theme'

export default {
  name: 'App',
  setup() {
    const isDark = computed(() => document.documentElement.classList.contains('dark-mode'))

    const loadTheme = () => {
      const dark = localStorage.getItem('darkMode') === 'true'
      if (dark) {
        document.documentElement.classList.add('dark-mode')
      } else {
        document.documentElement.classList.remove('dark-mode')
      }
    }

    loadTheme()

    return {
      zhCN,
      dateZhCN,
      naiveTheme: computed(() => isDark.value ? darkThemeOverrides : null),
      themeOverrides: computed(() => isDark.value ? darkThemeOverrides : themeOverrides)
    }
  },
  mounted() {
    document.body.style.cssText = `
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      background-color: #f5f7fa;
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
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

.icp-footer {
  text-align: center;
  padding: 16px 0 12px;
  z-index: 9999;
}

.icp-footer a {
  color: rgba(0, 0, 0, 0.25);
  font-size: 12px;
  text-decoration: none;
  transition: color 0.2s;
}

.icp-footer a:hover {
  color: rgba(0, 0, 0, 0.45);
}

html.dark-mode .icp-footer a {
  color: rgba(255, 255, 255, 0.2);
}

html.dark-mode .icp-footer a:hover {
  color: rgba(255, 255, 255, 0.4);
}

@media screen and (max-width: 768px) {
  body {
    padding: 0;
    overflow-x: hidden;
  }
}
</style>
