<!-- 个人主页 -->

<template>
  <div style="width: 50%">
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>个人信息</span>
        </div>
      </template>
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        label-width="100px"
        style="width: 80%; padding-right: 100px"
        v-loading="loading"
      >
        <el-form-item label="账号" >
          <el-input disabled v-model="form.username" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="角色">
          <el-input disabled v-model="roleLabel" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item >
          <el-button type="primary":loading="submitting" @click="handleSubmit">保存修改</el-button>
        </el-form-item>
        
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { getUserInfo, updateUserInfo } from '@/api/user'
import { ref, reactive, onMounted,computed} from 'vue'
import { ElMessage } from 'element-plus'
import { useUser } from '@/utils/user'

const { updateUser } = useUser()

const loading = ref(false)
const submitting = ref(false)

const form = reactive({
  username: '',
  name: '',
  role: '',
  email: '',
  phone: '',
  avatar: ''
})

const formRef = ref()

const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式错误', trigger: 'blur' }],
  phone: [{ pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误', trigger: 'blur' }]
}

const roleLabel = computed(()=>{
  return form.role === 'admin'?'管理员':form.role ==='student'?'学生':'未知角色'
})

// 将res中的数据逐个赋值给form
const loadUserInfo = async () => {
  loading.value = true
  try {
    const res = await getUserInfo()
    if (res.code === 200) {
      Object.assign(form, res.data)
    }
  } finally {
    loading.value = false
  }
}

//发送请求跟新用户信息
const handleSubmit = async ()=>{
  // 如果里面发生错误返回false，表示表单验证失败
  const valid = await formRef.value.validate().catch(()=>false)
  if(!valid) return
  submitting.value=true
  try{
    const res = await updateUserInfo(form)
    if(res.code === 200){
      updateUser(res.data)
      ElMessage.success('更新成功')
    }
  }finally{
    submitting.value=false
  }
}

onMounted(()=>{
  loadUserInfo()
  })
</script>

<style scoped></style>
