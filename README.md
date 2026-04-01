# Stable Diffusion WebUI Forge - Neo (中文改良版)


## 项目介绍

本项目是基于 **Stable Diffusion WebUI Forge Neo** 的中文改良版本，专注于优化和多模态插件融合，目标是通过简单易用的 GUI 运行最新的流行模型。

**原作者**：[Haoming02](https://github.com/Haoming02)  
**原项目链接**：[https://github.com/Haoming02/sd-webui-forge-classic/tree/neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo?tab=readme-ov-file#installation)
qq群内领取开源整合包
<img width="357" height="587" alt="QQ20260329-165103" src="https://github.com/user-attachments/assets/1d75d3f0-c31b-4dd7-828b-b5377cede2e5" />



教程视频：https://www.bilibili.com/video/BV1KfXyBTEXb?vd_source=343e49b703fb5b4137cd6c1987846f37&spm_id_from=333.788.videopod.sections

> [!说明]
> 本版本为改良版本，部分插件直接安装会发生兼容性错误，为了适应众多新旧插件做了些许修改。

### Forge 是什么？

Stable Diffusion WebUI Forge 是建立在原始 AUTOMATIC1111 Stable Diffusion WebUI 之上的平台，旨在：
- 简化开发流程。优化资源管理
- 加速推理，所有项目与插件最高均不超过16gb显存，以12gb-8gb居多
- 配置要求从高到低依次是 wan2.2，Qwen-Image，flux2-Klein，flux，qwen3-tts，Anima，XL


名称 "Forge" 的灵感来自 "Minecraft Forge"。该项目旨在成为 Stable Diffusion WebUI 的 "Forge"。

---

## 插件列表

### 新增插件

| 插件名称 | 功能说明 |
|---------|---------|
| **� 美学提升sd-webui-AestheticEnhancement** | qwen3.5图像与视频美学质量分析 |  
| **� 分镜助手 sd-webui-Storyboard Assistant** | 专业的剧本与分镜管理系统，支持多故事、多角色管理，可视化分镜墙编排 | 
| **🎥 相机角度选择器sd-webui-camera-angle-selector** | 3D 可视化多角度提示词选择，支持方位角、高程角、距离调整 |
| **🎬 多媒体处理sd-webui-multimodal-media** | qwen3-TTS，唇形同步多媒体处理|  |
| **👁️ 图像识别与语言交互sd-webui-qwen-vision-chat** | 基于qwen3.5视觉模型的图像识别与对话功能 |  
| **✂️ 图像分割与清理sd-webui-sam-matting** | 图像分割、抠图、背景清理功能 |

### 使用参考：【webui分镜助手插件与qwen3-TTS协作】 https://www.bilibili.com/video/BV1foQzBMErp/?share_source=copy_web&vd_source=6e632e0a48d2988d197f22d4879aabb2


### 修改的旧插件

| 插件名称 | 修改说明 |
|---------|---------|
| **🔧 adetailer修脸** | 兼容性优化 |
| **🔧 SD-PPP** | PS插件|
| **🔧 Auto-Photoshop-StableDiffusion-Plugin** | PS插件|
| **🏷️ WD 1.4 标签器** | 自动生成图像标签 

### 汉化的内置功能

| 功能名称 | 说明 |
|---------|------|
| **🛡️ 显存防溢出保护** | 防止显存溢出导致的崩溃 |
| **🖼️ 多图拼接参考** | 多图像拼接与参考功能 |
| **🌱 种子多样性增强** | 改善蒸馏模型的种子多样性 |
| **⚡ 频谱预测加速** | 免训练加速所有模型 |
| **🔥 PyTorch 编译加速** | 使用 torch.compile 加速推理 |
| **🎛️ 调制引导控制** | 改善 Anima 模型的生成质量 |

---

## 优化功能

- **ComfyUI 后端重写** - 内存管理、模型补丁、注意力机制等
- **模型加载优化** - 加速启动和模型切换
- **内存泄漏修复** - 切换 checkpoint 时的内存问题
- **uv 包管理器支持** - 大幅加速依赖安装
- **多种注意力优化** - SageAttention、FlashAttention、xFormers
- **Triton 内核** - int8 矩阵乘法加速
- **Spectrum** - 免训练加速所有模型
- **TAESD 实时预览** - 所有模型支持
- **半精度上采样器** - 加速同时降低质量
- **GPU 瓦片合成** - 加速上采样
- **支持更多图像格式** - .avif、.heif、.jxl
- **X/Y/Z 图自动行计数优化**

---
## 特性

### 支持的模型

- **Anima** - 最新的文本到图像模型
- **Flux.2-Klein** (4B / 9B) - 高效的小模型
- **Z-Image / Z-Image-Turbo** - 快速图像生成
- **Wan 2.2** - 视频生成模型
  - 使用 Refiner 实现高噪声/低噪声切换
- **Qwen-Image / Qwen-Image-Edit** - 通义千问图像模型
- **Flux Kontext** - 支持上下文控制
- **Nunchaku (SVDQ)** - 量化模型加速
- **Lumina-Image-2.0** - Neta-Lumina / NetaYume-Lumina
- **Chroma1-HD** - 高清图像生成
- **SDXL 高级模型** - 包括 v-prediction、Zero Terminal SNR、Rectified Flow 等

> [!重要提示]
> 导出视频需要安装 **[FFmpeg](https://ffmpeg.org/)**

### 模型组件说明

不同类型的模型需要不同的组件文件，以下是各类模型的组件结构：
使用参考链接https://github.com/Haoming02/sd-webui-forge-classic/wiki/Inference-References

#### SD1.5 / SD2.1 模型
只需一个 checkpoint 文件即可运行：
```
models/diffusion_models/
└── your_model.safetensors  # 包含 UNet + VAE + CLIP
```

#### SDXL 模型
同样只需一个 checkpoint 文件：
```
models/diffusion_models/
└── sdxl_model.safetensors  # 包含 UNet + VAE + 双文本编码器
```

#### Flux 模型
Flux 模型采用 DiT 架构，组件分离存储：
```
models/diffusion_models/
└── flux1-dev-fp8.safetensors    # 或 flux-schnell.safetensors

models/text_encoder/         # T5 文本编码器
└── t5xxl_fp16.safetensors

models/clip/                 # CLIP 文本编码器（可选）
└── clip_l.safetensors

models/VAE/                  # Flux 专用 VAE（可选）
└── flux_vae.safetensors
```

#### Flux.2-Klein 模型
Flux.2-Klein 是 多模态编辑模型
```
models/diffusion_models/
├── flux2-klein-4b.safetensors   # 4B 轻量版
└── flux-2-klein-9b-fp8.safetensors   # 9B 标准版

models/text_encoder/              # 文本编码器（首次运行自动下载）
└── qwen_3_8b_fp8mixed.safetensors
└── qwen_3_4b.safetensors

models/vae/
└── flux2-vae.safetensors
```

#### Anima 模型
Anima 是二次元高质量专用模型：
```
models/diffusion_models/
└── anima.safetensors            # Anima 主模型

models/text_encoder/              # 文本编码器
├── qwen_3_06b_base.safetensors      # 通义千问编码器

models/VAE/
└── qwen_image_vae.safetensors       # Qwen-Image 专用 VAE
```

#### Qwen-Image 模型
```
models/diffusion_models/
├──（编辑模型） svdq-fp4_r128-qwen-image-edit-2509-lightningv2.0-8steps.safetensors  # 主模型（nunchaku版本的qwen模型，在魔搭社区进行下载要区分50系模型）
├──（文生图模型）svdq-fp4_r128-qwen-image-lightningv1.1-8steps.safetensors # 主模型（nunchaku版本的qwen模型，在魔搭社区进行下载要区分50系模型）

models/text_encoder/              # 文本编码器
├── qwen_2.5_vl_7b_fp8_scaled.safetensors   # 通义千问编码器
models/VAE/
└── qwen_image_vae.safetensors       # Qwen-Image 专用 VAE
```

#### Wan 2.2 视频模型

# 文生视频模型
```
models/diffusion_models/
├── wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors  # 文生视频模型
├── wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors  # 文生视频模型
models/text_encoder/   # 文本编码器          
├── umt5-xx-fp8-scaled.safetensors  # 文本编码器
├── umt5-xxl-enc-bf16.safetensors    # 文本编码器
models/VAE/
└── wan_2.2_vae.safetensors      # Wan 2.2 专用 VAE
```

#### ControlNet 模型
```
models/ControlNet/
├── controlnet-union-sdxl-1.0_promax.safetensors  # 
└── ...
```

#### ControlNetPreprocessor预处理模型
```
models/ontrolNetPreprocessor/
├── dw-ll_ucoco_384.pth  # 
└── ...
```

## 模型目录结构

项目 `models` 目录包含以下子目录：

| 目录名称 | 说明 |
|---------|------|
| **Stable-diffusion** | 主模型目录，存放 SD1.5、SDXL、Flux 等大模型 |
| **Lora** | LoRA 微调模型，用于风格/角色/概念微调 |
| **VAE** | 变分自编码器，影响图像色彩和细节 |
| **text_encoder** | 文本编码器模型（T5、CLIP 等） |
| **clip** | CLIP 视觉-语言模型 |
| **diffusion_models** | 扩散模型（Flux、SD3 等 DiT 架构） |
| **embeddings** | 文本反转嵌入向量 |
| **ControlNet** | ControlNet 控制网络模型 |
| **ControlNetPreprocessor** | ControlNet 预处理器模型 |
| **ESRGAN** | ESRGAN 超分辨率放大模型 |
| **RealESRGAN** | RealESRGAN 超分辨率模型 |
| **adetailer** | ADetailer 面部修复模型 |
| **cleaner** | 图像清理模型 |
| **sams** | SAM (Segment Anything Model) 分割模型 |
| **qwen3-tts** | 通义千问语音合成模型 |
| **whisper-tiny** | Whisper 语音识别模型 |
| **LatentSync** | 潜在同步模型（音视频同步） |
| **diffusers** | Diffusers 格式模型 |

---

## 安装

1. 安装 **[Python 3.13.12](https://www.python.org/downloads/release/python-31312/)**
   - 记得勾选 `Add Python to PATH`

### 启动

1. （可选）配置命令行参数
2. 双击运行 `webui（启动器）.bat`
3. 首次启动时会自动安装所有依赖
4. 安装完成后，WebUI 会自动在浏览器中启动

---

## 模型共享配置

本项目支持与 ComfyUI 双向模型共享：

### WebUI 共享模型给 ComfyUI

在 ComfyUI 的 `extra_model_paths.yaml` 中添加：
```yaml
a111:
    base_path: sd-webui-forge-neo-v2/webui
    checkpoints: models/Stable-diffusion
    loras: models/Lora
    vae: models/VAE
    text_encoder: models/text_encoder
    unet: models/unet
    diffusion_models: models/diffusion_models
    clip: models/clip
```

### ComfyUI 共享模型给 WebUI

创建 `comfy_paths.yaml`：
```yaml
comfyui:
    base_path: d:\ComfyUI-aki-v2.1\ComfyUI\models
    checkpoints: checkpoints
    diffusion_models: diffusion_models
    unet: unet
    clip: clip
    text_encoders: text_encoders
    loras: loras
    vae: vae
```

---

## 问题

- Linux、macOS、AMD 将不会得到官方支持，因为我无法验证或维护它们...

> [!提示]
> 查看 [Wiki](https://github.com/Haoming02/sd-webui-forge-classic/wiki) 获取更多信息

---

## 致谢

感谢原作者 **Haoming02** 提供的 [sd-webui-forge-classic](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) 项目。

感谢 **AUTOMATIC1111**、**lllyasviel** 和 **comfyanonymous**、**kijai**、**city96**，以及所有其他贡献者，感谢他们在开源图像生成社区中的宝贵努力。

---

<p align="right">
<sub><i>Buy me a <a href="https://ko-fi.com/Haoming">Coffee</a>~ ☕
</i></sub>
</p>
