# Docker 部署指南

## 快速开始

```bash
# 构建镜像
docker build -t password-generator .

# 运行：将容器 80 端口映射到本机 8080
docker run --rm -p 8080:80 password-generator
```

浏览器访问 http://localhost:8080 即可看到页面。

## 常用变体

- 前台查看日志：默认即前台运行，可按 Ctrl+C 退出并删除容器。
- 后台运行：`docker run -d --name password-generator -p 8080:80 password-generator`
- 更换端口：把 `8080:80` 改成你需要的主机端口，例如 `3000:80`。
- 自定义镜像名：构建时替换 `-t password-generator`，运行时保持一致。
