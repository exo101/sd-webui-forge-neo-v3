# Stable Diffusion WebUI Forge - Neo 

<p align="center">
<img src="html\ui.webp" width=512 alt="UI">
</p>

## 项目介绍

本项目是基于 **Stable Diffusion WebUI Forge Neo** 的中文定制版本，专注于优化和易用性，目标是通过简单易用的 GUI 运行最新的流行模型。

**原作者**：[Haoming02](https://github.com/Haoming02)  
**原项目链接**：[https://github.com/Haoming02/sd-webui-forge-classic/tree/neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo?tab=readme-ov-file#installation)

> [!说明]
> 本版本为改良版本，部分插件直接安装会发生兼容性错误，为了适应众多新旧插件做了些许修改。

### Forge 是什么？

Stable Diffusion WebUI Forge 是建立在原始 AUTOMATIC1111 Stable Diffusion WebUI 之上的平台，旨在：
- 简化开发流程
- 优化资源管理
- 加速推理
- 研究实验性功能

名称 "Forge" 的灵感来自 "Minecraft Forge"。该项目旨在成为 Stable Diffusion WebUI 的 "Forge"。

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

---

## 插件列表

### 新增插件

| 插件名称 | 功能说明 |
|---------|---------|
| **� 美学提升** | 图像美学质量优化 |
| **� 分镜助手** | 专业的剧本与分镜管理系统，支持多故事、多角色管理，可视化分镜墙编排 |
| **🎥 相机角度选择器** | 3D 可视化多角度提示词选择，支持方位角、高程角、距离调整 |
| **🎬 多媒体处理** | 多媒体文件处理功能 |
| **👁️ 图像识别与语言交互** | 基于视觉模型的图像识别与对话功能 |
| **✂️ 图像分割与清理** | 图像分割、抠图、背景清理功能 |
| **🏷️ WD 1.4 标签器** | 自动生成图像标签 |

### 修改的旧插件

| 插件名称 | 修改说明 |
|---------|---------|
| **🔧 辅助** | 兼容性优化 |
| **🏷️ WD 1.4 标签器** | 兼容性优化 |

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

## 模型目录结构

项目 `models` 目录包含以下子目录：

| 目录名称 | 说明 |
|---------|------|
| **Stable-diffusion** | 主模型目录，存放 SD1.5、SDXL、Flux 等大模型 |
| **Lora** | LoRA 微调模型，用于风格/角色/概念微调 |
| **VAE** | 变分自编码器，影响图像色彩和细节 |
| **text_encoder** | 文本编码器模型（T5、CLIP 等） |
| **clip** | CLIP 视觉-语言模型 |
| **unet** | UNet 去噪网络模型 |
| **diffusion_models** | 扩散模型（Flux、SD3 等 DiT 架构） |
| **embeddings** | 文本反转嵌入向量 |
| **ControlNet** | ControlNet 控制网络模型 |
| **ControlNetPreprocessor** | ControlNet 预处理器模型 |
| **ESRGAN** | ESRGAN 超分辨率放大模型 |
| **RealESRGAN** | RealESRGAN 超分辨率模型 |
| **adetailer** | ADetailer 面部修复模型 |
| **cleaner** | 图像清理模型 |
| **sams** | SAM (Segment Anything Model) 分割模型 |
| **qwen-image** | 通义千问图像生成模型 |
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
    base_path: D:\sd-webui-forge-classic-neo-v2
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
