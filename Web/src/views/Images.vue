<script setup>
  import {Picture as IconPicture} from '@element-plus/icons-vue'
</script>
<template>
  <div style="height: 100%; width: 100%">
    <el-scrollbar>
      <div class="image-masonry">
        <div v-for="img in imgs" :key="img" class="image-wrapper">
          <el-image
            :src="img"
            fit="cover"
            v-loading="isLoadingImg"
            loading-text="Loading..."
          >
            <template #error>
              <div class="image-slot">
                <el-icon>
                  <icon-picture />
                </el-icon>
                <span>Failed to load</span>
              </div>
            </template>
          </el-image>
        </div>
      </div>
    </el-scrollbar>
  </div>
</template>
<script>
import {get_config, images, text2img} from "@/api/sd.js";
import {ElMessage} from "element-plus";
import Config from "@/config/config.js";

export default {
  data(){
    return {
      imgs: [],
    }
  },
  methods: {
    async GetImgs(){
      try {
        this.imgs = (await images()).map(img => `${Config.baseURL}:${img}`)
      } catch (error) {
        ElMessage.error('获取图片失败')
        console.log(error)
      }
    }
  },
  mounted() {
    this.GetImgs()
    console.log(this.imgs)
  }
}
</script>
<style scoped>
.image-masonry {
  column-count: 6;
  column-gap: 20px;
}

.image-wrapper {
  break-inside: avoid;
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;

  .el-image {
    width: 100%;
    height: auto;
    display: block;
  }

  .image-slot {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    background-color: #f5f7fa;
    color: #909399;
    font-size: 14px;

    .el-icon {
      font-size: 28px;
      margin-bottom: 10px;
    }
  }
}

</style>