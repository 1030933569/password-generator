# 🔐 动态密码生成器 Web 版

基于 SHA256 + Base64 双重加密的动态密码生成系统，支持部署到 Vercel 等静态托管平台，国内可访问。

## ✨ 功能特点

- 🎯 **今日密码**：自动生成当天的8位密码
- 📅 **自定义日期**：查询任意日期的密码
- 📊 **本周密码**：一键生成未来7天的密码列表
- 📋 **一键复制**：快速复制密码到剪贴板
- 📱 **响应式设计**：完美支持手机、平板、电脑
- 🚀 **纯前端实现**：无需服务器，加载速度快
- 🔒 **安全加密**：SHA256 + Base64 双重加密算法

## 🌐 在线部署

### 方案一：Vercel 部署（推荐）

Vercel 是一个免费的静态网站托管平台，在国内可以访问（使用香港节点）。

#### 步骤：

1. **注册 Vercel 账号**
   - 访问 https://vercel.com
   - 使用 GitHub/GitLab/Bitbucket 账号登录

2. **上传代码到 GitHub**
   ```bash
   cd password-web
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/你的用户名/password-web.git
   git push -u origin main
   ```

3. **在 Vercel 导入项目**
   - 登录 Vercel 后，点击 "Add New" → "Project"
   - 选择你的 GitHub 仓库 `password-web`
   - 点击 "Import"
   - 保持默认设置，点击 "Deploy"

4. **等待部署完成**
   - 部署通常需要 1-2 分钟
   - 完成后会自动分配一个域名，如：`your-project.vercel.app`

5. **访问网站**
   - 直接访问分配的域名即可使用

#### 自定义域名（可选）：

在 Vercel 项目设置中可以绑定自己的域名。

### 方案二：Netlify 部署

Netlify 也是一个免费的静态托管平台。

1. 访问 https://netlify.com
2. 注册并登录
3. 拖拽 `password-web` 文件夹到 Netlify 的部署区域
4. 等待部署完成

### 方案三：GitHub Pages 部署

1. 在 GitHub 创建仓库 `password-web`
2. 上传所有文件到仓库
3. 在仓库设置中启用 GitHub Pages
4. 选择 `main` 分支作为源
5. 访问 `https://你的用户名.github.io/password-web`

### 方案四：本地运行

如果只是临时使用，可以直接在本地打开：

```bash
# 在 password-web 目录下
# 方法1：直接双击 index.html
# 方法2：使用 Python 启动简单服务器
python -m http.server 8000

# 然后访问 http://localhost:8000
```

## 📁 项目结构

```
password-web/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # JavaScript 逻辑
├── vercel.json         # Vercel 配置
├── .vercelignore       # Vercel 忽略文件
└── README.md           # 说明文档
```

## 🔧 技术实现

### 密码生成算法

```javascript
1. 输入：月份 + 日期
2. 组合：dateNum = month * 100 + day
3. 拼接：raw = dateNum + SECRET_KEY
4. SHA256 哈希：hash = SHA256(raw)
5. Base64 编码：encoded = Base64(hash)
6. 清理字符：去除 O/0/I/l/1 等易混淆字符
7. 输出：取前8位并转大写
```

### 关键代码

```javascript
async function generatePassword(month, day) {
    const dateNum = month * 100 + day;
    const raw = `${dateNum}${SECRET_KEY}`;
    
    // SHA256 哈希
    const encoder = new TextEncoder();
    const data = encoder.encode(raw);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    
    // 转换为 Base64
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashBase64 = btoa(String.fromCharCode.apply(null, hashArray));
    
    // 提取8位密码
    const cleanChars = hashBase64.replace(/[^a-zA-Z0-9]/g, '')
                                  .replace(/[O0Il1]/g, '')
                                  .toUpperCase();
    
    return cleanChars.substring(0, 8);
}
```

## 🔑 修改密钥

如果需要修改密钥，请同时修改：

1. **前端代码** (`script.js` 第2行)：
   ```javascript
   const SECRET_KEY = "你的新密钥";
   ```

2. **后端代码** (`Ui_py/password_generator.py` 第18行)：
   ```python
   SECRET_KEY = "你的新密钥"
   ```

⚠️ **重要**：前后端密钥必须完全一致，否则生成的密码会不匹配！

## 🛡️ 安全建议

1. ✅ 建议修改默认的 `SECRET_KEY`
2. ✅ 不要将密钥提交到公开的 Git 仓库
3. ✅ 部署后可以设置访问密码保护（Vercel 支持）
4. ✅ 定期更换密钥并通知相关人员
5. ✅ 只分享给需要的管理员

## 📱 使用说明

### 1. 查看今日密码
- 页面加载后自动显示今日密码
- 点击 "🔄 刷新今日密码" 可重新生成

### 2. 生成指定日期密码
- 输入月份（1-12）和日期（1-31）
- 点击 "🔍 生成密码"
- 点击密码旁的 📋 图标可复制

### 3. 查看本周密码
- 点击 "📈 生成本周密码"
- 显示未来7天的密码列表

## 🌍 国内访问优化

### Vercel 节点选择

项目配置使用香港和新加坡节点（`vercel.json`）：
```json
"regions": ["hkg1", "sin1"]
```

这确保了国内用户的访问速度。

### 备选方案

如果 Vercel 访问不稳定，可以考虑：
1. **Cloudflare Pages**（免费，速度快）
2. **腾讯云静态托管**（国内服务器）
3. **阿里云 OSS 静态网站**（国内服务器）

## 🐛 故障排除

### 密码不匹配
- 检查前后端 `SECRET_KEY` 是否一致
- 确认日期格式正确

### 复制功能不工作
- 确保浏览器支持剪贴板 API
- 使用 HTTPS 协议访问（Vercel 自动提供）

### 样式显示异常
- 清除浏览器缓存
- 确保 `styles.css` 正确加载

## 📞 技术支持

如有问题，请检查：
1. 浏览器控制台（F12）查看错误信息
2. 确认所有文件都已正确上传
3. 验证密钥配置是否正确

## 📄 许可证

本项目仅供内部使用，请勿公开分享或用于商业用途。

## 🔄 更新日志

### v1.0.0 (2025-12-02)
- ✨ 初始版本发布
- ✨ 支持今日密码、自定义日期、本周密码
- ✨ 完整的响应式设计
- ✨ 一键复制功能
- ✨ Vercel 部署支持

---

**⚠️ 警告**：请妥善保管此系统，不要泄露给非管理员！修改密钥后需要同时更新客户端代码。