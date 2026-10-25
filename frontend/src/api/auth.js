import request from "@/utils/request"


/**
 * 登陆请求
 * @param {*} data 
 * @returns 
 */
export function loginApi(data){
  return request({
    url:'/api/auth/login',
    method:'post',
    data
  })
}

/**
 * 注册请求
 * @param {*} data 
 * @returns 
 */
export function registerApi(data){
  return request({
    url:'/api/auth/register',
    method:'post',
    data
  })
}