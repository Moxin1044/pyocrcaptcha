# pyocrcaptcha

基于 YOLO 的图片验证码 OCR Python 包。安装后既可以作为对象调用，也可以直接使用命令行识别图片。

## 安装

```bash
pip install pyocrcaptcha
```

`pip` 会根据包元数据自动安装运行依赖：

- `ultralytics>=8.3.0`
- `Pillow>=10.0.0`
- Ultralytics 的传递依赖，包括 PyTorch、TorchVision、NumPy、OpenCV 等

因此不需要再手动安装 `requirements.txt`。如果需要确认依赖解析结果，可以执行：

```bash
python -m pip show pyocrcaptcha
python -m pip check
```

## 发布到 PyPI

仓库通过 `.github/workflows/workflow.yml` 使用 PyPI Trusted Publishing 发布，不需要保存 API Token。工作流会在发布 GitHub Release 时自动运行，也可以在 GitHub Actions 页面手动运行。

首次发布前，需要在 PyPI 的 Trusted Publisher 设置中填写：

```text
PyPI project name: pyocrcaptcha
Owner: Moxin1044
Repository: pyocrcaptcha
Workflow: workflow.yml
Environment: pypi
```

工作流会拉取 Git LFS 模型、构建 wheel 和 sdist，并确认 wheel 内包含完整模型后再上传。

从源码安装：

```bash
git clone https://github.com/Moxin1044/pyocrcaptcha.git
cd pyocrcaptcha
pip install .
```

模型也可从 [V1.0.0 Release](https://github.com/Moxin1044/pyocrcaptcha/releases/tag/V1.0.0) 单独下载：

[下载 captcha-character-classifier-yolo11n-100e.pt](https://github.com/Moxin1044/pyocrcaptcha/releases/download/V1.0.0/captcha-character-classifier-yolo11n-100e.pt)

## 命令行

自动判断 4 位或 5 位验证码（支持宽度不是 4/5 整数倍的截图）：

```bash
pyocrcaptcha xxx.png
```

强制指定位数并显示置信度：

```bash
pyocrcaptcha xxx.png --positions 4 --details
```

## Python API

```python
from pyocrcaptcha import CaptchaOCR

ocr = CaptchaOCR()
text = ocr("xxx.png")
print(text)
```

获取置信度和逐字符结果：

```python
result = ocr.recognize("xxx.png")
print(result.text)
print(result.confidence)
print(result.character_confidences)
print(result.positions)
```

也可以传入自定义模型、设备或固定长度：

```python
ocr = CaptchaOCR(model="best.pt", positions=4, device="cpu")
print(ocr("four_digit.png"))
```

## 说明

- 默认模型随包发布，支持数字 `0-9` 和大写字母 `A-Z`。
- 图片字符应大致等宽排列；自动模式会分别尝试 4 位和 5 位并选择平均置信度较高的结果。图片带边距、缩放或宽度不是整数倍也可以识别。
- 当前模型验证集单字符 Top-1 为 83.23%，Top-5 为 94.59%。整串完全正确率会低于单字符准确率。
- 仅供学习与研究使用，请遵守验证码来源网站的服务条款和适用法律法规。
