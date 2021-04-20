from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Relations, Post, Likes, Comment
from .. import db

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/newpost', methods=['GET', 'POST'])
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

@profile.route('/deletepost', methods=['GET', 'POST'])
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

@profile.route('/addfriend', methods=['GET', 'POST'])
@login_required
def addFriend():
    if request.method == 'POST':
        user_id = request.form['user_id']
        relation = Relations(current_user.id,user_id, 'pending')
        db.session.add(relation)
        # commit
        db.session.commit()
    print('added friend')
    return redirect(url_for('profile.Profile', id=user_id))

@profile.route('/confirmrelation', methods=['GET', 'POST'])
@login_required
def confirmRelation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        print(user_id)
        relation = Relations.query.filter(Relations.user1_id==user_id, Relations.user2_id==current_user.id).first()
        relation.status = 'done'
        # commit
        db.session.commit()
    print('confirming relation')
    return redirect(url_for('profile.Profile', id=user_id))

@profile.route('/rejectrelation', methods=['GET', 'POST'])
@login_required
def rejectRelation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        print(user_id)
        relation = Relations.query.filter(Relations.user1_id==user_id, Relations.user2_id==current_user.id).first()
        db.session.delete(relation)
        # commit
        db.session.commit()
    print('rejecting relation')
    return redirect(url_for('profile.Profile', id=user_id))

@profile.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editProfile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.city = request.form['city']
        user.age = request.form['age']
        user.bio = request.form['bio']
        user.picture_path = request.form['picture_path']
        db.session.commit()

    return redirect(url_for('profile.Profile', id=1))

@profile.route('/profile/<id>')
@login_required
def Profile(id):
    from sqlalchemy import desc

    user = User.query.get(id)
    if not user:
        return redirect(url_for('main.Index'))
    
    # load posts made by user of page visited
    posts = Post.query.filter(Post.user_id==id).order_by(desc('id')).all()

    # load list of id of friends of user of page visited
    friends_id_list = [x.user2_id for x in Relations.query.filter(Relations.user1_id==id,Relations.status=='done').all()] \
                    + [x.user1_id for x in Relations.query.filter(Relations.user2_id==id,Relations.status=='done').all()]
    # load their profiles
    profile_friends_list = [User.query.filter(User.id==x).first() for x in friends_id_list]

    # load list of id of friends of the logged in user
    current_user_friends_id_list = [x.user2_id for x in Relations.query.filter(Relations.user1_id==current_user.id).all()] \
                                + [x.user1_id for x in Relations.query.filter(Relations.user2_id==current_user.id).all()]

    # check if user logged in is friend with user of page visited
    friendship_check = int(id) in current_user_friends_id_list
    if friendship_check:
        if Relations.query.filter(Relations.user1_id==current_user.id).first() :
            if Relations.query.filter(Relations.user1_id==current_user.id).first().status=='pending':
                relation_status = 'sent'
            else :
                relation_status = 'friends'
        elif Relations.query.filter(Relations.user2_id==current_user.id).first():
            if Relations.query.filter(Relations.user2_id==current_user.id).first().status=='pending':
                relation_status = 'received'
            else :
                relation_status = 'friends'
        else :
            relation_status = 'none'
    else:
        relation_status = 'none'
    
    # check relation between logged in user and friends of user of page visited
    for x in profile_friends_list:
        if x.id != current_user.id:
            if x.id in current_user_friends_id_list :
                x.is_friend = 1
            else :
                x.is_friend = 0
        else:
            x.is_friend = 1

    # check if posts are liked by logged in user
    is_post_liked_by_me = []
    for post in posts:
        liked_by = Likes.query.filter(Likes.post_id==post.id).all()
        if current_user.id in [x.user_id for x in liked_by] :
            post.is_liked_by_me = True
            is_post_liked_by_me.append(True)
        else :
            post.is_liked_by_me = False
            is_post_liked_by_me.append(False)
        #find comments
        comments = Comment.query.filter(Comment.post_id==post.id).all()
        for comment in comments:
            comment.image = User.query.get(comment.user_id).picture_path
            comment.user_name = User.query.get(comment.user_id).first_name +" "+User.query.get(comment.user_id).last_name
        post.comments = comments

    return render_template('profile/profile.html', 
                        id=id,
                        connected_id=current_user.id,
                        connected_user=current_user,
                        friendship_check=friendship_check,
                        relation_status=relation_status,
                        data={
                            'infos':{'name':user.first_name+" "+user.last_name, 'email': user.email, 'phone':user.phone, 'age': user.age, 'city':user.city},
                            'image' :user.picture_path,
                            'bio':user.bio,
                            'posts':[x.__dict__ for x in posts],
                            'friends_list':profile_friends_list
                            })