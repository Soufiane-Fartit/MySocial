import json
from flask import request
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
    emit('call', 
        {'msg': {'user': {c.name: getattr(current_user, c.name) for c in current_user.__table__.columns}, 'convId':message['convId']}}, 
        broadcast=True, 
        include_self=False)



# WEBRTC

connectedUsers = []
@socketio.on('connect')
def onConnect():
    global connectedUsers
    connectedUsers.append(request.sid)

    otherUsers = [x for x in connectedUsers if x!= request.sid]

    emit('other-users', otherUsers)

@socketio.on('offer')
def onOffer(socketId, description):
    emit('offer', (request.sid, description), room=socketId)

@socketio.on('answer')
def onAnswer(socketId, description):
    emit('answer', description, room=socketId)

@socketio.on('candidate')
def onCandidate(socketId, candidate):
    emit('candidate', candidate, room=socketId)

@socketio.on('disconnect')
def onDisconnect():
    global connectedUsers
    connectedUsers = [x for x in connectedUsers if x!=request.sid]

