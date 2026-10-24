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