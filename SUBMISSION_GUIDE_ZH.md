# 四季网站提交说明

这份说明帮助你把当前项目上传 GitHub、获得公网演示链接，并整理老师要求的提交内容。

## 当前已经完成的内容

- 纯 Python、HTML、CSS、JavaScript 网站
- 四季首页与四个独立季节页面
- 响应式桌面和手机布局
- 键盘与触摸交互
- 6 项自动化测试
- 英文项目报告、Word 版和 PDF 版
- 首页、四季页面和手机页面截图
- 源码压缩包

## 一 上传到 GitHub

当前电脑没有安装 Git，最简单的方法是用 GitHub Desktop。

1. 注册或登录 GitHub。
2. 安装 GitHub Desktop。
3. 在 GitHub Desktop 选择 `File > Add local repository`。
4. 选择 `four-seasons-china` 文件夹。
5. 如果提示该文件夹不是 Git 仓库，选择创建仓库。
6. 仓库名称建议填写 `four-seasons-across-china`。
7. 提交说明填写 `Complete four seasons web technologies project`。
8. 点击 `Publish repository`。

上传时不要包含 `.venv` 文件夹。项目里的 `.gitignore` 已经会忽略它。

如果使用 GitHub 网页上传：

1. 新建一个空仓库。
2. 只把 `app.py`、`templates`、`static`、`tests`、`previews`、`.gitignore`、`README.md`、`render.yaml`、报告文件上传。
3. 不要上传 `.venv` 和 `__pycache__`。

## 二 部署公开演示链接

推荐使用 Render，因为项目已经提供 `render.yaml`。

1. 登录 Render。
2. 新建 Web Service。
3. 连接刚才的 GitHub 仓库。
4. Runtime 选择 Python。
5. Build Command 留空。
6. Start Command 填写 `python app.py`。
7. 创建服务，等待部署完成。
8. 打开 Render 提供的公网地址，检查首页和四个季节页。

如果部署平台要求安装命令，可以填写：

```text
python -m pip install --upgrade pip
```

不要填写 Flask、Gunicorn 或其他依赖，因为网站不需要它们。

## 三 老师要求的三个提交内容

1. 文本内容：提交 `Project_Report.docx`，也可以同时提交 `Project_Report.pdf`。
2. GitHub 链接：提交 GitHub 仓库主页地址。
3. 项目演示链接：提交 Render 生成的公网地址。

提交前打开演示链接，检查：

- 首页四张图片正常显示
- 四张图片都能进入对应季节页面
- 名言和作者正确显示
- 上一页和下一页能切换
- 手机宽度下没有横向滚动

## 四 图片说明

网站图片由你提供。公开上传前需要确认这些图片允许用于课程展示。如果图片来自网络，最好保留原始页面链接或摄影师署名；如果无法确认授权，建议替换成 Wikimedia Commons、Pixabay 或自己拍摄的图片。

