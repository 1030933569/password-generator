# 🚀 快速部署指南

## 方法一：Vercel 部署（最推荐，国内可访问）

### 准备工作
1. 注册 GitHub 账号（如果没有）：https://github.com
2. 注册 Vercel 账号（使用 GitHub 登录）：https://vercel.com

### 部署步骤

#### 1️⃣ 上传代码到 GitHub

```bash
# 进入项目目录
cd password-web

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "动态密码生成器首次提交"

# 在 GitHub 创建新仓库（password-web），然后执行：
git branch -M main
git remote add origin https://github.com/你的用户名/password-web.git
git push -u origin main
```

#### 2️⃣ 在 Vercel 部署

1. 访问 https://vercel.com 并登录
2. 点击 **"Add New"** → **"Project"**
3. 点击 **"Import Git Repository"**
4. 选择你的 `password-web` 仓库
5. 点击 **"Import"**
6. 保持默认设置，直接点击 **"Deploy"**
7. 等待 1-2 分钟，部署完成！

#### 3️⃣ 访问网站

部署完成后，Vercel 会自动分配一个域名：
- 默认域名：`your-project-xxxxx.vercel.app`
- 这个域名在国内可以正常访问！

### 自定义域名（可选）

1. 在 Vercel 项目中点击 **"Settings"** → **"Domains"**
2. 输入你的域名（例如：`password.yourdomain.com`）
3. 按照提示在域名服务商处添加 DNS 记录
4. 等待 DNS 生效（通常几分钟）

---

## 方法二：Netlify 部署（同样免费）

### 拖拽部署（最简单）

1. 访问 https://app.netlify.com/drop
2. 直接拖拽整个 `password-web` 文件夹到页面上
3. 等待上传和部署完成
4. 获得域名：`random-name.netlify.app`

### 通过 Git 部署

1. 登录 https://netlify.com
2. 点击 **"Add new site"** → **"Import an existing project"**
3. 选择 GitHub 并授权
4. 选择 `password-web` 仓库
5. 点击 **"Deploy site"**

---

## 方法三：GitHub Pages 部署（完全免费）

### 步骤：

1. 在 GitHub 创建仓库 `password-web`
2. 上传所有文件
3. 进入仓库的 **Settings** → **Pages**
4. Source 选择 **"Deploy from a branch"**
5. Branch 选择 **"main"** 和 **"/ (root)"**
6. 点击 **Save**
7. 等待几分钟后访问：`https://你的用户名.github.io/password-web`

⚠️ **注意**：GitHub Pages 在国内访问可能较慢。

---

## 方法四：本地运行（无需部署）

### 方式 1：直接打开
双击 `index.html` 文件即可在浏览器中打开

### 方式 2：本地服务器
```bash
# 进入项目目录
cd password-web

# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# 然后访问：http://localhost:8000
```

### 方式 3：使用 VS Code
1. 安装 "Live Server" 插件
2. 右键 `index.html` → "Open with Live Server"

---

## 国内访问优化建议

### 1. Vercel 区域设置
已在 `vercel.json` 中配置使用香港和新加坡节点：
```json
"regions": ["hkg1", "sin1"]
```

### 2. 备用国内平台

如果 Vercel 访问不稳定，可以使用：

#### 腾讯云 CloudBase（国内服务器）
1. 访问 https://cloud.tencent.com/product/tcb
2. 创建静态网站托管
3. 上传文件

#### 阿里云 OSS（国内服务器）
1. 开通 OSS 服务
2. 创建 Bucket
3. 启用静态网站托管
4. 上传文件

---

## 部署后验证

访问网站后，检查以下功能：

- ✅ 页面正常加载，样式显示正确
- ✅ 自动显示今日密码
- ✅ 可以生成自定义日期的密码
- ✅ 可以生成本周密码列表
- ✅ 复制功能正常工作

---

## 常见问题

### Q: 密码与客户端不匹配？
A: 检查 `script.js` 中的 `SECRET_KEY` 是否与后端 Python 文件一致

### Q: 样式显示异常？
A: 清除浏览器缓存，或使用无痕模式访问

### Q: 在国内访问很慢？
A: 
1. 使用 Vercel 时确保配置了 `hkg1` 或 `sin1` 区域
2. 或改用国内的托管平台（腾讯云、阿里云）

### Q: 如何保护网站不被他人访问？
A: 
1. Vercel Pro 版支持密码保护
2. 使用 Cloudflare 添加访问限制
3. 或者不公开域名，只分享给需要的人

---

## 更新网站

### 如果使用 Git 部署（Vercel/Netlify/GitHub Pages）：

```bash
# 修改代码后
git add .
git commit -m "更新说明"
git push

# Vercel/Netlify 会自动重新部署
# GitHub Pages 可能需要等待几分钟
```

### 如果使用拖拽部署（Netlify）：

重新拖拽文件夹即可（会覆盖旧版本）

---

## 安全提醒

✅ **推荐做法**：
- 修改默认的 `SECRET_KEY`
- 不要将密钥提交到公开仓库
- 使用私有仓库（GitHub 支持）
- 定期更换密钥

❌ **避免**：
- 在公开场合分享网址
- 将密钥写在代码注释中
- 使用过于简单的密钥

---

需要帮助？检查 `README.md` 获取更多技术细节。