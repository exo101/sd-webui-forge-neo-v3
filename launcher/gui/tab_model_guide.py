"""模型架构使用说明 Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QHBoxLayout, QDialog, QPushButton
)
from PyQt6.QtCore import Qt
from .theme import COLORS


class ModelGuideTab(QWidget):
    """模型架构使用说明标签页"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        content = QWidget()
        content.setStyleSheet(f"background-color:{COLORS['bg_card']};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)
        
        # 标题
        title = QLabel("📚 模型架构使用说明")
        title.setStyleSheet(
            f"color:{COLORS['text_primary']};font-size:24px;font-weight:bold;"
        )
        content_layout.addWidget(title)
        
        # 说明文字
        intro = QLabel(
            "本页面详细介绍 WebUI Forge Neo v2 支持的各种模型架构、组件结构和配置方法。\n"
            "帮助您了解如何正确放置和使用各类模型文件。"
        )
        intro.setWordWrap(True)
        intro.setStyleSheet(
            f"color:{COLORS['text_secondary']};font-size:13px;line-height:1.6;"
        )
        content_layout.addWidget(intro)
        
        # 分割线
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{COLORS['border']};")
        content_layout.addWidget(sep)
        
        # 模型概述
        overview_section = self._create_overview_section()
        content_layout.addWidget(overview_section)
        
        # SD1.5/SD2.1
        sd15_section = self._create_sd15_section()
        content_layout.addWidget(sd15_section)
        
        # SDXL
        sdxl_section = self._create_sdxl_section()
        content_layout.addWidget(sdxl_section)
        
        # Flux
        flux_section = self._create_flux_section()
        content_layout.addWidget(flux_section)
        
        # Flux.2-Klein
        flux2_section = self._create_flux2_klein_section()
        content_layout.addWidget(flux2_section)
        
        # Anima
        anima_section = self._create_anima_section()
        content_layout.addWidget(anima_section)
        
        # Qwen-Image
        qwen_section = self._create_qwen_image_section()
        content_layout.addWidget(qwen_section)
        
        # Zimage
        zimage_section = self._create_zimage_section()
        content_layout.addWidget(zimage_section)
        
        # Wan 2.2
        wan_section = self._create_wan_section()
        content_layout.addWidget(wan_section)
        
        # ControlNet
        controlnet_section = self._create_controlnet_section()
        content_layout.addWidget(controlnet_section)
        
        # LoRA
        lora_section = self._create_lora_section()
        content_layout.addWidget(lora_section)
        
        # Qwen Vision Chat
        qwen_vision_section = self._create_qwen_vision_chat_section()
        content_layout.addWidget(qwen_vision_section)
        
        # See-Through
        see_through_section = self._create_see_through_section()
        content_layout.addWidget(see_through_section)
        
        # Multimodal Media
        multimodal_section = self._create_multimodal_media_section()
        content_layout.addWidget(multimodal_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _create_section_title(self, title: str) -> QLabel:
        """创建章节标题"""
        label = QLabel(title)
        label.setStyleSheet(
            f"color:{COLORS['accent_light']};font-size:18px;font-weight:bold;margin-top:16px;"
        )
        return label
    
    def _create_subsection_title(self, title: str) -> QLabel:
        """创建子章节标题"""
        label = QLabel(title)
        label.setStyleSheet(
            f"color:{COLORS['text_primary']};font-size:15px;font-weight:bold;margin-top:12px;"
        )
        return label
    
    def _create_description(self, text: str) -> QLabel:
        """创建描述文本"""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(
            f"color:{COLORS['text_secondary']};font-size:12px;line-height:1.6;"
        )
        return label
    
    def _create_code_block(self, code: str) -> QLabel:
        """创建代码块"""
        label = QLabel(code)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            QLabel {{
                background:{COLORS['bg_dark']};
                color:{COLORS['cyan']};
                border:1px solid {COLORS['border']};
                border-radius:6px;
                padding:12px;
                font-family:'Consolas','Courier New',monospace;
                font-size:11px;
                line-height:1.5;
            }}
        """)
        return label
    
    def _create_note(self, text: str, note_type: str = "info") -> QLabel:
        """创建提示框"""
        colors_map = {
            "info": ("#1e3a5f", COLORS['cyan']),
            "warning": ("#3d2e1f", COLORS['orange']),
            "tip": ("#1a3a2a", COLORS['green']),
        }
        bg, fg = colors_map.get(note_type, colors_map["info"])
        
        label = QLabel(f"💡 {text}")
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            QLabel {{
                background:{bg};
                color:{fg};
                border-left:4px solid {fg};
                border-radius:4px;
                padding:10px 14px;
                font-size:12px;
                line-height:1.5;
            }}
        """)
        return label
    

    

    
    def _create_overview_section(self) -> QWidget:
        """创建模型概述部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        layout.addWidget(self._create_section_title("🎯 支持的模型列表"))
        
        overview_text = """
        <div style="line-height:1.8;color:#D1D5DB;">
        <p>WebUI Forge Neo v2 支持以下主流模型架构：</p>
        <table style="width:100%;border-collapse:collapse;margin:12px 0;">
            <tr style="background:#1F2937;">
                <th style="padding:10px;text-align:left;border:1px solid #374151;color:#60A5FA;">模型名称</th>
                <th style="padding:10px;text-align:left;border:1px solid #374151;color:#60A5FA;">类型</th>
                <th style="padding:10px;text-align:left;border:1px solid #374151;color:#60A5FA;">推荐显存</th>
                <th style="padding:10px;text-align:left;border:1px solid #374151;color:#60A5FA;">说明</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Wan 2.2</b></td>
                <td style="padding:8px;border:1px solid #374151;">视频生成</td>
                <td style="padding:8px;border:1px solid #374151;">16GB+</td>
                <td style="padding:8px;border:1px solid #374151;">文生视频模型，支持高/低噪声切换</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>Qwen-Image</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">12GB+</td>
                <td style="padding:8px;border:1px solid #374151;">通义千问图像模型，支持文生图和编辑</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Qwen Vision Chat</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像识别与交互</td>
                <td style="padding:8px;border:1px solid #374151;">8GB+</td>
                <td style="padding:8px;border:1px solid #374151;">Qwen3.5 图像识别与语言交互模型</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>See-Through</b></td>
                <td style="padding:8px;border:1px solid #374151;">图层分解</td>
                <td style="padding:8px;border:1px solid #374151;">8GB+</td>
                <td style="padding:8px;border:1px solid #374151;">动漫图像多层 PSD 分解工具</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Multimodal Media</b></td>
                <td style="padding:8px;border:1px solid #374151;">多模态处理</td>
                <td style="padding:8px;border:1px solid #374151;">8GB+</td>
                <td style="padding:8px;border:1px solid #374151;">TTS、数字人、视频生成等多功能插件</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Flux.2-Klein</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">12GB+</td>
                <td style="padding:8px;border:1px solid #374151;">多模态编辑模型，4B/9B 版本</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Flux</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">12GB+</td>
                <td style="padding:8px;border:1px solid #374151;">DiT 架构模型，组件分离存储</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>Anima</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">8GB+</td>
                <td style="padding:8px;border:1px solid #374151;">二次元高质量专用模型</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>SDXL</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">8GB+</td>
                <td style="padding:8px;border:1px solid #374151;">高级 SDXL 模型</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>SD1.5 / SD2.1</b></td>
                <td style="padding:8px;border:1px solid #374151;">图像生成</td>
                <td style="padding:8px;border:1px solid #374151;">6GB+</td>
                <td style="padding:8px;border:1px solid #374151;">经典 Stable Diffusion 模型</td>
            </tr>
        </table>
        </div>
        """
        overview_label = QLabel(overview_text)
        overview_label.setOpenExternalLinks(True)
        overview_label.setWordWrap(True)
        overview_label.setStyleSheet("QLabel { background:transparent; }")
        layout.addWidget(overview_label)
        
        return container
    
    def _create_sd15_section(self) -> QWidget:
        """创建 SD1.5/SD2.1 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🔵 SD1.5 / SD2.1 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_description("需要以下文件才能正常运行："))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
