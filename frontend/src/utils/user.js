//仅供页面 setup函数使用
//“前端的登录状态管理
import { getUserInfo, setToken, setUserInfo } from './auth'
import { ref } from 'vue'

//用 ref 保存响应式用户信息
const userInfo = ref(getUserInfo()) //响应式的对象，可以随时更新最新的值

//hook
export function useUser() {
  //saveLoginData()
  //保存后端的数据
  function saveLoginData(data) {
    setToken(data.token)
    setUserInfo(data.user)
    userInfo.value = data.user
  }

  //更新用户信息
  function updateUser(user) {
    setUserInfo(user)
    userInfo.value = user
  }

  //从 localStorage 重新读取
  function reloadUser() {
    userInfo.value = getUserInfo()
  }

  return {
    userInfo,
    saveLoginData,
    updateUser,
    reloadUser
  }
}
