import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
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
