# 天猫商品数据提取工具

鉴于一个网友需求，这是一个用于从天猫商品详情页提取数据的 Python 脚本，通过请求天猫的 API，提取商品的 `vid`（属性值 ID）、`skuid`（SKU ID）、价格、库存状态和属性名称，并将它们配对输出为 JSON 格式。本项目适合需要分析天猫商品数据的开发者。

## 功能

- 从天猫商品详情页的 JSONP API 提取数据。
- 提取以下信息：
  - 商品属性值 ID（`vid`）和 SKU ID（`skuid`）。
  - 每个 SKU 的价格（`priceText`）和库存状态（`quantityText`）。
  - 属性名称（例如颜色分类的名称，如 “K2黑色（INA226 36V）”）。
- 将提取的数据配对，生成包含 `name`、`skuid`、`vid`、`price` 和 `text`（库存状态）的 JSON 数据。
- 输出结果为 JSON 格式，便于后续处理或存储。
- 测试了好几个天猫商品，该脚本都可以成功提取到所需的数据。
- 对于没有`mtopjsonppcdetail2`开头的返回内容，只需替换：`json_text = json.loads(response.text)`

## 依赖

- Python 3.x
- 所需库：
  - `requests`：用于发送 HTTP 请求。
  - `re`：用于正则表达式解析 JSONP 数据。
  - `json`：用于处理 JSON 数据。

安装依赖：
```bash
pip install requests
```


## 使用方法
- 获取登录后的 Cookie
- 天猫的 API 请求需要登录后的 Cookie 来访问完整数据。以下是获取 Cookie 的步骤：

- 打开浏览器（推荐 Chrome 或 Edge），访问天猫商品详情页（如 https://detail.tmall.com/item.htm?id=897269589370 ）。
- 登录你的天猫/淘宝账号。
- 按 F12 打开浏览器开发者工具（或右键点击页面，选择“检查”）。
- 切换到 Network（网络） 面板。
- 刷新页面，找到请求 URL 包含 mtop.taobao.pcdetail.data.get 的请求（通常是 JSONP 请求），例如；https://h5api.m.tmall.com/h5/mtop.taobao.pcdetail.data.get/1.0/?jsv=2.7.5&appKey=12574478&... 或 https://h5api.m.taobao.com/h5/mtop.taobao.pcdetail.data.get/1.0/... 。
- 在请求的 Headers（请求头） 中，找到 Cookie 字段，复制全部 Cookie 值。
- 打开脚本文件（main.py），将以下代码中的 'cookie': '' 替换为复制的 Cookie。
- 保存，找ai给你写一个发送信息的额外函数即可。

## 贡献
- 欢迎提交 issue 或 pull request，分享改进建议或新功能！

## 许可证
- 本项目仅用于学习和研究目的，请遵守天猫的使用条款。数据提取可能涉及法律风险，请确保你的使用符合相关法律法规。