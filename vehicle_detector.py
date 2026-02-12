import cv2
import numpy as np


def load_yolo():
    net = cv2.dnn.readNetFromDarknet(
        "yolo_files/yolov3.cfg",
        "yolo_files/yolov3.weights"
    )

    with open("yolo_files/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    return net, classes, output_layers


def detect_vehicles(frame, net, classes, output_layers):
    height, width = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False
    )

    net.setInput(blob)
    outputs = net.forward(output_layers)

    vehicle_classes = ["car", "bus", "truck", "motorbike"]
    count = 0

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.4:
                label = classes[class_id]
                if label in vehicle_classes:
                    count += 1

    return count
