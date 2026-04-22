#!/bin/bash
# 服务器部署脚本 - Luvoy 职业规划平台
# 服务器: 8.147.129.14
# 用途: 一键部署前端 + 后端

set -e

echo "======================================"
echo "  律途 Luvoy 部署脚本"
echo "======================================"

# 配置变量
APP_DIR="/opt/luvoy"
FRONTEND_DIR="$APP_DIR/frontend"
BACKEND_DIR="$APP_DIR/backend"

# 1. 安装系统依赖
echo "[1/7] 安装系统依赖..."
apt-get update
apt-get install -y nginx python3 python3-pip python3-venv unzip curl

# 2. 创建应用目录
echo "[2/7] 创建应用目录..."
mkdir -p $APP_DIR
mkdir -p $FRONTEND_DIR
mkdir -p $BACKEND_DIR

# 3. 解压上传的文件（假设已上传 Luvoy.zip 到 /tmp）
echo "[3/7] 解压项目文件..."
cd /tmp
if [ -f "Luvoy.zip" ]; then
    unzip -o Luvoy.zip -d /tmp/luvoy-temp
    # 复制前端 dist
    cp -r /tmp/luvoy-temp/Luvoy/frontend/dist/* $FRONTEND_DIR/
    # 复制后端
    cp -r /tmp/luvoy-temp/Luvoy/backend/* $BACKEND_DIR/
    rm -rf /tmp/luvoy-temp
else
    echo "错误: 未找到 /tmp/Luvoy.zip"
    exit 1
fi

# 4. 配置后端 Python 环境
echo "[4/7] 配置后端 Python 环境..."
cd $BACKEND_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. 创建后端 systemd 服务
echo "[5/7] 创建后端服务..."
cat > /etc/systemd/system/luvoy-backend.service << 'EOF'
[Unit]
Description=Luvoy Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/luvoy/backend
Environment=FLASK_APP=app.py
Environment=FLASK_ENV=production
ExecStart=/opt/luvoy/backend/venv/bin/python -m flask run --host=0.0.0.0 --port=5000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable luvoy-backend
systemctl restart luvoy-backend

# 6. 配置 Nginx
echo "[6/7] 配置 Nginx..."
cat > /etc/nginx/sites-available/luvoy << 'EOF'
server {
    listen 80;
    server_name _;
    
    # 前端静态文件
    root /opt/luvoy/frontend;
    index index.html;
    
    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
    
    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/luvoy /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试并重启 Nginx
nginx -t && systemctl restart nginx

# 7. 防火墙配置
echo "[7/7] 配置防火墙..."
ufw allow 80/tcp 2>/dev/null || true
ufw allow 443/tcp 2>/dev/null || true

echo ""
echo "======================================"
echo "  部署完成!"
echo "======================================"
echo ""
echo "访问地址: http://$(curl -s ifconfig.me)"
echo "后端服务状态: systemctl status luvoy-backend"
echo "Nginx 状态: systemctl status nginx"
echo ""
