import axios from 'axios'
import {
  Message
} from 'element-ui'

const service = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 30000
})

service.interceptors.request.use(
  config => {
    if (config.method === 'post') {
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
      const params = new URLSearchParams()
      for (const item in config.data) {
        params.append(item, config.data['' + item + ''])
      }
      config.data = params
    }
    return config
  },
  error => {
    Message.error({
      message: '发送失败' + error,
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code % 1000 !== 0) {
      Message({
        message: res.message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    return response.data
  },
  (error) => {
    console.log(error)
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
