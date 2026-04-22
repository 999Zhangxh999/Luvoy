#!/usr/bin/env python
"""启动Flask服务器"""
import os
import sys

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.chdir(current_dir)

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
