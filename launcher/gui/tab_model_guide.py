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
    
