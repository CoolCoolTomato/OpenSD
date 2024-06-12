<script setup>
import {Picture as IconPicture} from '@element-plus/icons-vue'
</script>

<template>
  <el-row :gutter="30" style="margin-bottom: 20px">
    <el-col :span="16" style="display:flex;">
      <label class="el-form-item__label" style="width: 170px; text-align: right">选择模型</label>
      <el-select v-model="model" placeholder="模型" size="large" v-loading="isSwitchModel">
        <el-option
          v-for="model in models"
          :key="model.title"
          :label="model.title"
          :value="model.title">
        </el-option>
      </el-select>
      <el-button size="large" @click="SetConfig" style="margin-left: 15px">确认</el-button>
    </el-col>
    <el-col :span="8">
      <el-button size="large" type="primary" @click="ExtraImage">生成</el-button>
    </el-col>
  </el-row>
  <el-row :gutter="30">
    <el-col :span="16">
      <el-form :model="enhanceData">
        <el-form-item label="初始图像" :label-width="formLabelWidth">
          <el-upload
            action=""
            list-type="picture"
            :auto-upload="false"
            :file-list="fileList"
            @change="handleFileChange">
            <el-button size="large" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="Upscaler1" :label-width="formLabelWidth">
          <el-select
            v-model="enhanceData.upscaler_1"
          >
            <el-option
              v-for="upscaler in upscalers"
              :key="upscaler"
              :label="upscaler.name"
              :value="upscaler.name"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Upscaler2" :label-width="formLabelWidth">
          <el-select
            v-model="enhanceData.upscaler_2"
          >
            <el-option
              v-for="upscaler in upscalers"
              :key="upscaler"
              :label="upscaler.name"
              :value="upscaler.name"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Upscaler2可见度" :label-width="formLabelWidth">
          <el-slider v-model="enhanceData.extras_upscaler_2_visibility" :min="0" :max="1" step="0.001" show-input></el-slider>
        </el-form-item>
        <el-form-item>
          <el-tabs style="width: 100%; margin-left: 170px;" v-model="sizemod">
            <el-tab-pane label="等比缩放" name="scaleTo">
              <el-form-item label="启用">
                <el-switch v-model="mod0"/>
              </el-form-item>
              <el-form-item label="缩放比例">
                <el-slider v-model="enhanceData.upscaling_resize" :min="1" :max="8" step="0.1" show-input></el-slider>
              </el-form-item>
            </el-tab-pane>
            <el-tab-pane label="指定分辨率" name="scaleBy">
              <el-form-item label="启用">
                <el-switch v-model="mod1"/>
              </el-form-item>
              <el-form-item label="宽度">
                <el-slider v-model="enhanceData.upscaling_resize_w" :min="64" :max="8192" step="1" show-input></el-slider>
              </el-form-item>
              <el-form-item label="高度">
                <el-slider v-model="enhanceData.upscaling_resize_h" :min="64" :max="8192" step="1" show-input></el-slider>
              </el-form-item>
              <el-form-item label="裁剪以适应宽高比">
                <el-switch v-model="enhanceData.upscaling_crop" />
              </el-form-item>
            </el-tab-pane>
          </el-tabs>
        </el-form-item>
        <el-form-item label="GFPGAN" :label-width="formLabelWidth">
          <el-slider v-model="enhanceData.gfpgan_visibility" :min="0" :max="1" step="0.001" show-input></el-slider>
        </el-form-item>
        <el-form-item label="CodeFormer" :label-width="formLabelWidth">
          <div style="width: 100%">
              <el-form-item label="可见性" label-width="100px">
                <el-slider v-model="enhanceData.codeformer_visibility" :min="0" :max="1" step="0.001" show-input></el-slider>
              </el-form-item>
              <el-form-item label="权重" label-width="100px">
                <el-slider v-model="enhanceData.codeformer_weight" :min="0" :max="1" step="0.001" show-input></el-slider>
              </el-form-item>
          </div>
        </el-form-item>

      </el-form>
    </el-col>
    <el-col :span="8">
      <div style="height: 600px;">
        <el-scrollbar>
          <div v-if="imgs.length > 0"
              v-for="img in imgs"
              :key="img"
              v-loading="isLoadingImg"
               style="width: 99%">
            <div class="block">
              <el-image :src="img" fit="contain">
                <template #error>
                  <div class="image-slot">
                    <el-icon><icon-picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
          <div v-else v-loading="isLoadingImg" style="width: 99%">
              <el-image fit="contain">
                <template #error>
                  <div class="image-slot">
                    <el-icon><icon-picture /></el-icon>
                  </div>
                </template>
              </el-image>
          </div>
        </el-scrollbar>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import {extraImage, get_config, get_models, get_samplers, set_config, get_upscalers} from "@/api/sd.js";
