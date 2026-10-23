<template>
  <div class="register-container">
    <div class="register-box">
      <h1 style="font-size: 30px;margin-bottom: 30px;">欢迎注册</h1>

      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item>
          <el-input
            size="large"
            v-model="form.username"
            placeholder="请输入账号"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            type="password"
            size="large"
            v-model="form.password"
            placeholder="请输入密码"
            :prefix-icon="lock"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-input
            type="password"
            size="large"
            v-model="form.confirmPassword"
            placeholder="请确认输入的密码"
            :prefix-icon="lock"
            show-password
          />
        </el-form-item>
        <div>
          <el-button size="large" type="primary" style="width: 100%" @click="register">注 册</el-button>
          <div style="text-align: right; margin-top: 20px">
            已有账号？请<a href="/login" style="margin-left: 3px; color: var(--el-color-primary)">登录</a>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import router from '@/router'

const form = reactive({
  username: '',
  password: '',
  confirmPassword:''
})

const register = ()=>{
  setTimeout(()=>{
    ElMessage.success('注册成功')
    router.push('/login')
  },2000)
}

</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.register-box {
  width: 380px;
  border-radius: 8px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
  text-align: center;
  background-color: white;
}
</style>
