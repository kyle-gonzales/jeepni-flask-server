from flask import Flask, request, session, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "jeepni_by_algofirst_secret_key"
app.config["JSONIFY_MIMETYPE"] = "application/json"
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def home():
    """
    if request.method == "POST":
        id = request.form.get("id")
        # socketio.emit("message", {"data": f": id == {id}"})

        if id not in rooms:
            rooms[id] = {"members": 0}

        session["id"] = id

        return str(id)
    """
    return render_template("index.html")


@socketio.on("connect")
def connect():
    print("\n-----new socket connection:", request.sid, "-----\n")


@socketio.on("join")
def handle_join(room):
    join_room(room)

    session["id"] = room
    print(f"\n-----JOINED ROOM {session.get('id')}------\n")


@socketio.on("leave")
def handle_leave():
    room = session.get("id")
    leave_room(room)

    print(f"\n-----LEAVING ROOM {room}-------\n")


@socketio.on("message")
def handle_message(message):
    print("i got a message", str(message))


@socketio.on("update_location")
def handle_update_location(data):
    room = session.get("id")

    print(f"\n----INCOMING DATA FROM: {data.get('driver_id')}-----")
    print(f"------trying to send only to room: {room}----\n\n")

    driver_id = data.get("driver_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    emit(
        "update_location",
        {
            "driver_id": driver_id,
            "latitude": latitude,
            "longitude": longitude,
        },
        broadcast=True,
        to=room,
        include_self=False,
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port="1234", debug=True)
