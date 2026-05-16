const lazyMap = new WeakMap()

const defaultSrc = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60"%3E%3Crect fill="%23f0f0f0" width="100" height="60"/%3E%3Ctext x="50" y="32" text-anchor="middle" fill="%23aaa" font-size="12"%3E加载中...%3C/text%3E%3C/svg%3E'

export default {
  mounted(el, binding) {
    const img = el.tagName === 'IMG' ? el : el.querySelector('img')
    if (!img) return

    const oldSrc = binding.value || img.getAttribute('data-src') || img.src
    img.src = defaultSrc
    img.setAttribute('data-src', oldSrc)

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const src = img.getAttribute('data-src')
          if (src) {
            img.src = src
            img.removeAttribute('data-src')
          }
          observer.unobserve(img)
        }
      })
    }, { rootMargin: '100px' })

    observer.observe(img)
    lazyMap.set(el, observer)
  },
  beforeUnmount(el) {
    const observer = lazyMap.get(el)
    if (observer) {
      observer.disconnect()
      lazyMap.delete(el)
    }
  }
}
