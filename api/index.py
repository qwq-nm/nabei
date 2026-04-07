import os
import sys
import datetime
from flask import send_from_directory

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

# 添加静态文件路由
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('public', path)

# 导入Markdown解析库
import mistune

# 创建Markdown解析器
markdown = mistune.create_markdown()

# 扫描并导入文章
def import_posts():
    with app.app_context():
        from app.models import Post
        
        # 扫描blog文件夹及其子文件夹中的 .txt 和 .md 文件
        blog_dir = 'blog'
        if os.path.exists(blog_dir):
            for root, dirs, files in os.walk(blog_dir):
                # 只处理context文件夹中的文件
                if 'context' in root:
                    for filename in files:
                        # 支持 .txt 和 .md 文件
                        if filename.endswith('.txt') or filename.endswith('.md'):
                            file_path = os.path.join(root, filename)
                            try:
                                # 读取文件内容
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # 解析文件内容
                                lines = content.split('\n')
                                title = ''
                                date_str = ''
                                post_content = ''
                                
                                # 解析标题和日期
                                for i, line in enumerate(lines):
                                    if line.startswith('标题：'):
                                        title = line.replace('标题：', '').strip()
                                    elif line.startswith('日期：'):
                                        date_str = line.replace('日期：', '').strip()
                                    elif line == '':
                                        # 空行之后的内容作为文章正文
                                        post_content = '\n'.join(lines[i+1:])
                                        break
                                
                                # 验证必要信息
                                if not title or not date_str or not post_content:
                                    print(f"跳过文件 {file_path}：缺少必要信息")
                                    continue
                                
                                # 检查文章是否已存在
                                existing_post = Post.query.filter_by(title=title).first()
                                if existing_post:
                                    print(f"跳过文件 {file_path}：文章已存在")
                                    continue
                                
                                # 解析日期
                                try:
                                    date_posted = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    print(f"跳过文件 {file_path}：日期格式错误")
                                    continue
                                
                                # 从文件路径中提取分类信息
                                category = ''
                                # 处理Windows和Unix系统的文件路径
                                if 'blog/' in file_path or 'blog\\' in file_path:
                                    # 替换所有反斜杠为正斜杠
                                    normalized_path = file_path.replace('\\', '/')
                                    category = normalized_path.split('blog/')[1].split('/')[0]
                                
                                # 如果是Markdown文件，将内容转换为HTML
                                if filename.endswith('.md'):
                                    post_content = markdown(post_content)
                                
                                # 创建新文章
                                post = Post(title=title, content=post_content, date_posted=date_posted, category=category)
                                db.session.add(post)
                                db.session.commit()
                                print(f"导入文章：{title} (来自 {file_path}, 分类：{category})")
                                
                            except Exception as e:
                                print(f"处理文件 {file_path} 时出错：{e}")

# 在应用启动时创建数据库表
with app.app_context():
    from app.models import Post, Comment
    try:
        # 先删除所有表，然后重新创建
        db.drop_all()
        db.create_all()
        # 导入文章
        import_posts()
    except Exception as e:
        print(f"数据库操作失败: {e}")
        # 在只读环境中，忽略数据库操作错误
        pass

# 导出Flask应用
app = app