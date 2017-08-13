from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret secret.'
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('connect')
def handle_connect():
	print('Client connected')
	emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
	print('Client disconnected')

@socketio.on('my event')
def handle_my_event(msg):
	emit('my response', {'data': msg['data']})

@socketio.on('my broadcast event')
def handle_my_broadcast_event(msg):
	emit('my response', {'data': msg['data']}, broadcast=True)

@socketio.on('join')
def handle_join(message):
	join_room(message['room'])

	emit('my response', {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('leave')
def handle_leave(message):
	leave_room(message['room'])

	emit('my response', {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('send_room')
def handle_send_room(message):
	emit('my response', {'data': message['data']}, room=message['room'])

@socketio.on('close_room')
def handle_close_room(message):
	emit('my response', {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
	close_room(message['room'])

if __name__ == '__main__':
	socketio.run(app)