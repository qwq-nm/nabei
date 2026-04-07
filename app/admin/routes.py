from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import os
import sys
import datetime
from app import app, db
from app.models import Post
from main import import_posts

admin = Blueprint('admin', __name__)

# 管理员密码
ADMIN_PASSWORD = 'Lpzn@061023'

@admin.route('/admin')
def admin_login():
    """管理员登录页面"""
    # 获取所有文章，用于侧边栏显示
    from app.models import Post
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin/login.html', all_posts=all_posts)

@admin.route('/admin/login', methods=['POST'])
def admin_login_post():
    """管理员登录验证"""
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        flash('登录成功！', 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        flash('密码错误，请重试。', 'danger')
        return redirect(url_for('admin.admin_login'))

@admin.route('/admin/logout')
def admin_logout():
    """管理员登出"""
    session.pop('admin_logged_in', None)
    flash('已登出。', 'info')
    return redirect(url_for('main.home'))

@admin.route('/admin/dashboard')
def dashboard():
    """管理员仪表盘"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    # 获取所有文章
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin/dashboard.html', posts=posts, all_posts=all_posts)

@admin.route('/admin/import')
def import_posts_page():
    """导入文章页面"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    # 执行导入文章操作
    import_posts()
    flash('文章导入成功！', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/delete/<int:post_id>')
def delete_post(post_id):
    """删除文章"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    # 获取文章
    post = Post.query.get_or_404(post_id)
    
    # 删除对应分类的context文件夹中的文件
    blog_dir = f'blog/{post.category}/context'
    filename = f'{post.title}.txt'.replace(' ', '_')
    file_path = os.path.join(blog_dir, filename)
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"删除文件 {file_path} 时出错：{e}")
    
    # 从数据库中删除文章
    db.session.delete(post)
    db.session.commit()
    
    flash(f'文章《{post.title}》删除成功！', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    """创建文章"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    # 获取所有文章，用于侧边栏显示
    from app.models import Post
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        category = request.form.get('category')
        date_posted_str = request.form.get('date_posted')
        content = request.form.get('content')
        
        # 验证数据
        if not title or not category or not date_posted_str or not content:
            flash('请填写所有必填字段！', 'danger')
            return redirect(url_for('admin.create_post'))
        
        # 解析日期
        try:
            # 处理datetime-local格式：2026-03-28T12:00
            date_posted_str = date_posted_str.replace('T', ' ')
            date_posted = datetime.datetime.strptime(date_posted_str, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('日期格式错误！', 'danger')
            return redirect(url_for('admin.create_post'))
        
        # 检查文章是否已存在
        existing_post = Post.query.filter_by(title=title).first()
        if existing_post:
            flash('文章标题已存在！', 'danger')
            return redirect(url_for('admin.create_post'))
        
        # 创建新文章
        post = Post(title=title, content=content, date_posted=date_posted, category=category)
        db.session.add(post)
        db.session.commit()
        
        # 同时保存到对应分类的context文件夹
        blog_dir = f'blog/{category}/context'
        if not os.path.exists(blog_dir):
            os.makedirs(blog_dir, exist_ok=True)
        
        # 生成文件名
        filename = f'{title}.txt'.replace(' ', '_')
        file_path = os.path.join(blog_dir, filename)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'标题：{title}\n')
            f.write(f'日期：{date_posted.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
            f.write(content)
        
        flash(f'文章《{title}》创建成功！', 'success')
        # 跳转到新发布的文章页面
        return redirect(url_for('blog.post', post_id=post.id))
    
    # GET请求，显示创建文章页面
    return render_template('admin/create_post.html', all_posts=all_posts)
