# pdf2text
扫描版pdf 文字识别并自动翻译


#### 依赖
pillow

pytesseract

pdf2image

tqdm

requests


#### 注意
确保
pytesseract
pdf2image 
所依赖软件可用性


#### 配置文件
在config目录下修改config.json
本项目基于百度翻译api，请自行申请并修改下面字段
```python
{
    "app_id": "",    # 百度翻译api获取
    "secret_key": "",    # 百度翻译api获取
    "source_lang": "en",    # 输入文本语言默认英文
    "target_lang": "zh",    # 翻译语言，中文
    "input_dir": "./input",    # pdf文件目录
    "output_image": "./output/image",    # 单页pdf查分路径
    "output_text": "./output/text"    # ocr文本与翻译文本存储路径
}
```
