<template>
<div class="common-layout" id="main">
    <el-container>
    <el-header>
      <el-menu
        mode="horizontal"
        :ellipsis="false"
        router
        >
        <el-menu-item >
          <h2 style="color: var(--el-text-color-primary);">OpenSD</h2>
        </el-menu-item>
        <div class="flex-grow" />
        <el-menu-item index="/index">
          <el-text class="mx-1" size="large"></el-text>
        </el-menu-item>
        <el-menu-item index="/text2img">
          <el-text class="mx-1" size="large">文生图</el-text>
        </el-menu-item>
        <el-menu-item index="/images">
          <el-text class="mx-1" size="large">图库</el-text>
        </el-menu-item>
        <el-menu-item>
          <el-dropdown :hide-on-click="false" @command="handleCommand" @visible-change="GetUser">
            <span class="el-dropdown-link">用户</span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>当前用户：{{ user.username }}</el-dropdown-item>
                <el-dropdown-item>剩余点数：{{ user.points }}</el-dropdown-item>
                <el-dropdown-item command="logout">注销</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <RouterView />
    </el-main>
    <el-footer>
      <el-text size="small">Powered By liuqiukai</el-text>
    </el-footer>
  </el-container>
  </div>
</template>
<script>
import {getuser, logout} from "@/api/user.js";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      user: {},
    }
  },
  methods: {
    async GetUser() {
      try{
        this.user = await getuser()
      } catch (error) {
        ElMessage.error('获取当前用户失败')
        console.log(error)
      }
    },
    async Logout() {
      try {
        await logout({
          "refresh_token": localStorage.getItem('refresh_token')
        })
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.$router.push("/login")
      } catch (error) {
        ElMessage.error('注销失败')
        console.log(error)
      }
    },
    handleCommand(command) {
      if (command === 'logout') {
        this.Logout();
      }
    },
  },
  mounted() {
    this.GetUser()
  }
}
</script>
<style scoped>
#main{
  width: 100%;
  height: 100%;
  position: absolute;
}
.el-container{
  width: 100%;
  height: 100%;
}
.flex-grow {
  flex-grow: 1;
}
.el-footer{
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
<script setup>
</script>