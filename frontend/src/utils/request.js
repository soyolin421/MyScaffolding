import axios from 'axios'
import { getToken, logout } from './auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000 //三十秒
})

//请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (err) => Promise.reject(err)
)

//响应拦截器
service.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data.code !== 200) {
      ElMessage.error(data.message || '请求失败')
      // 没有权限错误
      if (data.code === 401) {
        logout()
        router.push('/login')
        return Promise.reject(data)
      }
    }
    return data
  },
  (err) => {
    if (err.response) {
      const httpStatusCode = err.response.state
      // 没有权限错误
      if (httpStatusCode === 401) {
        ElMessage.error('登录状态已经失效，请重新登录')
        logout()
        router.push('/login')
        return Promise.reject(data)
      } else {
        ElMessage.error(err.response.data?.message || '请求失败')
      }
    } else {
      //后端没启动，网络异常
      ElMessage.error('网络异常，请稍后再试')
    }
    return Promise.reject(err)
  }
)

export default service
