# 多GPU切换功能使用说明

## 📋 功能概述

本启动器支持在多显卡系统中选择使用哪张GPU运行Stable Diffusion WebUI。

## 🎯 适用场景

- **双显卡笔记本**: 集成显卡 + 独立显卡，强制使用高性能独显
- **多显卡工作站**: RTX 3090 + RTX 4090，选择更强的卡进行推理
- **多用户共享服务器**: 不同用户使用不同的GPU避免冲突
- **测试对比**: 在不同显卡上测试性能差异

## 🔧 使用方法

### 方法一: 通过GUI界面（推荐）

1. **打开启动器**
   - 双击 `2.GUI启动器.bat`

2. **进入环境检测**
   - 点击左侧导航栏的 "🔍 环境检测"

3. **查看GPU信息**
   - 系统会自动检测所有可用的NVIDIA GPU
   - 显示每张卡的: 名称、显存大小、计算能力

4. **选择GPU设备**
   - 如果检测到多个GPU，会显示"GPU设备选择"卡片
   - 在下拉框中选择:
     - 🌐 **使用所有 GPU**: 默认模式，WebUI可以看到所有显卡
     - 🔹 **GPU 0: XXXX (XX GB, CC X.X)**: 只使用指定的某张显卡

5. **自动保存**
   - 选择后配置会自动保存到 `config.json`
   - 无需手动点击保存按钮

6. **重启生效**
   - 如果WebUI正在运行，需要先停止
   - 重新启动WebUI，新的GPU设置才会生效

### 方法二: 手动编辑配置文件

1. 打开 `config.json` 文件
2. 找到或添加 `"gpu_device"` 字段:
   ```json
   {
     "gpu_device": "0",  // 使用GPU 0
     // 其他配置...
   }
   ```
3. 可选值:
   - `""` (空字符串): 使用所有GPU（默认）
   - `"0"`: 只使用GPU 0
   - `"1"`: 只使用GPU 1
   - `"0,1"`: 同时使用GPU 0和1（多卡并行）

## 💡 技术原理

### CUDA_VISIBLE_DEVICES 环境变量

启动器通过设置Windows环境变量 `CUDA_VISIBLE_DEVICES` 来控制PyTorch可见的GPU设备：

```batch
set CUDA_VISIBLE_DEVICES=0    # WebUI只能看到GPU 0
set CUDA_VISIBLE_DEVICES=1    # WebUI只能看到GPU 1
不设置                        # WebUI可以看到所有GPU
```

### 工作流程

```
用户选择GPU → 保存到config.json → 启动时读取配置 
→ 生成bat脚本(set CUDA_VISIBLE_DEVICES=X) 
→ WebUI进程继承环境变量 → PyTorch只看到指定GPU
```

## 📊 验证是否生效

### 方法一: 查看启动日志

启动WebUI后，在控制台日志中查找:

```
Device: cuda:0
GPU: NVIDIA GeForce RTX 4090
```

如果只显示一张卡的信息，说明切换成功。

### 方法二: Python代码验证

在WebUI的控制台中执行:

