<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>用户管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px">
        <el-input placeholder="请输入账号或者密码查询" v-model="params.keywords" style="width: 240px;margin-right:5px;"
          @keyup.enter="handleSearch" clearable @clear="handleSearch"></el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button type="success" :icon="Plus" @click="handleCreate">新增</el-button>
      </div>
      <div style="margin-top: 10px;">
        <el-table :header-cell-style="{ 'backgroundColor': '#f5f7fa', color: '#333' }" :data="tableData"
          style="width: 100%;" v-loading="loading">
          <el-table-column prop="username" label="账号" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="avatar" label="头像">
            <template #default="{ row }">
              <div style="min-height: 50px;">
                <img v-if="row.avatar" style="display: block; width: 50px; height: 50px;border-radius: 50%;"
                  :src="row.avatar" alt="" />
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="phone" label="手机号" />
          <el-table-column prop="role" label="角色">
            <template #default="{ row }">
              {{ row.role === 'admin' ? '管理员' : '学生' }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                {{ row.status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160" header-align="center">
            <template #default="{ row }">
              <el-button type="primary" text bg @click="handleEdit(row)">编辑</el-button>
              <el-button type="danger" text bg @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
        <el-pagination v-model:current-page="params.page" v-model:page-size="params.pageSize" :total="total" background
          layout="total,prev, pager, next" @current-change="load" />
      </div>
    </el-card>
    <el-dialog v-model="dialogTableVisible" :title="form.id ? '编辑' : '新增'" width="450">

      <el-form ref="formRef" :rules="rules" :model="form" label-width="100px"
        style="width: 100%; padding-right: 30px;padding-top:16px" v-loading="loading">
        <el-form-item label="账号" prop="username">
          <!-- form.id 有值的时候就是disabled 也就是编辑的情形 -->
          <el-input :disabled="!!form.id" v-model="form.username" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" show-password v-model="form.password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role">
            <el-option label="学生" value="student"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">正常</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button>取消</el-button>
        <el-button type="primary" :loading="formLoading" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { createUserAPI, deleteUserAPI, getUserPageList, updateUserAPI } from '@/api/user';
import { ref, reactive, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus';
const params = reactive({
  page: 1,
  pageSize: 10,
  keywords: '',
})
const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const dialogTableVisible = ref(false)
const formRef = ref()
const form = reactive({
  username: '',
  name: '',
  role: 'student',
  email: '',
  phone: '',
  avatar: '',
  status: 1
})
const resetFrom = () => {
  Object.assign(form, {
    id: null,
    username: '',
    name: '',
    role: 'student',
    email: '',
    phone: '',
    avatar: '',
    status: 1
  })
}

const formLoading = ref(false)

const handleSave = async()=>{
  // 如果里面发生错误返回false，表示表单验证失败
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  formLoading.value = true
  try{
    const res = form.id ? await updateUserAPI(form.id,form):await createUserAPI(form)
    if (res.code === 200){
      dialogTableVisible.value = false
      ElMessage.success("操作成功")
      load()
    }
  } finally{
    formLoading.value=false
  }
}

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' },
  { min: 3, max: 10, message: '密码是3到10位' }
  ],
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式错误', trigger: 'blur' }],
  phone: [{ pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误', trigger: 'blur' }]
}

//打开表单
const handleCreate = () => {
  resetFrom()
  dialogTableVisible.value = true
}
//修改用户
const handleEdit = (row)=>{
  resetFrom()
  Object.assign(form, {
    id: row.id,
    username: row.username,
    name: row.name,
    role: row.role,
    email: row.email,
    phone: row.phone,
    avatar: row.avatar,
    status: row.status
  })
  dialogTableVisible.value=true
}

//删除用户信息
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除用户[${row.username}]?`,'确认删除',{type:'warning'}).then(async()=>{
    const res = await deleteUserAPI(row.id)
    if(res.code===200){
      ElMessage.success("删除用户成功")
      load()
    }
  })
}

//加载分页数据
const load = async () => {
  loading.value = true
  try {
    const res = await getUserPageList({
      page: params.page,
      page_size: params.pageSize,
      keywords: params.keywords
    })
    if (res.code === 200) {
      tableData.value = res.data?.list
      total.value = res.data?.total
    }
  } finally {
    loading.value = false
  }
}

//查询用户信息
const handleSearch = async () => {
  params.page = 1
  load()
}
onMounted(() => {
  load()
})
</script>