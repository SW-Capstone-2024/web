# from flask import Flask, render_template, request, jsonify, redirect, url_for

# application = Flask(__name__)

# # 저장된 데이터
# detections = []
# phone_gps_data = []


# @application.route('/')
# def index():
#     """
#     루트 페이지: 기기 등록 HTML 렌더링
#     """
#     return render_template('index.html')


# @application.route('/device', methods=['POST'])
# def device():
#     """
#     /device: 기기 번호를 입력받아 device.html로 이동
#     """
#     device_number = request.form.get('device_number')
#     if device_number:
#         return render_template('device.html', device_number=device_number)
#     else:
#         return redirect(url_for('index'))


# @application.route('/api/phone-gps', methods=['POST'])
# def receive_phone_gps():
#     """
#     /api/phone-gps: 클라이언트로부터 GPS 데이터를 수신
#     """
#     data = request.get_json()
#     if data and 'gps' in data:
#         gps_data = data['gps']
#         phone_gps_data.append(gps_data)
#         print(f"Received GPS data: {gps_data}")
#         return jsonify({"status": "success", "message": "GPS data received"}), 200
#     return jsonify({"status": "error", "message": "Invalid data"}), 400


# @application.route('/api/phone-gps', methods=['GET'])
# def get_phone_gps():
#     """
#     /api/phone-gps: 저장된 모든 GPS 데이터 반환
#     """
#     return jsonify(phone_gps_data)


# @application.route('/api/detection', methods=['POST'])
# def receive_detection():
#     """
#     /api/detection: YOLO 탐지 데이터와 GPS 데이터를 수신
#     """
#     data = request.get_json()
#     if not data or 'gps' not in data or 'detected' not in data:
#         return jsonify({"status": "error", "message": "Invalid data"}), 400

#     gps_data = data['gps']
#     latitude = gps_data.get('latitude')
#     longitude = gps_data.get('longitude')
#     detected = data['detected']  # YOLO 탐지 여부

#     if detected:  # 위험 탐지 시 데이터 저장
#         detections.append({"latitude": latitude, "longitude": longitude})
#         print(f"Stored detection: Latitude={latitude}, Longitude={longitude}")
#         return jsonify({"status": "success", "message": "Detection saved"}), 200
#     else:
#         print("No detection, data not saved.")
#         return jsonify({"status": "success", "message": "No detection, nothing saved"}), 200


# @application.route('/api/detections', methods=['GET'])
# def get_detections():
#     """
#     /api/detections: 저장된 탐지 데이터 반환
#     """
#     return jsonify(detections)


# if __name__ == '__main__':
#     application.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, request, render_template_string
import folium

app = Flask(__name__)

# 지도 중심 설정
map_center = [37.8864, 127.7371]  # 기본 지도 중심
zoom_level = 16

# 사용자 지정 좌표 (4개)
custom_coords = [
    [37.886582, 127.739342],
    [37.886600, 127.739270], 
     [37.886532, 127.739192], 
    [37.886525, 127.739212]



    

]

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Markers</title>
</head>
<body>
    <h1 style="text-align: center;">기기 번호: {{ device_number }}</h1>
    <p style="text-align: center;"></p>
    <div style="width: 80%; margin: 0 auto;">
        {{ map_html|safe }}
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    """
    루트 페이지: 기기 등록 HTML 렌더링
    """
    return render_template('index.html')


@app.route("/device", methods=["POST"])
def device():
    """
    기기 번호를 입력받아 지도 페이지로 이동
    """
    device_number = request.form.get("device_number")
    if not device_number:
        return render_template('index.html', error="기기 번호를 입력하세요.")

    # Folium 지도 생성
    m = folium.Map(location=map_center, zoom_start=zoom_level)

    # 사용자 지정 좌표에 마커 추가
    for lat, lon in custom_coords:
        folium.Marker(
            location=[lat, lon],
            popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # Folium 지도 HTML 렌더링
    map_html = m._repr_html_()

    # HTML 반환 (기기 번호와 지도 표시)
    return render_template_string(HTML_TEMPLATE, device_number=device_number, map_html=map_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

