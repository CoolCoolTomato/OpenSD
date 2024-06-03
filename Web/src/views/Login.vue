<template>
  <div id="login-box">
    <el-form
      :model="loginFormData"
      label-width="auto"
      style="width: 500px"
    >
      <el-form-item>
        <h2 style="color: var(--el-text-color-regular);">用户登录</h2>
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="loginFormData.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="loginFormData.password" type="password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="large" @click="SubmitLoginForm">登录</el-button>
        <el-button size="large">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { login } from "@/api/user.js";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      loginFormData: {
        username: "",
        password: "",
      },
    }
  },
  methods: {
    async SubmitLoginForm() {
      try {
        const res = await login(this.loginFormData);
        const { access, refresh } = res;

        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);

        ElMessage.success('登录成功');
        this.$router.push('/index')

      } catch (error) {
        ElMessage.error('用户名或密码错误');
        console.log(error);
      }
    }
  }
}
</script>

<style scoped>
#login-box {
  width: 100%;
  height: 100%;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