└── your_model.safetensors      # 主模型文件（Checkpoint）

models/vae/
└── vae-ft-mse-840000-ema-pruned.safetensors  # VAE 文件（必需）"""))
        
        layout.addWidget(self._create_description("⚠️ <b>重要提示：</b>虽然某些 Checkpoint 文件内置了 VAE，但为了获得最佳效果，建议单独放置 VAE 文件。如果生成图像出现颜色异常、灰暗或模糊，请检查是否正确配置了 VAE。"))
        

        
        return container
    
    def _create_sdxl_section(self) -> QWidget:
        """创建 SDXL 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🟣 SDXL 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_description("同样只需一个 checkpoint 文件："))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
└── xl-lustrious_4.0.safetensors  # SDXL主模型"""))
        

        
        return container
    
    def _create_flux_section(self) -> QWidget:
        """创建 Flux 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("⚡ Flux 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_description("Flux 模型采用 DiT 架构，组件分离存储："))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
└── flux1-dev-fp8.safetensors    # 或 flux-schnell.safetensors

models/text_encoder/         # T5 文本编码器
└── t5xxl_fp16.safetensors

models/clip/                 # CLIP 文本编码器（可选）
└── clip_l.safetensors

models/VAE/                  # Flux 专用 VAE（可选）
└── flux_vae.safetensors"""))
        

        
        return container
    
    def _create_flux2_klein_section(self) -> QWidget:
        """创建 Flux.2-Klein 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🌟 Flux.2-Klein 模型"))
        layout.addWidget(self._create_description("Flux.2-Klein 是多模态编辑模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
├── flux2-klein-4b.safetensors   # 4B 轻量版
└── flux-2-klein-9b-fp8.safetensors   # 9B 标准版

models/text_encoder/              # 文本编码器
├── qwen_3_8b_fp8mixed.safetensors
└── qwen_3_4b.safetensors

models/vae/
└── flux2-vae.safetensors"""))
        

        
        return container
    
    def _create_anima_section(self) -> QWidget:
        """创建 Anima 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🎨 Anima 模型"))
        layout.addWidget(self._create_description("Anima 是二次元高质量专用模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
└── anima.safetensors            # Anima 主模型

models/text_encoder/              # 文本编码器
└── qwen_3_06b_base.safetensors      # 通义千问编码器

models/VAE/
└── qwen_image_vae.safetensors       # Qwen-Image 专用 VAE"""))
        

        
        return container
    
    def _create_qwen_image_section(self) -> QWidget:
        """创建 Qwen-Image 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🤖 Qwen-Image 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
├── svdq-fp4_r128-qwen-image-edit-2509-lightningv2.0-8steps.safetensors  # 编辑模型
└── svdq-fp4_r128-qwen-image-lightningv1.1-8steps.safetensors  # 文生图模型

models/text_encoder/              # 文本编码器
└── qwen_2.5_vl_7b_fp8_scaled.safetensors   # 通义千问编码器

models/VAE/
└── qwen_image_vae.safetensors       # Qwen-Image 专用 VAE"""))
        
        layout.addWidget(self._create_subsection_title("模型类型对比"))
        layout.addWidget(self._create_description("""<table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#1f2937;">
                <th style="padding:10px;border:1px solid #374151;text-align:left;color:#60a5fa;">模型类型</th>
                <th style="padding:10px;border:1px solid #374151;text-align:left;color:#60a5fa;">用途</th>
                <th style="padding:10px;border:1px solid #374151;text-align:left;color:#60a5fa;">特点</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>编辑模型</b><br><code style="color:#fbbf24;">qwen-image-edit</code></td>
                <td style="padding:8px;border:1px solid #374151;">图像编辑功能</td>
                <td style="padding:8px;border:1px solid #374151;">支持对现有图像进行修改、增强、风格转换等操作</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>文生图模型</b><br><code style="color:#fbbf24;">qwen-image</code></td>
                <td style="padding:8px;border:1px solid #374151;">文本生成图像功能</td>
                <td style="padding:8px;border:1px solid #374151;">根据文字描述从头生成全新的图像</td>
            </tr>
        </table>"""))
        
        layout.addWidget(self._create_note("""⚠️ <b>重要提示 - 魔搭社区下载注意事项：</b><br><br>
<b>1. 区分 50 系与非 50 系模型：</b><br>
&nbsp;&nbsp;&nbsp;• <b>50 系模型</b>：专为 NVIDIA RTX 50 系列显卡优化（如 RTX 5090、5080）<br>
&nbsp;&nbsp;&nbsp;• <b>非 50 系模型</b>：适用于其他显卡（RTX 30/40 系列、AMD 等）<br>
&nbsp;&nbsp;&nbsp;• <b>务必根据您的显卡型号选择对应版本</b>，否则可能导致性能问题或无法运行<br><br>
<b>2. 如何识别：</b><br>
&nbsp;&nbsp;&nbsp;• 文件名中包含 <code>rtx50</code>、<code>50系</code>、<code>50-series</code> 等关键词的为 50 系模型<br>
&nbsp;&nbsp;&nbsp;• 没有这些标识的为非 50 系通用模型<br><br>
<b>3. 推荐配置：</b><br>
&nbsp;&nbsp;&nbsp;• <b>RTX 5090/5080</b>：使用 50 系优化模型，性能提升显著<br>
&nbsp;&nbsp;&nbsp;• <b>RTX 4090/4080/3090</b>：使用非 50 系标准模型即可<br>
&nbsp;&nbsp;&nbsp;• <b>显存要求</b>：建议 16GB+ 显存以获得最佳体验""", "warning"))
        

        
        return container
    
    def _create_zimage_section(self) -> QWidget:
        """创建 Zimage 模型部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🌟 Zimage 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
└── z_image_turbo_bf16.safetensors  # Zimage 模型

models/text_encoder/              # 文本编码器
└── qwen_3_4b.safetensorsx  # Qwen 3.4B 文本编码器

models/VAE/
└── flux-vae.safetensors  # Flux VAE"""))
        

        
        return container
    
    def _create_wan_section(self) -> QWidget:
        """创建 Wan 2.2 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🎬 Wan 2.2 视频模型"))
        
        layout.addWidget(self._create_subsection_title("文生视频模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusion_models/
├── wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors  # 文生视频模型（高噪声）
└── wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors   # 文生视频模型（低噪声）

models/text_encoder/   # 文本编码器          
├── umt5-xx-fp8-scaled.safetensors  # 文本编码器
└── umt5-xxl-enc-bf16.safetensors    # 文本编码器

models/VAE/
└── wan_2.2_vae.safetensors      # Wan 2.2 专用 VAE"""))
        
        layout.addWidget(self._create_note("""• 高噪声模型：适合需要更多创意的视频生成<br>
• 低噪声模型：适合需要更稳定输出的视频生成""", "tip"))
        

        
        return container
    
    def _create_controlnet_section(self) -> QWidget:
        """创建 ControlNet 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🎮 ControlNet 模型"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/ControlNet/
├── controlnet-union-sdxl-1.0_promax.safetensors  # SDXL ControlNet
└── ...  # 其他 ControlNet 模型

models/ControlNet/preprocessor/  # 预处理器目录
├── Animal openpose
├── lineart
├── mlsd
├── openpose
└── zoedepth"""))
        
        layout.addWidget(self._create_subsection_title("预处理器类型"))
        layout.addWidget(self._create_description("""• <b>Animal openpose</b> - 动物姿态检测
• <b>lineart</b> - 线稿提取
• <b>mlsd</b> - 直线检测（建筑/室内）
• <b>openpose</b> - 人体姿态检测
• <b>zoedepth</b> - 深度图估计"""))
        
        layout.addWidget(self._create_note("""• 不同预处理器适用于不同类型的参考图<br>
• OpenPose 适合人物姿势控制<br>
• Lineart 适合线稿上色<br>
• MLSD 适合建筑/室内设计<br>
• ZoeDepth 适合保持场景深度关系""", "tip"))
        
        return container
    
    def _create_lora_section(self) -> QWidget:
        """创建 LoRA 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("✨ LoRA 模型"))
        layout.addWidget(self._create_description("LoRA 是轻量级微调模型，用于调整画风、角色或概念"))
        
        layout.addWidget(self._create_subsection_title("模型目录"))
        layout.addWidget(self._create_description("""• <b>LoRA 模型</b>：<code>models/Lora/</code>"""))
        
        layout.addWidget(self._create_note("""• LoRA 文件通常较小（几十 MB 到几百 MB）<br>
