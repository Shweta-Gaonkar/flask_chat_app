
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = []

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/chat')
def chat():
    username = request.args.get("username")
    room = request.args.get("room")
    return render_template('chat.html', username=username, room=room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{username} has joined the room."}, room=room)

@socketio.on('send_message')
def handle_message(data):
    timestamp = datetime.now().strftime('%H:%M:%S')
    emit('message', {
        'msg': f"[{timestamp}] {data['username']}: {data['message']}"
    }, room=data['room'])

@socketio.on('create_room')
def create_room(data):
    room = data['room']
    if room not in rooms:
        rooms.append(room)
        emit('room_created', {'room': room}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
