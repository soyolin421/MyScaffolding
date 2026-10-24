//auth.js 负责在浏览器的 localStorage 中管理登录状态
const TOKEN_KEY = 'token'
const USER_KEY = 'userInfo'

// 获取token
export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}
//存储token
export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}
//删除token
export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

// 获取user
export function getUserInfo() {
  const str = localStorage.getItem(USER_KEY)
  return str ? JSON.parse(str) : null
}
//存储token
//userinfo是个json要转成字符串
export function setUserInfo(userInfo) {
  localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
}
//删除token
export function removeUserInfo() {
  localStorage.removeItem(USER_KEY)
}

//登出函数
export function logout(){
  removeToken()
  removeUserInfo()
}