• 不同基础模型需要对应的 LoRA（SD1.5 LoRA 不能用于 SDXL）<br>
• 权重过高可能导致画面崩坏""", "info"))
        
        return container
    
    def _create_qwen_vision_chat_section(self) -> QWidget:
        """创建 Qwen Vision Chat 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🤖 Qwen Vision Chat - 图像识别与语言交互"))
        layout.addWidget(self._create_description("基于 Ollama 的 Qwen 多模态大模型，支持图像识别和智能对话"))
        
        layout.addWidget(self._create_subsection_title("支持的视觉模型（带图片识别）"))
        layout.addWidget(self._create_description("""<table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#1f2937;">
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">模型名称</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">显存要求</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">特点</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><code>qwen3.5:9b</code></td>
                <td style="padding:8px;border:1px solid #374151;">16GB+</td>
                <td style="padding:8px;border:1px solid #374151;">高精度版本，识别最准确</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><code>qwen3.5:4b</code></td>
                <td style="padding:8px;border:1px solid #374151;">12GB</td>
                <td style="padding:8px;border:1px solid #374151;">平衡版本，推荐大多数用户</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><code>qwen3-vl:8b</code></td>
                <td style="padding:8px;border:1px solid #374151;">12GB+</td>
                <td style="padding:8px;border:1px solid #374151;">视觉语言模型</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><code>qwen3-vl:4b</code></td>
                <td style="padding:8px;border:1px solid #374151;">10GB</td>
                <td style="padding:8px;border:1px solid #374151;">中等视觉模型</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><code>qwen3-vl:2b</code></td>
                <td style="padding:8px;border:1px solid #374151;">8GB</td>
                <td style="padding:8px;border:1px solid #374151;">轻量级，低显存首选</td>
            </tr>
        </table>"""))
        
        layout.addWidget(self._create_subsection_title("支持的语言模型（纯文本对话）"))
        layout.addWidget(self._create_description("""• <code>qwen3:latest</code> - 最新版本<br>
• <code>qwen3.5:4b</code> - 平衡版本<br>
• <code>deepseek-r1:8b</code> - DeepSeek 模型"""))
        
        layout.addWidget(self._create_subsection_title("安装步骤"))
        layout.addWidget(self._create_description("""1. 安装 Ollama：访问 https://ollama.com/ 下载安装<br>
2. 下载模型（示例）：<br>
&nbsp;&nbsp;&nbsp;<code>ollama run qwen3.5:4b</code> （推荐）<br>
&nbsp;&nbsp;&nbsp;<code>ollama run qwen3-vl:2b</code> （低显存）<br>
3. 插件已预装在 extensions 目录<br>
4. 重启 WebUI Forge，在顶部标签页找到"图像识别与语言交互" """))
        
        layout.addWidget(self._create_subsection_title("核心功能"))
        layout.addWidget(self._create_description("""• 🖼️ <b>视觉模型对话</b>：上传图片进行智能识别和对话<br>
• 💬 <b>纯文本对话</b>：无需图片即可进行文本交流<br>
• 🔄 <b>多轮对话</b>：支持上传一次图片后连续提问<br>
• 🎯 <b>快捷描述</b>：自然语言、MJ提示词、分镜构图、视频生成等<br>
• 📁 <b>标签管理</b>：批量处理 txt 文件的关键词添加/删除<br>
• 🖼️ <b>图像管理</b>：图片预览、目录加载、网格展示"""))
        
        layout.addWidget(self._create_note("""• 需要先安装 Ollama 并下载对应模型<br>
• 视觉模型（带 vl 后缀）才能识别图片<br>
• 显存不足时选择更小的模型（如 qwen3-vl:2b）<br>
• Ollama 默认端口：11434""", "tip"))
        

        
        return container
    
    def _create_see_through_section(self) -> QWidget:
        """创建 See-Through 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🎨 See-Through - 动漫图层分解"))
        layout.addWidget(self._create_description("基于 AI 的动漫图像分解工具，将单张动漫图像转换为多层 PSD 文件"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/diffusers/
├── models--24yearsold--seethroughv0.0.1_marigold_nf4   # Marigold深度估计模型（NF4量化）
└── models--24yearsold--seethroughv0.0.2_layerdiff3d_nf4  # LayerDiff 3D透明层生成模型（NF4量化）

models/sams/  # SAM场景分割模型
└── ...  # vit_b/vit_l/vit_h 等版本"""))
        
        layout.addWidget(self._create_subsection_title("核心技术"))
        layout.addWidget(self._create_description("""• <b>LayerDiff 3D</b>：基于扩散的透明层生成<br>
• <b>Marigold 深度估计</b>：专为动漫优化的伪深度估计<br>
• <b>SAM 分割</b>：语义身体部分分割<br>
• <b>PSD 输出</b>：导出为可编辑的 Photoshop 文件"""))
        
        layout.addWidget(self._create_subsection_title("分割模式"))
        layout.addWidget(self._create_description("""<table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#1f2937;">
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">模式</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">适用场景</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">特点</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>人物分割</b></td>
                <td style="padding:8px;border:1px solid #374151;">动漫人物、写实人物、人物插画</td>
                <td style="padding:8px;border:1px solid #374151;">分层头发、身体部位、饰品、装备等</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>场景分割 (SAM)</b></td>
                <td style="padding:8px;border:1px solid #374151;">复杂场景、背景元素</td>
                <td style="padding:8px;border:1px solid #374151;">自动分割场景中的多个元素</td>
            </tr>
        </table>"""))
        
        layout.addWidget(self._create_subsection_title("SAM 模型类型"))
        layout.addWidget(self._create_description("""• <code>vit_b</code> - 小模型（~1.2GB），速度快<br>
• <code>vit_l</code> - 中模型（~2.5GB），平衡选择<br>
• <code>vit_h</code> - 大模型（~3.9GB），精度最高"""))
        
        layout.addWidget(self._create_subsection_title("显存配置建议"))
        layout.addWidget(self._create_description("""<table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#1f2937;">
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">显存</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">分辨率</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">批处理</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">优化选项</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;">8GB</td>
                <td style="padding:8px;border:1px solid #374151;">512-768</td>
                <td style="padding:8px;border:1px solid #374151;">1-2</td>
                <td style="padding:8px;border:1px solid #374151;">启用 NF4 量化、缓存嵌入</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;">12GB</td>
                <td style="padding:8px;border:1px solid #374151;">768-1024</td>
                <td style="padding:8px;border:1px solid #374151;">2-3</td>
                <td style="padding:8px;border:1px solid #374151;">启用缓存嵌入</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;">16GB</td>
                <td style="padding:8px;border:1px solid #374151;">1024-1280</td>
                <td style="padding:8px;border:1px solid #374151;">3-4</td>
                <td style="padding:8px;border:1px solid #374151;">默认设置</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;">24GB+</td>
                <td style="padding:8px;border:1px solid #374151;">1280-1536</td>
                <td style="padding:8px;border:1px solid #374151;">4-6</td>
                <td style="padding:8px;border:1px solid #374151;">可使用较大分辨率</td>
            </tr>
        </table>"""))
        
        layout.addWidget(self._create_subsection_title("内存优化选项"))
        layout.addWidget(self._create_description("""• <b>NF4 量化 (8GB GPU)</b>：使用 4 位量化，峰值显存~8GB<br>
• <b>缓存文本嵌入</b>：节省约 2GB 显存且无速度损失<br>
• <b>组卸载</b>：将显存降至~0.2GB，但速度降低 2-3 倍<br>
• <b>CPU 卸载</b>：将模型卸载到 CPU 以节省显存"""))
        
        layout.addWidget(self._create_subsection_title("输出文件"))
        layout.addWidget(self._create_description("""• <b>人物分割</b>：<code>extensions\\sd-webui-see-through\\see-through\\workspace\\layerdiff_output\\</code><br>
• <b>场景分割</b>：<code>extensions\\sd-webui-see-through\\see-through\\workspace\\scene_output\\</code><br>
• 包含：分层 PSD 文件、各图层 PNG、深度图、分割掩码"""))
        
        layout.addWidget(self._create_note("""• 适用于动漫人物、写实人物、人物插画<br>
• 动物图像只能获得粗略分割结果<br>
• 插件会自动安装依赖（psd-tools、pycocotools）<br>
• 推理步数推荐 20-30，较低可加快速度""", "tip"))
        

        
        return container
    
    def _create_multimodal_media_section(self) -> QWidget:
        """创建 Multimodal Media 部分"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        layout.addWidget(self._create_section_title("🎬 Multimodal Media - 多模态媒体处理"))
        layout.addWidget(self._create_description("多功能多媒体处理插件，支持 TTS、数字人、视频生成等"))
        
        layout.addWidget(self._create_subsection_title("模型组件结构"))
        layout.addWidget(self._create_code_block("""models/qwen3-tts/  # Qwen3-TTS 语音合成模型
