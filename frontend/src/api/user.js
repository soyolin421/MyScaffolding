import request from '@/utils/request'

/**
 * 获取当前登录用户
 */
export function getUserInfo(){
  return request({
    url:'/api/user/me',
    method:'get',
  })
}


/**
 * 修改当前用户的个人信息接口
 */
export function updateUserInfo(data){
  return request({
    url:'/api/user/me',
    method:'put',
    data
  })
}

/**
 * 修改当前用户的个人密码
 */
export function updatePassword(data){
  return request({
    url:'/api/user/password',
    method:'put',
    data
  })
}

/**
 * 获取用户列表
 */
export function getUserPageList(params){
  return request({
    url:'/api/user/list',
    method:'get',
    params
  })
}


/**
 * 获取新增用户
 */
export function createUserAPI(data){
  return request({
    url:'/api/user',
    method:'post',
    data
  })
}

/**
 * 获取更新修改用户
 */
export function updateUserAPI(userId ,data){
  return request({
    url:`/api/user/${userId}`,
    method:'put',
    data
  })
}

/**
 * 获取删除修改用户
 */
export function deleteUserAPI(userId){
  return request({
    url:`/api/user/${userId}`,
    method:'delete',
  })
}



