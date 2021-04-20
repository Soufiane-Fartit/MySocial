from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_socketio import emit
from ..models import User, Conversation, Message, Relations
from .. import db
from . import consumers

messaging = Blueprint('messaging', __name__, template_folder='templates')

@messaging.route('/messages/<id>')
@messaging.route('/messages/')
@login_required
def Messages(id=None):
    from sqlalchemy import or_, and_

    friends_id_list = [x.user2_id for x in Relations.query.filter(Relations.user1_id==current_user.id,Relations.status=='done').all()] \
                    + [x.user1_id for x in Relations.query.filter(Relations.user2_id==current_user.id,Relations.status=='done').all()]
    friends_list = [User.query.filter(User.id==x).first() for x in friends_id_list]
    for friend in friends_list:
        conv = Conversation.query.filter(or_(and_(Conversation.user1_id==current_user.id , Conversation.user2_id==friend.id ),
                                            and_(Conversation.user2_id==current_user.id , Conversation.user1_id==friend.id )))\
                                .first()
        if conv :
            friend.conversation_id = conv.id
        else:
            new_conv = Conversation(current_user.id, friend.id)
            db.session.add(new_conv)
            db.session.commit()
            conv = Conversation.query.filter(or_(Conversation.user1_id==current_user.id, Conversation.user1_id==friend.id)).first()
            friend.conversation_id = conv.id

    if id:
        conversation = Message.query.filter(Message.conversation_id==id).all()
        ids = [Conversation.query.get(id).user1_id, Conversation.query.get(id).user2_id]
        current_conv_user = User.query.get([x for x in ids if x!=current_user.id][0])
        return render_template('messaging/conversation.html',
                        connected_id=current_user.id,
                        connected_user=User.query.get(current_user.id),
                        friends=friends_list,
                        current_conv_user=current_conv_user,
                        conversastion_id = id,
                        conversation=conversation)

    return render_template('messaging/conversation.html',
                        connected_id=current_user.id,
                        connected_user=User.query.get(current_user.id),
                        friends=friends_list)


@messaging.route('/newmesage', methods=['POST'])
@login_required
def newMessage():
    message_text = request.form['message']
    receiver_id = request.form['receiver_id']
    # print('sent new message', message_text, 'to ', receiver_id)
    new_message = Message(current_user.id,receiver_id,message_text)
    db.session.add(new_message)
    db.session.commit()
    return ('', 204)

@messaging.route('/videocallroom/<id>')
@login_required
def videocallroom(id):
    return render_template('messaging/videocall.html')