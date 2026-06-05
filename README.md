
# Stable Diffusion WebUI Forge - Neo v3 中文改良版

本项目是基于 Stable Diffusion WebUI Forge Neo v3的中文改良版本，专注于优化和多模态插件融合，目标是通过简单易用的 GUI 运行最新的流行模型。

---

本目录是 SD WebUI Forge Neo 的核心工作目录。

---

## 📁 目录结构

```
webui/
├── models/              # 模型文件目录
├── extensions/           # 用户安装的扩展插件
├── extensions-builtin/   # 内置扩展插件
├── output/              # 生成图片输出目录
├── outputs/             # 高分辨率输出目录
├── config_states/       # 配置文件状态备份
├── cache/               # 缓存目录
├── tmp/                 # 临时文件目录
├── scripts/              # 辅助脚本
├── html/                # HTML模板
├── javascript/          # 前端JavaScript
├── localizations/       # 国际化语言文件
├── modules/            # 核心模块
├── modules_forge/      # Forge优化模块
├── backend/            # 后端模型组件
├── config.json        # 配置文件
├── config.py          # 配置模块
├── launch.py          # 启动脚本入口
├── webui.py           # WebUI主程序
└── webui-user.bat     # 用户启动脚本
```

---

## 📦 支持的模型项目

### 图像生成模型

| 模型架构 | 说明 | 显存要求 |
|---------|------|---------|
| **SD1.5 / SD2.1** | Stable Diffusion 1.5 / 2.1 | 4-6GB |
| **SDXL** | Stable Diffusion XL | 8GB+ |
| **Flux** | Flux.1 (DiT架构) | 12GB+ |
| **Flux.2-Klein** | 多模态编辑模型 (4B/9B) | 8-12GB |
| **Anima** | 二次元高质量专用模型 | 12GB+ |
| **Qwen-Image** | 通义千问图像模型 | 12GB+ |
| **Chroma** | Chroma图像模型 | 12GB+ |
| **Mugen** | Mugen动画模型 | 12GB+ |
| **ERNIE-Image** | 文心一格图像模型 | 12GB+ |
| **Neta-Lumina** | Neta-Lumina图像模型 | 12GB+ |


### 模型组件说明

