import socketio
import time

# Create Socket.IO client
sio = socketio.Client()

# =========================
# Event handlers
# =========================

@sio.event(namespace="/chat")
def connect():
    print("Connected to server")

    # Step 1: Send CONNECTED message
    sio.emit("message", {
        "message": "CONNECTED",
        "user_id": "databricks_sql_test",     
        "chat_session_id": "abc123",
        "history": []
    }, namespace="/chat")

    time.sleep(1)

    # Step 2: Send a query
    sio.emit("message", {
        "message": "total principal by loan status",
        "user_id": "databricks_sql_test",     
        "chat_session_id": "abc123",
        "history": []
    }, namespace="/chat")

@sio.on("message", namespace="/chat")
def on_message(*args):
    """
    Handle server messages.
    *args is used to avoid TypeError if extra args are passed.
    """
    if args:
        data = args[0]  # first argument is the message data
        print("Server response:", data)

@sio.event(namespace="/chat")
def disconnect():
    print("Disconnected from server")


# =========================
# Function to run the client
# =========================
def test_xyz():
    try:
        # Connect to server
        sio.connect("http://localhost:5000/chat", namespaces=["/chat"])
        print("Waiting for messages...")

        # Keep client running to receive messages
        sio.wait()
    except Exception as e:
        print("Error:", e)
    finally:
        # Ensure disconnect in case of error
        if sio.connected:
            sio.disconnect()


# =========================
# Entry point
# ===================
if __name__ == "__main__":
    test_xyz()
