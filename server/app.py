from flask import Flask, request, render_template
import time

app = Flask(__name__)

devices = {}
gps_data = {}

# -------------------------------
# ESP32 DATA ENDPOINT
# -------------------------------
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    device_id = data["device_id"]

    devices[device_id] = {
        "state": data["state"],
        "voltage": data["voltage"],
        "soc": data["soc"],
        "temperature": data["temperature"],
        "last_seen": time.time()
    }
    return {"message": "BMS updated"}

# -------------------------------
# GPS ENDPOINT (FROM MOBILE)
# -------------------------------
@app.route("/gps", methods=["POST"])
def gps():
    data = request.json
    gps_data["lat"] = data["lat"]
    gps_data["lon"] = data["lon"]
    gps_data["last_seen"] = time.time()
    return {"message": "GPS updated"}

# -------------------------------
# DASHBOARD
# -------------------------------
@app.route("/")
def dashboard():
    now = time.time()
    view = {}

    for dev, d in devices.items():
        view[dev] = {
            **d,
            "status": "ONLINE" if now - d["last_seen"] < 15 else "OFFLINE",
            "last_seen": time.strftime("%H:%M:%S",
                time.localtime(d["last_seen"]))
        }

    return render_template(
        "dashboard.html",
        devices=view,
        gps=gps_data
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
