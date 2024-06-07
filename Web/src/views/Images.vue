<script setup>
  import {Picture as IconPicture} from '@element-plus/icons-vue'
</script>
<template>
  <div style="height: 100%; width: 100%">
    <el-scrollbar>
      <div class="image-masonry">
        <div v-for="img in imgs" :key="img" class="image-wrapper">
          <el-image
            :src="img.url"
            fit="cover"
            v-loading="isLoadingImg"
            loading-text="Loading..."
            @contextmenu.prevent="openImgForm($event, img.id, img.url)"
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
    <div
      v-if="deleteImgForm"
      :style="{ top: formPosition.top + 'px', left: formPosition.left + 'px' , width: '100px'}"
      class="context-menu"
    >
      <el-button
        @click="openImg"
        type="primary"
        text
        bg
        style="width: 100%; margin: 0; padding: 0;"
      >
        查看
      </el-button>
      <el-button
        @click="deleteImg"
        type="primary"
        text
        bg
        style="width: 100%; margin: 0; padding: 0;"
      >
      删除
    </el-button>
    </div>
    <el-dialog
      v-model="imgShow"
      @close="closeImgShowForm"
      style="max-width: 850px; max-height: 700px;padding: 20px"
    >
      <el-scrollbar>
        <div
          style="max-width: 800px; max-height: 640px; position: relative;"
        >
          <el-image :src="imgShowData.image_url" style="width: 100%" />
      </div>
      </el-scrollbar>
    </el-dialog>
  </div>
</template>
<script>
import {deleteImages, get_config, images, text2img} from "@/api/sd.js";
import {ElMessage} from "element-plus";
import Config from "@/config/config.js";


export default {
  data(){
    return {
      imgs: [],
      imgShow: false,
      imgShowData: {
        "image_url": 0,
      },
      deleteImgData: {
        "image_id": 0,
      },
      deleteImgForm: false,
      formPosition: {
        "top": 0,
        "let": 0,
      },
    }
  },
  methods: {
    async GetImgs() {
      try {
        const response = await images();
        this.imgs = response.map(img => ({
          id: img.id,
          url: `${Config.baseURL}:${img.url}`
        }));
      } catch (error) {
        ElMessage.error('获取图片失败');
        console.log(error);
      }
    },
    openImg() {
      this.imgShow = true
      this.closeDeleteImgForm()
    },
    openImgForm(event, image_id, image_url) {
      this.deleteImgForm = true
      this.formPosition.top = event.clientY
      this.formPosition.left = event.clientX
      this.deleteImgData.image_id = image_id
      this.imgShowData.image_url = image_url
    },
    closeDeleteImgForm(){
      this.deleteImgForm = false
      this.deleteImgData = {
        "image_id": 0,
      }
    },
    closeImgShowForm(){
      this.imgShow = false
      this.imgShowData = {
        "image_url": 0,
      }
    },
    async deleteImg(){
      try {
        let res = await deleteImages(this.deleteImgData)
        this.GetImgs()
        ElMessage({
          message: '删除成功',
          type: 'success',
        })
        this.closeDeleteImgForm()
      } catch (error) {
        ElMessage.error('删除失败')
        console.log(error)
      }
    }
  },
  mounted() {
    this.GetImgs()
    document.addEventListener('click', this.closeDeleteImgForm);
  }
}
</script>
<style scoped>
.image-masonry {
  column-count: 5;
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
.context-menu {
  position: fixed;
  z-index: 100;
}
</style>