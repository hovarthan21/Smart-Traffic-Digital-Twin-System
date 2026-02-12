import streamlit as st
import cv2
import pandas as pd
import time
from ultralytics import YOLO

from traffic_simulator import TrafficDigitalTwin
from signal_optimizer import optimize_signal
from pollution_estimator import estimate_pollution
from emergency_detector import detect_emergency


st.set_page_config(layout="wide")
st.title("🚦 Smart Traffic Digital Twin System ")

option = st.sidebar.selectbox(
    "Select Mode",
    ["Live Camera", "Upload Video", "Digital Twin Simulation"]
)

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  

model = load_model()

def detect_vehicles(frame):
    results = model(frame)

    vehicle_targets = ["car", "motorcycle", "bus", "truck"]

    vehicle_counts = {
        "Car": 0,
        "Motorcycle": 0,
        "Bus": 0,
        "Truck": 0
    }

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[cls_id]

            if class_name in vehicle_targets and confidence > 0.4:

                formatted_name = class_name.capitalize()
                vehicle_counts[formatted_name] += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 255, 0), 2)

                label = f"{formatted_name} {confidence:.2f}"

                cv2.putText(frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2)

    total_vehicles = sum(vehicle_counts.values())

    return frame, total_vehicles, vehicle_counts

if option == "Live Camera":

    st.subheader("📷 Live Traffic Monitoring")

    start = st.button("Start Camera")

    if start:
        cap = cv2.VideoCapture(0)
        frame_placeholder = st.empty()
        stats_placeholder = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, vehicle_count, vehicle_counts = detect_vehicles(frame)

            signal = optimize_signal(vehicle_count)
            co2, pollution = estimate_pollution(vehicle_count)
            emergency = detect_emergency(vehicle_count)

            frame_placeholder.image(frame, channels="BGR")

            with stats_placeholder.container():
                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric("🚗 Total", vehicle_count)
                col2.metric("🚙 Cars", vehicle_counts["Car"])
                col3.metric("🚌 Buses", vehicle_counts["Bus"])
                col4.metric("🚚 Trucks", vehicle_counts["Truck"])
                col5.metric("🏍 Bikes", vehicle_counts["Motorbike"])

                st.markdown("---")

                col6, col7 = st.columns(2)

                col6.metric("🌫 CO2 Emission (kg)", f"{co2:.2f}")
                col7.metric("🚥 Pollution Level", pollution)

                st.markdown("---")
                st.info(signal)
                st.warning(emergency)

        cap.release()

elif option == "Upload Video":

    st.subheader("📂 Upload Traffic Video")

    video_file = st.file_uploader("Upload MP4 File", type=["mp4"])

    if video_file:
        tfile = open("temp.mp4", "wb")
        tfile.write(video_file.read())

        cap = cv2.VideoCapture("temp.mp4")

        frame_placeholder = st.empty()
        stats_placeholder = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, vehicle_count, vehicle_counts = detect_vehicles(frame)

            signal = optimize_signal(vehicle_count)
            co2, pollution = estimate_pollution(vehicle_count)
            emergency = detect_emergency(vehicle_count)

            frame_placeholder.image(frame, channels="BGR")

            with stats_placeholder.container():
                
                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric("🚗 Total", vehicle_count)
                col2.metric("🚙 Cars", vehicle_counts["Car"])
                col3.metric("🚌 Buses", vehicle_counts["Bus"])
                col4.metric("🚚 Trucks", vehicle_counts["Truck"])
                col5.metric("🏍 Bikes", vehicle_counts["Motorcycle"])

                st.markdown("---")

                col6, col7 = st.columns(2)

                col6.metric("🌫 CO2 Emission (kg)", f"{co2:.2f}")
                col7.metric("🚥 Pollution Level", pollution)

                st.markdown("---")
                st.info(signal)
                st.warning(emergency)


        cap.release()
        st.success("Video Processing Completed")

elif option == "Digital Twin Simulation":

    import plotly.graph_objects as go
    import random
    import time

    st.subheader("🚦 3D Traffic Intersection Digital Twin")

    start_sim = st.button("Start 3D Simulation")

    if start_sim:

        placeholder = st.empty()

        signal = "North"

        for step in range(50):

            if step % 10 == 0:
                signal = random.choice(["North", "South", "East", "West"])

            vehicles_x = []
            vehicles_y = []
            vehicles_z = []

            for i in range(15):
                vehicles_x.append(0)
                vehicles_y.append(random.uniform(5, 20) - step * 0.3)
                vehicles_z.append(0)

                vehicles_x.append(0)
                vehicles_y.append(random.uniform(-5, -20) + step * 0.3)
                vehicles_z.append(0)

                vehicles_x.append(random.uniform(5, 20) - step * 0.3)
                vehicles_y.append(0)
                vehicles_z.append(0)
              
                vehicles_x.append(random.uniform(-5, -20) + step * 0.3)
                vehicles_y.append(0)
                vehicles_z.append(0)

            fig = go.Figure()

            fig.add_trace(go.Scatter3d(
                x=[-25, 25],
                y=[0, 0],
                z=[0, 0],
                mode='lines',
                line=dict(width=20),
                name="East-West Road"
            ))

            fig.add_trace(go.Scatter3d(
                x=[0, 0],
                y=[-25, 25],
                z=[0, 0],
                mode='lines',
                line=dict(width=20),
                name="North-South Road"
            ))

            fig.add_trace(go.Scatter3d(
                x=vehicles_x,
                y=vehicles_y,
                z=vehicles_z,
                mode='markers',
                marker=dict(
                    size=6,
                ),
                name="Vehicles"
            ))

            fig.update_layout(
                scene=dict(
                    xaxis=dict(range=[-30, 30]),
                    yaxis=dict(range=[-30, 30]),
                    zaxis=dict(range=[-5, 10]),
                ),
                height=600,
                title=f"Active Signal: {signal}"
            )

            placeholder.plotly_chart(fig, use_container_width=True)

            time.sleep(0.3)

        st.success("3D Simulation Completed")

st.markdown(
    """
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 15px;
        font-size: 15px;
        color: white;
        background-color: #111111;
        margin-top: 50px;
        border-top: 1px solid #444;
    }
    </style>

    <div class="footer">
        © 2026 Developed by <b>Hovarthan S</b> | An AI Innovator 
    </div>
    """,
    unsafe_allow_html=True
)
