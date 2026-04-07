from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
# 静态文件目录（位于项目根目录下）
static_dir = os.path.join(project_root, '..', 'public')
# 为Vercel部署设置临时instance_path
import tempfile
temp_dir = tempfile.gettempdir()
app = Flask(__name__, static_folder=static_dir, static_url_path='/static', instance_path=temp_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'default_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'app/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
# 静态文件缓存配置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1年

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 添加自定义过滤器：去除HTML标签
def strip_html(value):
    """去除HTML标签，返回纯文本"""
    if value is None:
        return ''
    return re.sub(r'<[^>]+>', '', value)

app.jinja_env.filters['strip_html'] = strip_html

from app.models import Post, Comment
from app.blog.routes import blog
from app.main.routes import main
from app.admin.routes import admin

app.register_blueprint(blog)
app.register_blueprint(main)
app.register_blueprint(admin)