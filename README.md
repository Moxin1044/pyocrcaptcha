# pyocrcaptcha

基于 YOLO 的图片验证码 OCR Python 包。安装后既可以作为对象调用，也可以直接使用命令行识别图片。

## 安装

```bash
pip install pyocrcaptcha
```

从源码安装：

```bash
git clone https://github.com/Moxin1044/pyocrcaptcha.git
cd pyocrcaptcha
pip install .
```

## 命令行

自动判断 4 位或 5 位验证码：

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
- 图片字符必须是等宽排列；自动模式会分别尝试 4 位和 5 位并选择平均置信度较高的结果。
- 当前模型验证集单字符 Top-1 为 83.23%，Top-5 为 94.59%。整串完全正确率会低于单字符准确率。
- 仅供学习与研究使用，请遵守验证码来源网站的服务条款和适用法律法规。
