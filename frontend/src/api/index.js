import axios from 'axios'

// 缓存对象
const cache = new Map()
// 缓存过期时间（毫秒）
const CACHE_EXPIRY = 5 * 60 * 1000 // 5分钟

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 生成缓存键
const generateCacheKey = (url, params) => {
  return `${url}_${JSON.stringify(params || {})}`
}

// 检查缓存是否有效
const isCacheValid = (cacheItem) => {
  if (!cacheItem) return false
  return Date.now() - cacheItem.timestamp < CACHE_EXPIRY
}

request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

request.interceptors.response.use(
  response => {
    // 缓存GET请求的响应
    if (response.config.method === 'get') {
      const cacheKey = generateCacheKey(response.config.url, response.config.params)
      cache.set(cacheKey, {
        data: response.data,
        timestamp: Date.now()
      })
    }
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 清除缓存的方法
export const clearCache = (url) => {
  if (url) {
    // 清除指定URL的缓存
    for (const key of cache.keys()) {
      if (key.startsWith(url)) {
        cache.delete(key)
      }
    }
  } else {
    // 清除所有缓存
    cache.clear()
  }
}

// 获取缓存数据
export const getCache = (url, params) => {
  const cacheKey = generateCacheKey(url, params)
  const cacheItem = cache.get(cacheKey)
  if (isCacheValid(cacheItem)) {
    return cacheItem.data
  }
  return null
}

export default request
