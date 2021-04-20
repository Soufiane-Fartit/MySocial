from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Relations, Post, Likes, Comment
from .. import db

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
@login_required
def Index():
    from sqlalchemy import desc, Date, cast
    from datetime import date

    current_user_friends_id_list = [x.user2_id for x in Relations.query.filter(Relations.user1_id==current_user.id).all()] \
                                 + [x.user1_id for x in Relations.query.filter(Relations.user2_id==current_user.id).all()]
    posts = sum([Post.query.filter(Post.user_id==friend_id)\
                            .filter(Post.date==date.today().strftime("%d/%m/%Y"))\
                            .order_by(desc('id'))\
                            .all() \
                for friend_id in current_user_friends_id_list], [])
    for post in posts:
        post.user_name = " ".join([User.query.get(post.user_id).first_name, User.query.get(post.user_id).last_name])
        post.user_image = User.query.get(post.user_id).picture_path
    return render_template('main/home.html',
                        connected_id=current_user.id,
                        connected_user=User.query.get(current_user.id),
                        data={'posts':posts
                        })

@main.route('/like', methods=['GET', 'POST'])
@login_required
def receiveLike():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = current_user.id
        # check if post already liked by user
        x = Likes.query.filter(Likes.post_id==post_id, Likes.user_id==user_id).first()
        if x :
            # delete from table
            db.session.delete(x)
            # update post attributes
            post = Post.query.get(post_id)
            post.total_likes -= 1
            db.session.commit()
        else :
            # add to table
            new_like = Likes(post_id, user_id)
            # update post attributes
            post = Post.query.get(post_id)
            post.total_views += 1
            post.total_likes += 1
            db.session.add(new_like)
            # commit
            db.session.commit()
    print('done')
    return redirect(url_for('profile.Profile', id=1))


@main.route('/comment', methods=['GET', 'POST'])
@login_required
def receiveComment():
    if request.method == 'POST':
        post_id = request.form['post_id']
        text = request.form['text']
        user_id = current_user.id
        new_comment = Comment(post_id, user_id, text)
        db.session.add(new_comment)
        # update post attributes
        post = Post.query.get(post_id)
        post.total_comments += 1
        # commit
        db.session.commit()
    return redirect(url_for('profile.Profile', id=id))

@main.route('/newpost', methods=['GET', 'POST'])
@login_required
def receiveNewPost():
    if request.method == 'POST':
        text = request.form['text']
        user_id = current_user.id
        new_post = Post(user_id=user_id, text=text)
        db.session.add(new_post)
        print('received new comment', text, 'by user : ', user_id)
        # commit
        db.session.commit()
    return redirect(url_for('profile.Profile', id=id))

@main.route('/sharepost', methods=['GET', 'POST'])
@login_required
def sharePost():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = current_user.id
        post = Post.query.get(post_id)
        new_post = Post(user_id=user_id, text=post.text)
        db.session.add(new_post)
        # commit
        db.session.commit()
    return redirect(url_for('profile.Profile', id=id))

@main.route('/deletepost', methods=['GET', 'POST'])
@login_required
def deletePost():
    if request.method == 'POST':
        post_id = request.form['post_id']
        post = Post.query.get(post_id)
        db.session.delete(post)
        # commit
        db.session.commit()
    print('deleted')
    return redirect(url_for('profile.Profile', id=current_user.id))