```python
import torch
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"可见GPU数量: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

预期输出（选择GPU 0后）:
```
CUDA可用: True
可见GPU数量: 1
GPU 0: NVIDIA GeForce RTX 4090
```

### 方法三: 任务管理器

1. 打开Windows任务管理器 → 性能标签
2. 查看GPU 0和GPU 1的占用率
3. 生成图像时，只有被选中的GPU会有负载

## ⚠️ 注意事项

### 1. 必须重启WebUI

- 切换GPU后，**必须停止并重新启动WebUI**才能生效
- 运行时修改配置不会影响当前进程

### 2. 显存限制

- 选择的GPU必须有足够显存运行模型
- SDXL/Flux等大模型需要12GB+显存
- 如果显存不足，会报错: `CUDA out of memory`

### 3. 多卡并行训练

- 如果要使用多卡并行训练，选择"使用所有GPU"
- 或在配置文件中设置: `"gpu_device": "0,1"`

### 4. 笔记本双显卡

- 很多笔记本有集显(Intel) + 独显(NVIDIA)
- PyTorch通常自动使用独显，无需手动切换
- 如果发现使用了集显，强制选择NVIDIA GPU的ID

### 5. AMD/Intel显卡

- 本功能仅适用于NVIDIA CUDA GPU
- AMD显卡使用DirectML，不支持CUDA_VISIBLE_DEVICES
- Intel显卡使用IPEX，有独立的设备选择机制

## 🛠️ 故障排查

### 问题1: 下拉框没有显示

**原因**: 系统只有一个GPU或未检测到CUDA

**解决**:
```bash
# 在命令行检查
nvidia-smi
python -c "import torch; print(torch.cuda.device_count())"
```

### 问题2: 切换后仍然使用错误的GPU

**原因**: WebUI未重启或配置未保存

**解决**:
1. 确认config.json中gpu_device字段已更新
2. 完全停止WebUI进程
3. 重新启动WebUI

### 问题3: 提示"CUDA out of memory"

**原因**: 选择的GPU显存不足

**解决**:
1. 切换到显存更大的GPU
2. 启用medvram/lowvram模式
3. 降低图像分辨率或批次大小

### 问题4: 想恢复默认设置

**解决**:
- 在GUI中选择"🌐 使用所有 GPU"
- 或删除config.json中的 `"gpu_device"` 字段

## 📝 配置示例

### 单显卡系统（无需配置）
```json
{
  "gpu_device": "",
  "cuda_malloc": true,
  "medvram": false
}
```

### 双显卡 - 使用GPU 0（RTX 4090）
```json
{
  "gpu_device": "0",
  "cuda_malloc": true,
  "medvram": false
}
```

### 双显卡 - 使用GPU 1（RTX 3090）
```json
{
  "gpu_device": "1",
  "cuda_malloc": true,
  "lowvram": true
}
```

### 多卡并行训练
```json
{
  "gpu_device": "0,1",
  "cuda_malloc": true,
  "medvram": false
}
```

## 🎓 进阶知识

### GPU ID编号规则

- GPU ID从0开始编号
- 编号顺序由系统决定，不一定是性能排序
- 可通过 `nvidia-smi` 查看对应关系

```
nvidia-smi
+-----------------------------------------------------------------------------+
| GPU  Name        | Memory-Usage | GPU-Util |
|   0  RTX 4090    |  24576 MiB   |    0%    |
|   1  RTX 3090    |  24576 MiB   |    0%    |
+-----------------------------------------------------------------------------+
```

### CUDA计算能力(Compute Capability)

- CC 8.9: RTX 40系列 (Ada Lovelace)
- CC 8.6: RTX 30系列 (Ampere)
- CC 7.5: RTX 20系列 (Turing)
- 更高CC = 更新的架构 = 更好的性能和新特性

### xFormers兼容性

新一代GPU（CC > 9.0，如RTX 50系列）可能不兼容当前版本的xFormers：
- 症状: `NotImplementedError: memory_efficient_attention`
- 解决: 在参数设置中勾选"禁用xFormers"

## 🔗 相关文档

- [NVIDIA CUDA文档](https://docs.nvidia.com/cuda/)
- [PyTorch多GPU教程](https://pytorch.org/tutorials/beginner/blitz/data_parallel_tutorial.html)
- [Stable Diffusion WebUI Wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki)

## ❓ 常见问题

**Q: 可以同时使用两张卡加速生成吗？**  
A: 标准txt2img/img2img不支持多卡并行。多卡主要用于训练或批量处理。

**Q: 切换GPU会影响已生成的图片吗？**  
A: 不会。只影响新生成的图片使用的硬件设备。

**Q: 为什么我的笔记本只有一个GPU选项？**  
A: 可能另一张是集成显卡（Intel HD Graphics），PyTorch无法直接使用。

**Q: 可以动态切换GPU而不重启吗？**  
A: 不可以。CUDA上下文在进程启动时创建，必须重启进程才能切换。

---

**技术支持**: 如遇问题，请提供:
1. 系统GPU配置 (`nvidia-smi` 输出)
2. config.json内容
3. WebUI启动日志
4. 具体的错误信息
