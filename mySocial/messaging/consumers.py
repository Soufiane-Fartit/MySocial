import json
from flask_socketio import emit
from flask_login import current_user
from .. import socketio
from ..models import Message

@socketio.on('message', namespace='/newmesagesocket')
def text(message):
    msg = message['msg']
    receiver_id = message['receiver_id']
    new_message = Message(current_user.id,receiver_id,msg)
    # print(msg, receiver_id)
    emit('message', {'msg': {c.name: getattr(new_message, c.name) for c in new_message.__table__.columns}}, broadcast=True, include_self=False)


@socketio.on('videocall', namespace='/videocall')
def videocall(message):
    # print('sending videocall request')
    emit('call', {'msg': {'user': {c.name: getattr(current_user, c.name) for c in current_user.__table__.columns}}}, broadcast=True, include_self=False)