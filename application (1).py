from flask import Flask, render_template, request, jsonify, redirect, url_for

application = Flask(__name__)

# 저장된 데이터
detections = []
phone_gps_data = []


@application.route('/')
def index():
    """
    루트 페이지: 기기 등록 HTML 렌더링
    """
    return render_template('index.html')


@application.route('/device', methods=['POST'])
def device():
    """
    /device: 기기 번호를 입력받아 device.html로 이동
    """
    device_number = request.form.get('device_number')
    if device_number:
        return render_template('device.html', device_number=device_number)
    else:
        return redirect(url_for('index'))


@application.route('/api/phone-gps', methods=['POST'])
def receive_phone_gps():
    """
    /api/phone-gps: 클라이언트로부터 GPS 데이터를 수신
    """
    data = request.get_json()
    if data and 'gps' in data:
        gps_data = data['gps']
        phone_gps_data.append(gps_data)
        print(f"Received GPS data: {gps_data}")
        return jsonify({"status": "success", "message": "GPS data received"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400


@application.route('/api/phone-gps', methods=['GET'])
def get_phone_gps():
    """
    /api/phone-gps: 저장된 모든 GPS 데이터 반환
    """
    return jsonify(phone_gps_data)


@application.route('/api/detection', methods=['POST'])
def receive_detection():
    """
    /api/detection: YOLO 탐지 데이터와 GPS 데이터를 수신
    """
    data = request.get_json()
    if not data or 'gps' not in data or 'detected' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    gps_data = data['gps']
    latitude = gps_data.get('latitude')
    longitude = gps_data.get('longitude')
    detected = data['detected']  # YOLO 탐지 여부

    if detected:  # 위험 탐지 시 데이터 저장
        detections.append({"latitude": latitude, "longitude": longitude})
        print(f"Stored detection: Latitude={latitude}, Longitude={longitude}")
        return jsonify({"status": "success", "message": "Detection saved"}), 200
    else:
        print("No detection, data not saved.")
        return jsonify({"status": "success", "message": "No detection, nothing saved"}), 200


@application.route('/api/detections', methods=['GET'])
def get_detections():
    """
    /api/detections: 저장된 탐지 데이터 반환
    """
    return jsonify(detections)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)