├── Qwen3-TTS-12Hz-1.7B-Base           # 基础版本
├── Qwen3-TTS-12Hz-1.7B-CustomVoice    # 自定义音色版本
└── Qwen3-TTS-12Hz-1.7B-VoiceDesign    # 音色设计版本

models/LatentSync/  # LatentSync 唇形同步模型
└── ...  # 唇形同步模型文件"""))
        
        layout.addWidget(self._create_subsection_title("功能模块"))
        layout.addWidget(self._create_description("""<table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#1f2937;">
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">功能</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">说明</th>
                <th style="padding:8px;border:1px solid #374151;text-align:left;color:#60a5fa;">主要依赖</th>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Qwen3-TTS</b><br>语音合成</td>
                <td style="padding:8px;border:1px solid #374151;">文本转语音，支持多种音色和风格定制</td>
                <td style="padding:8px;border:1px solid #374151;">qwen-tts、soundfile</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>LatentSync</b><br>数字人对口型</td>
                <td style="padding:8px;border:1px solid #374151;">根据图片 + 音频生成对口型视频</td>
                <td style="padding:8px;border:1px solid #374151;">insightface、onnxruntime-gpu</td>
            </tr>
            <tr>
                <td style="padding:8px;border:1px solid #374151;"><b>Qwen Video</b><br>万相视频生成</td>
                <td style="padding:8px;border:1px solid #374151;">图生视频、文生视频、关键帧生视频</td>
                <td style="padding:8px;border:1px solid #374151;">dashscope（阿里云 API）</td>
            </tr>
            <tr style="background:#111827;">
                <td style="padding:8px;border:1px solid #374151;"><b>视频关键帧提取</b></td>
                <td style="padding:8px;border:1px solid #374151;">从视频中提取帧图像，支持批量导出</td>
                <td style="padding:8px;border:1px solid #374151;">ffmpeg-python</td>
            </tr>
        </table>"""))
        
        layout.addWidget(self._create_subsection_title("Qwen Video 支持的模式"))
        layout.addWidget(self._create_description("""• <b>wan2.6-i2v</b>：图生视频（最新版本）<br>
• <b>wan2.5-i2v</b>：图生视频（经典模型）<br>
• <b>wan2.2-kf2v</b>：关键帧生视频<br>
• <b>wan2.5-t2v</b>：文生视频（纯文本）"""))
        
        layout.addWidget(self._create_subsection_title("Python 依赖（自动安装）"))
        layout.addWidget(self._create_description("""插件会在 WebUI 启动时自动检查并安装以下 Python 包：<br>
• <code>insightface</code> - 人脸检测和分析<br>
• <code>onnxruntime-gpu</code> - GPU 加速的 ONNX 运行时<br>
• <code>ffmpeg-python</code> - FFmpeg Python 绑定<br>
• <code>torchaudio</code> - PyTorch 音频处理<br>
• <code>qwen-tts</code> - Qwen3-TTS 语音合成<br>
• <code>soundfile</code>、<code>resampy</code>、<code>librosa</code> - 音频处理<br>
• <code>dashscope</code> - 阿里云百炼 SDK（Qwen Video）<br>
• <code>Pillow</code> - 图像处理"""))
        
        layout.addWidget(self._create_subsection_title("系统工具（可选但推荐）"))
        layout.addWidget(self._create_description("""<b>FFmpeg</b>（推荐安装）⭐<br>
• 用途：视频编解码、音频提取、多媒体转换<br>
• 安装：<code>winget install Gyan.FFmpeg</code><br>
• 不安装的影响：基本功能仍可用，某些高级功能受限<br><br>
<b>SoX</b>（推荐安装）⭐<br>
• 用途：音频预处理、格式转换、音频效果处理<br>
• 安装：<code>winget install DavidHetherington.Sox</code><br>
• 注意：需将 <code>bin</code> 子目录添加到 PATH<br>
• 不安装的影响：使用 Python 库替代，性能略降"""))
        
        layout.addWidget(self._create_subsection_title("Qwen Video 使用说明"))
        layout.addWidget(self._create_description("""1. 获取阿里云百炼 API Key：https://dashscope.console.aliyun.com/<br>
2. 在界面中输入 API Key 并点击"设置"<br>
3. 选择视频生成模式（图生视频/文生视频等）<br>
4. 上传参考图片（如果需要）和输入提示词<br>
5. 配置分辨率、时长等参数<br>
6. 点击"生成视频"按钮（异步处理）<br>
7. 等待任务完成，查看和下载生成的视频"""))
        
        layout.addWidget(self._create_note("""• Python 依赖会自动安装，无需手动操作<br>
• FFmpeg 和 SoX 是可选的，但推荐安装以获得更好性能<br>
• Qwen Video 需要阿里云百炼 API Key（付费服务）<br>
• LatentSync 需要较好的 GPU（推荐 12GB+ 显存）<br>
• 一键安装脚本：<code>quick_install_tools.bat</code>""", "tip"))
        

        
        return container
