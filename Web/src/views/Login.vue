<template>
  <div id="login-div">
    <div id="left">
      <div>
        <h2>OpenSD</h2>
      </div>
      <div>
        <h3>基于AIGC技术的图像综合处理系统</h3>
      </div>
    </div>
    <div id="right">
      <div id="login-box">
    <el-form
      :model="loginFormData"
      label-width="auto"
      style="width: 330px"
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
    </div>
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
#login-div{
  width: 100%;
  height: 100%;
  position: absolute;
}
#left{
  width: 60%;
  height: 100%;
  left: 0;
  position: absolute;
  background-color: var(--el-color-primary);
}
#left div{
  width: 100%;
  left: 50%;
  top: 35%;
  transform: translateX(-50%) translateY(-50%);
  position: relative;
  display: flex;
  justify-content: center;
}
#left h2{
  color: white;
  font-size: 50px;
  width: 65%;
  margin: 10px;
}
#left h3{
  color: white;
  font-size: 40px;
  width: 65%;
}
#right{
  width: 40%;
  height: 100%;
  right: 0;
  position: absolute;
}
#login-box {
  width: 420px;
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
  background-color: white;
}
</style>