| 组件目录 | 说明 |
|---------|------|
| **Stable-diffusion/** | SD/SDXL/Flux 主模型 |
| **diffusion_models/** | DiT架构模型 (Flux/Wan等) |
| **Lora/** | LoRA 微调模型 |
| **VAE/** | 变分自编码器 |
| **text_encoder/** | 文本编码器 (T5/CLIP/Qwen等) |
| **clip/** | CLIP 文本编码器 |
| **ControlNet/** | ControlNet 控制模型 |
| **ControlNetPreprocessor/** | ControlNet 预处理器 |
| **ESRGAN/** | 超分辨率放大模型 |
| **RealESRGAN/** | RealESRGAN 模型 |
| **unet/** | UNet 模型 |
| **diffusers/** | Diffusers 格式模型 |

---

## 🧩 支持的插件/扩展

### 内置扩展 (extensions-builtin)

#### forge_legacy_preprocessors - 传统预处理器

| 预处理器 | 功能说明 |
|---------|---------|
| **anime_face_segment** | 动漫人脸分割 |
| **binary** | 二值化预处理 |
| **canny** | Canny边缘检测 |
| **color** | 颜色预处理 |
| **densepose** | DensePose姿态检测 |
| **hed** | HED边缘检测 |
| **keypose** | 关键姿态检测 |
| **leres** | 深度估计 |
| **lineart** | 线稿提取 |
| **lineart_anime** | 动漫线稿提取 |
| **manga_line** | 漫画线提取 |
| **mediapipe_face** | MediaPipe人脸检测 |
| **midas** | Midas深度估计 |
| **mlsd** | M-LSD线条检测 |
| **mmpkg/mmseg** | mmseg语义分割 |
| **oneformer** | 全景分割 |
| **zoe** | ZoeDepth深度估计 |

#### extra-options-section - 额外选项分组

提供额外的选项分组功能。

### 第三方扩展 (extensions)

#### 🎨 图像增强类

| 扩展名称 | 功能说明 |
|---------|---------|
| **sd-webui-AestheticEnhancement** | 构图技巧、打光技巧、画师百科，支持Qwen3.5-VL AI智能分析构图和灯光 |
| **sd-webui-SAM-Matting** | 智能分割与抠图，基于SAM模型 |
| **sd-webui-See-Through** | 动漫图层分解，生成PSD分层文件 |
| **sd-webui-Camera-Angle-Selector** | 3D可视化多角度提示词选择器 |

#### 🎬 视频与分镜类

| 扩展名称 | 功能说明 |
|---------|---------|
| **sd-webui-Storyboard-Assistant** | 专业分镜助手，支持多故事/多角色管理，可视化分镜墙编排，音频支持 |
| **sd-webui-Trellis23D** | 3D图像生成项目，支持从图像生成3D模型 |

#### 🎥 多媒体处理类

| 扩展名称 | 功能说明 |
|---------|---------|
| **sd-webui-Multimodal-Media** | 多功能多媒体处理，包含：<br>• **Qwen3-TTS**：文本转语音，支持多种音色定制<br>• **LatentSync**：数字人对口型，根据图片+音频生成对口型视频<br>• **Qwen Video**：万相视频生成（图生视频、文生视频、关键帧生视频）<br>• **视频关键帧提取**：从视频中提取帧图像 |

#### 🤖 AI对话与识别类

| 扩展名称 | 功能说明 |
|---------|---------|
| **sd-webui-Qwen-Vision-Chat** | 基于Qwen3.5的图像识别与对话，支持多轮对话 |
| **sd-webui-AestheticEnhancement** | Qwen3.5-VL AI智能分析（可选，需安装Ollama） |

#### 🛠️ 工具类

| 扩展名称 | 功能说明 |
|---------|---------|
| **ADetailer** | 自动面部修复，检测人脸/手部并重绘 |
| **Civitai-Helper** | Civitai模型下载与管理，支持元数据同步 |
| **LoRA-Prompt-Tool** | LoRA提示词管理，权重调节，快速调用 |
| **Prompt-All-in-One** | 提示词一体化，实时翻译、历史记录、收藏 |
| **Auto-Complete** | 提示词自动补全，Booru标签智能建议 |
| **WD14-Tagger** | 自动生成Booru风格图像标签 |
| **Infinite-Browsing** | 无限滚动图像浏览，虚拟滚动优化 |
| **Localization-zh_Hans** | 简体中文界面翻译 |

#### 🎨 Photoshop集成

| 扩展名称 | 功能说明 |
|---------|---------|
| **Auto-Photoshop-StableDiffusion-Plugin** | Photoshop插件，Photoshop内直接文生图/图生图 |

### 内置优化功能

| 功能 | 说明 |
|-----|------|
| **显存防溢出保护** | 防止显存溢出，支持UNet/VAE分块处理 |
| **多图拼接参考** | 多图像拼接与参考功能 |
| **种子多样性增强** | 改善蒸馏模型的种子多样性 |
| **频谱预测加速** | 免训练加速所有模型 |
| **PyTorch编译加速** | torch.compile加速推理 |
| **TAESD实时预览** | 所有模型支持实时预览 |
| **SageAttention** | Flux模型优化注意力机制 |
| **FlashAttention** | 通用快速注意力 |
| **xFormers** | 兼容性注意力优化 |

---

## ⚙️ 常用设置

### 启动参数配置

编辑 `webui-user.bat` 文件：

```batch
set COMMANDLINE_ARGS=--xformers --enable-insecure-extension-access --skip-python-version-check
```

### 常用参数

| 参数 | 说明 |
|-----|------|
| `--xformers` | 启用xFormers注意力优化 |
| `--medvram` | 中等显存优化 |
| `--lowvram` | 低显存优化 |
| `--enable-insecure-extension-access` | 允许扩展访问 |
| `--api` | 启用API服务 |
| `--listen` | 允许远程访问 |
| `--skip-python-version-check` | 跳过Python版本检查 |

### 显存优化建议

| 显存 | 推荐配置 |
|-----|---------|
| 4-6GB | 启用 `--medvram` |
| 8GB | 使用 `--xformers` |
| 12GB+ | 默认配置即可 |
| 16GB+ | 可启用所有优化 |

---

## 📚 相关资源

- [主项目README](../README.md) - 项目完整说明
- [视频教程](https://www.bilibili.com/video/BV1KfXyBTEXb)
- [QQ交流群]<img width="1284" height="1547" alt="qq群ai交流群" src="https://github.com/user-attachments/assets/88be640b-67bb-488a-a256-c4803834a627" />


---

## 📺 B站频道

关注 **哔哩哔哩（鸡肉爱土豆）** 获取最新教程和更新通知。

---

## 🙏 致谢

感谢以下项目和贡献者：

- **Haoming02** - sd-webui-forge-classic 原作者
- **AUTOMATIC1111** - Stable Diffusion WebUI 原始项目
- **lllyasviel** - Forge 优化框架
- **comfyanonymous** - ComfyUI 项目
- **kijai、city96** - 社区贡献者
- 所有开源图像生成社区的贡献者

---

## 📄 许可证

本项目遵循 AGPL-3.0 许可证。详情请参阅 LICENSE 文件。

---

> **Note**
>
> 此版本整合包通过秋叶aaaki、张吕敏、Haoming02 等多位大佬技术总结做出的版本，不属于任何个人、企业，是非盈利性质的开源软件。
