import { createApp } from 'vue'
import naive from 'naive-ui'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
app.use(router)
app.use(naive)
app.mount('#app')

const _ResizeObserver = window.ResizeObserver
window.ResizeObserver = function (callback) {
  const safeCallback = function (entries, obs) {
    window.requestAnimationFrame(() => {
      if (!Array.isArray(entries) || !entries.length) return
      try {
        callback(entries, obs)
      } catch (e) {
        if (!(e instanceof Error) || !e.message.includes('ResizeObserver loop')) {
          console.error(e)
        }
      }
    })
  }
  return new _ResizeObserver(safeCallback)
}
window.ResizeObserver.prototype = _ResizeObserver.prototype