import { ElMessage } from "element-plus";
import Config from "@/config/config.js";

export default {
  data() {
    return {
      sizemod: "scaleTo",
      formLabelWidth: '170px',
      model: "",
      models: [],
      upscalers: [],
      enhanceData: {
        "image": "",
        "resize_mode": 0,

        "gfpgan_visibility": 0,
        "codeformer_visibility": 0,
        "codeformer_weight": 0,

        "upscaling_resize": 2,
        "upscaling_resize_w": 512,
        "upscaling_resize_h": 512,
        "upscaling_crop": true,

        "upscaler_1": "None",
        "upscaler_2": "None",
        "extras_upscaler_2_visibility": 0,
        "upscale_first": false
      },
      imgs: [],
      isLoadingImg: false,
      isSwitchModel: false,
      fileList: []
    }
  },
  methods: {
    async GetModels() {
      try {
        this.models = await get_models()
      } catch (error) {
        ElMessage.error('获取模型失败')
        console.log(error)
      }
    },
    async GetConfig() {
      try {
        this.config = await get_config()
        this.model = this.config.sd_model_checkpoint
      } catch (error) {
        ElMessage.error('获取配置失败')
        console.log(error)
      }
    },
    async GetUpscalers() {
      try {
        this.upscalers = await get_upscalers()
      } catch (error) {
        ElMessage.error('获取采样器失败')
        console.log(error)
      }
    },
    async SetConfig() {
      try {
        this.isSwitchModel = true
        await set_config({ "sd_model_checkpoint": this.model })
        this.GetConfig()
        this.isSwitchModel = false
        ElMessage({
          message: '切换模型成功',
          type: 'success',
        })
      } catch (error) {
        ElMessage.error('更改配置失败')
        console.log(error)
      }
    },
    async ExtraImage() {
      try {
        this.isLoadingImg = true
        const response = await extraImage(this.enhanceData)
        this.imgs = response.map(img => `${Config.baseURL}:${img}`)
        this.isLoadingImg = false
      } catch (error) {
        console.log(error)
        this.isLoadingImg = false
        if (error.response.data.error === "Insufficient points") {
          ElMessage.error('点数不足')
        } else if (error.response.data.error === "Image is required"){
          ElMessage.error('未上传图片')
        } else {
          ElMessage.error('图片高清化失败')
        }
        console.log(error)
      }
    },
    handleFileChange(file, fileList) {
      const reader = new FileReader()
      reader.readAsDataURL(file.raw)
      reader.onload = () => {
        file.url = reader.result
        this.enhanceData.image = reader.result.split(',')[1] // 去掉base64头部
      }
      this.fileList = fileList
    }
  },
  computed: {
    mod0: {
      get() {
        return this.enhanceData.resize_mode === 0;
      },
      set(value) {
        if (value){
          this.enhanceData.resize_mode = 0
        } else {
          this.enhanceData.resize_mode = 1
        }
      }
    },
    mod1: {
      get() {
        return this.enhanceData.resize_mode === 1;
      },
      set(value) {
        if (value){
          this.enhanceData.resize_mode = 1
        } else {
          this.enhanceData.resize_mode = 0
        }
      }
    }
  },
  mounted() {
    this.GetConfig()
    this.GetModels()
    this.GetUpscalers()
  }
}
</script>

<style scoped>
.block {
  padding: 30px 0;
  display: inline-block;
  width: 99%;
  box-sizing: border-box;
  vertical-align: top;
}
.el-image {
  width: 99%;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 30px;
}
.image-slot .el-icon {
  font-size: 30px;
}
</style>
