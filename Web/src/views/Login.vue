<template>
  <div id="login-box">
    <el-form
      :model="loginFormData"
      label-width="auto"
      style="width: 350px"
    >
      <el-form-item>
        <h2 style="color: var(--el-text-color-regular);width: 100%;text-align: center">用户登录</h2>
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="loginFormData.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="loginFormData.password" type="password"></el-input>
      </el-form-item>
      <el-form-item>
        <div style="flex-grow: 1"></div>
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

        if (access !== "" && refresh !== "") {
          localStorage.setItem('access_token', access);
          localStorage.setItem('refresh_token', refresh);

          ElMessage.success('登录成功');
          this.$router.push('/index')
        } else {
          ElMessage.error('用户名或密码错误');
        }
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
  width: 450px;
  height: 300px;
  left: 50%;
  top: 50%;
  transform: translateX(-50%) translateY(-50%);
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 10px #808080;
  border-radius: 10px;
}
</style>
