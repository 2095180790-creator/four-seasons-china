# 四季网站提交说明

这份说明用于上传 GitHub、生成 GitHub Pages 演示链接，并准备老师要求的材料。

## 老师要求的材料

1. 文本内容
2. GitHub 链接
3. Live link
4. 5 张项目图片

## 已经完成

- 纯 Python、HTML、CSS、JavaScript 网站
- GitHub 公开仓库
- 英文项目报告 PDF 和 Word
- 可以直接粘贴的英文项目简介
- 首页、春、夏、秋、冬共 5 张截图
- 11 项自动化测试
- PythonAnywhere WSGI 入口文件
- GitHub Pages 静态演示文件

## 一 发布最新代码到 GitHub

项目已经包含 `docs/` 目录，GitHub Pages 可以直接把它发布成网站。

在 GitHub Desktop 中：

1. 打开 `four-seasons-china` 仓库。
2. 左侧 Changes 会显示新增或修改的文件。
3. Summary 填写 `Add GitHub Pages and PythonAnywhere support`。
4. 点击 `Commit to main`。
5. 点击 `Push origin`。

## 二 开启 GitHub Pages

1. 打开 https://github.com/2095180790-creator/four-seasons-china/settings/pages
2. 在 `Build and deployment` 中把 Source 设为 `Deploy from a branch`。
3. Branch 选择 `main`。
4. Folder 选择 `/docs`。
5. 点击 `Save`。
6. 等待 1 到 5 分钟并刷新页面。

Live link 将是：

```text
https://2095180790-creator.github.io/four-seasons-china/
```

这个免费演示链接只能运行 HTML、CSS 和 JavaScript。完整 Python 源码仍保存在 GitHub 仓库中，老师可以查看和下载。

## 三 PythonAnywhere 备用方案

如果需要让在线网站真正运行 Python，可以使用 PythonAnywhere。它通常不需要银行卡。

1. 打开 https://www.pythonanywhere.com/registration/register/beginner/
2. 创建一个 Free Beginner 账户。
3. 不需要银行卡。
4. 不要向任何人发送密码。

免费账户注册后，你的演示地址通常是：

```text
https://你的用户名.pythonanywhere.com
```

### 上传网站

最简单的方法是从公开 GitHub 仓库下载到 PythonAnywhere。

1. 登录 PythonAnywhere。
2. 点击 `Consoles` -> `Bash`。
3. 在 Bash 中运行：

```bash
git clone https://github.com/2095180790-creator/four-seasons-china.git
```

4. 运行下面的命令，把项目放进 PythonAnywhere 默认网站目录：

```bash
cp -r four-seasons-china/* mysite/
cp four-seasons-china/.gitignore mysite/
cd mysite
python -m unittest discover -s tests -v
```

### 创建 Web App

1. 点击 `Web`。
2. 点击 `Add a new web app`。
3. 选择合适的 Python 3 版本。
4. 选择 `Manual configuration`，不要选择 Flask 或 Django。
5. Source code 填写：

```text
/home/你的用户名/mysite
```

6. Working directory 填写：

```text
/home/你的用户名/mysite
```

### 配置 WSGI 文件

1. 在 Web 页面点击 `WSGI configuration file`。
2. 删除文件中的默认内容。
3. 写入以下代码，并把用户名改成你的 PythonAnywhere 用户名：

```python
import sys

project_path = "/home/你的用户名/mysite"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from pythonanywhere_wsgi import application
```

4. 保存文件。
5. 返回 Web 页面，点击绿色 `Reload` 按钮。
6. 打开 `https://你的用户名.pythonanywhere.com`。

### 设置静态图片目录

如果页面文字正常但图片没有显示：

1. 在 Web 页面找到 `Static files`。
2. URL 填写 `/static/`。
3. Directory 填写：

```text
/home/你的用户名/mysite/static
```

4. 点击保存并 Reload。

## 四 提交前检查

打开在线演示链接，依次检查：

- 首页四张图片显示
- Spring 页面打开
- Summer 页面打开
- Autumn 页面打开
- Winter 页面打开
- 名言和作者显示
- Previous 与 Next 可以切换

## 提交内容

- GitHub：https://github.com/2095180790-creator/four-seasons-china
- Live link：优先填写 `https://2095180790-creator.github.io/four-seasons-china/`
- 5 张图片：`outputs/submission-images`
- 文本：`Project_Report.pdf`
