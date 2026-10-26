import request from '@/utils/request'

/**
 * 获取当前登录用户
 */
export function getUserInfo(){
  return request({
    url:'/api/user/info',
    method:'get',
  })
}


/**
 * 修改当前用户的个人信息接口
 */
export function updateUserInfo(data){
  return request({
    url:'/api/user/update',
    method:'put',
    data
  })
}

