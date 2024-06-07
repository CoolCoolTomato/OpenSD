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
      <el-button size="large" type="primary" @click="Img2Img">生成</el-button>
    </el-col>
  </el-row>
  <el-row :gutter="30">
    <el-col :span="16">
      <el-form :model="img2ImgData">
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
        <el-form-item label="提示词" :label-width="formLabelWidth">
          <el-input v-model="img2ImgData.prompt" type="textarea" placeholder="提示词"></el-input>
        </el-form-item>
        <el-form-item label="负向提示词" :label-width="formLabelWidth">
          <el-input v-model="img2ImgData.negative_prompt" type="textarea" placeholder="负向提示词"></el-input>
        </el-form-item>
        <el-form-item label="采样器" :label-width="formLabelWidth">
          <el-select v-model="img2ImgData.sampler_name" placeholder="采样器">
            <el-option
              v-for="sampler in samplers"
              :key="sampler"
              :label="sampler.name"
              :value="sampler.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="调度类型" :label-width="formLabelWidth">
          <el-select v-model="img2ImgData.scheduler" placeholder="调度类型">
            <el-option
              v-for="scheduler in schedulers"
              :key="scheduler"
              :label="scheduler.name"
              :value="scheduler.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="采样步数" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.steps" :min="1" :max="150" show-input></el-slider>
        </el-form-item>
        <el-form-item label="图片宽度" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.width" :min="64" :max="2048" show-input></el-slider>
        </el-form-item>
        <el-form-item label="图片高度" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.height" :min="64" :max="2048" show-input></el-slider>
        </el-form-item>
        <el-form-item label="生成次数" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.batch_size" :min="1" :max="10" show-input></el-slider>
        </el-form-item>
        <el-form-item label="提示词引导系数" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.cfg_scale" :min="1" :max="30" show-input></el-slider>
        </el-form-item>
        <el-form-item label="图像生成种子" :label-width="formLabelWidth">
          <div style="display:flex;width: 100%;">
            <el-input v-model="img2ImgData.seed" placeholder="图像生成种子" size="large"></el-input>
            <el-button @click="getStableDiffusionSeed" size="large" style="margin-left: 15px">
              <el-icon style="vertical-align: middle">
                <RefreshRight />
              </el-icon>
            </el-button>
            <el-button @click="setSeedDefault" size="large">
              <el-icon style="vertical-align: middle">
                <CircleClose />
              </el-icon>
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="重绘强度" :label-width="formLabelWidth">
          <el-slider v-model="img2ImgData.denoising_strength" :min="0" :max="1" step="0.01" show-input></el-slider>
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
               style="width: 99%"
            >
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
import { get_models, get_config, set_config, get_schedulers, get_samplers, img2img } from "@/api/sd.js";
import { ElMessage } from "element-plus";
import Config from "@/config/config.js";
import { RefreshRight, CircleClose } from "@element-plus/icons-vue";

export default {
  components: {
    RefreshRight,
    CircleClose,
  },
  data() {
    return {
      formLabelWidth: '170px',
      config: {},
      model: "",
      models: [],
      samplers: [],
      schedulers: [],
      img2ImgData: {
        "init_images": [],
        "prompt": "",
        "negative_prompt": "",
        "sampler_name": "DPM++ 2M",
        "scheduler": "Automatic",
        "steps": 20,
        "width": 512,
        "height": 512,
        "batch_size": 1,
        "cfg_scale": 7,
        "seed": -1,
        "denoising_strength": 0.75
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
    async GetSchedulers() {
      try {
        this.schedulers = await get_schedulers()
      } catch (error) {
        ElMessage.error('获取调度类型失败')
        console.log(error)
      }
    },
    async GetSamplers() {
      try {
        this.samplers = await get_samplers()
      } catch (error) {
        ElMessage.error('获取采样器失败')
        console.log(error)
      }
    },
    async Img2Img() {
      try {
        this.isLoadingImg = true
        const init_images = this.fileList.map(file => file.url)
        this.img2ImgData.init_images = init_images
        const response = await img2img(this.img2ImgData)
        this.imgs = response.map(img => `${Config.baseURL}:${img}`)
        this.isLoadingImg = false
      } catch (error) {
        this.isLoadingImg = false
        if (error.response.data.error === "Insufficient points") {
          ElMessage.error('点数不足')
        } else if (error.response.data.error === "Initial images are required"){
          ElMessage.error('未上传图片')
        } else {
          ElMessage.error('图片生成失败')
        }
        console.log(error)
      }
    },
    handleFileChange(file, fileList) {
      const reader = new FileReader()
      reader.readAsDataURL(file.raw)
      reader.onload = () => {
        file.url = reader.result
      }
      this.fileList = fileList
    },
    getStableDiffusionSeed() {
      const timestamp = Date.now()
      const random = Math.floor(Math.random() * Math.pow(2, 32))
      const seedStr = timestamp.toString() + random.toString()
      const seedNum = parseInt(seedStr, 10)
      const seed = seedNum % Math.pow(2, 32)
      this.img2ImgData.seed = seed
    },
    setSeedDefault() {
      this.img2ImgData.seed = -1
    }
  },
  mounted() {
    this.GetConfig()
    this.GetModels()
    this.GetSchedulers()
    this.GetSamplers()
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
.demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
  text-align: center;
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
