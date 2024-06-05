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