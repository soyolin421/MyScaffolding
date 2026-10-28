import request from '@/utils/request'


/**
 * 获取列表
 */
export function getLabPageList(params) {
  return request({
    url: '/api/lab/list',
    method: 'get',
    params
  })
}

/**
 * 获取
 */
export function createLabAPI(data) {
  return request({
    url: '/api/lab',
    method: 'post',
    data
  })
}

/**
 * 获取更新修改
 */
export function updateLabAPI(labId, data) {
  return request({
    url: `/api/lab/${labId}`,
    method: 'put',
    data
  })
}

/**
 * 获取删除修改
 */
export function deleteLabAPI(labId) {
  return request({
    url: `/api/lab/${labId}`,
    method: 'delete'
  })
}
