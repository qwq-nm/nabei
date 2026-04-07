from flask import render_template, Blueprint, request, redirect, url_for
from ..models import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # 重定向到动画页面
    return redirect(url_for('main.animation'))

@main.route('/animation')
def animation():
    # 显示动画页面
    return render_template('main/animation.html')

@main.route('/home')
def home():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/home.html', posts=posts, all_posts=all_posts, title='首页')

@main.route('/about')
def about():
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/about.html', title='关于', all_posts=all_posts)

@main.route('/web')
def web():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='web').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/web.html', posts=posts, all_posts=all_posts, title='Web')

@main.route('/pwn')
def pwn():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='pwn').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/pwn.html', posts=posts, all_posts=all_posts, title='Pwn')

@main.route('/misc')
def misc():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='misc').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/misc.html', posts=posts, all_posts=all_posts, title='Misc')

@main.route('/crypto')
def crypto():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='crypto').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/crypto.html', posts=posts, all_posts=all_posts, title='Crypto')

@main.route('/reverse')
def reverse():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='reverse').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/reverse.html', posts=posts, all_posts=all_posts, title='Reverse')

@main.route('/算法')
def algorithm():
    # 分页功能，每页显示5篇文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='算法').order_by(Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/algorithm.html', posts=posts, all_posts=all_posts, title='算法')