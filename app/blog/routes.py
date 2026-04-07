from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.models import Post, Comment
from app.blog.forms import CommentForm

blog = Blueprint('blog', __name__)

@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author_name=form.author_name.data, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('评论发布成功！', 'success')
        return redirect(url_for('blog.post', post_id=post.id))
    # 获取所有文章，用于侧边栏显示
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog/post.html', title=post.title, post=post, form=form, all_posts=all_posts)