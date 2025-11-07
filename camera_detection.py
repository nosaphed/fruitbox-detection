"""
File 4: Real-time Camera Detection - Deteksi buah menggunakan kamera
Menampilkan bounding box, class name, dan harga
"""

import cv2
import json
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from collections import defaultdict
import time


class FruitDetectionCamera:
    def __init__(
        self,
        model_path="./models/fruit_detector_best.pt",
        class_info_path="./data/class_info.json",
    ):
        """
        Initialize camera detection system
        """
        self.model = YOLO(model_path)
        self.class_info = self.load_class_info(class_info_path)

        self.class_names = self.class_info["classes"]
        self.prices = self.class_info["prices"]

        # Color palette untuk bounding box
        self.colors = self.generate_colors(len(self.class_names))

        # Frame counter untuk FPS
        self.frame_count = 0
        self.fps = 0
        self.start_time = time.time()

        # Confidence threshold - higher for small dataset
        self.conf_threshold = 0.7

    def load_class_info(self, class_info_path):
        """
        Load class info dari JSON
        """
        if not Path(class_info_path).exists():
            print("[WARNING] Class info tidak ditemukan, menggunakan default...")
            return {
                "classes": {
                    0: "Peer Ya Li",
                    1: "Peer hijau",
                    2: "Peer Centuri",
                    3: "Pear Ya Li",
                    4: "Pear Crown",
                    5: "Pear Centuri",
                    6: "Jeruk Citrus",
                    7: "Apel Malang",
                    8: "Apel Fuji Premium",
                    9: "Apel Fuji Pinguin",
                    10: "Apel Fuji Lwstar",
                },
                "prices": {},
            }

        with open(class_info_path, "r") as f:
            return json.load(f)

    def generate_colors(self, num_classes):
        """
        Generate random colors untuk setiap class
        """
        colors = {}
        for i in range(num_classes):
            colors[i] = tuple(np.random.randint(0, 255, 3).tolist())
        return colors

    def detect_fruits(self, frame):
        """
        Detect fruits di frame menggunakan model
        """
        # Increase IoU threshold to reduce overlapping boxes
        # Increase confidence threshold for better precision
        results = self.model(
            frame, 
            conf=max(self.conf_threshold, 0.7),  # Minimum 0.7 confidence
            iou=0.7,  # Higher IoU threshold to reduce overlaps
            max_det=10,  # Limit maximum detections
            verbose=False
        )
        return results[0]

    def draw_predictions(self, frame, results):
        """
        Draw bounding box, class name, dan harga di frame
        """
        h, w = frame.shape[:2]

        detected_fruits = defaultdict(int)

        if results.boxes is not None:
            for box in results.boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())

                # Get class name dan price
                class_name = self.class_names.get(str(class_id), f"Class {class_id}")
                price = self.prices.get(class_name, "N/A")
                
                # Store detection with price info
                if class_name not in detected_fruits:
                    detected_fruits[class_name] = {"count": 0, "price": price}
                detected_fruits[class_name]["count"] += 1

                # Draw bounding box
                color = self.colors.get(class_id, (0, 255, 0))
                thickness = 2
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

                # Font settings
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 2

                # Label atas: Nama buah saja
                label_text = f"{class_name}"
                text_size = cv2.getTextSize(label_text, font, font_scale, font_thickness)[0]
                
                # Background untuk label
                y_offset = 25
                cv2.rectangle(
                    frame,
                    (x1, y1 - y_offset - 5),
                    (x1 + text_size[0] + 10, y1 - 5),
                    color,
                    -1,
                )
                cv2.putText(
                    frame,
                    label_text,
                    (x1 + 5, y1 - 8),
                    font,
                    font_scale,
                    (255, 255, 255),
                    font_thickness,
                )

                # Confidence di pojok kanan atas box
                conf_text = f"{confidence:.2f}"
                conf_size = cv2.getTextSize(conf_text, font, 0.4, 1)[0]
                cv2.rectangle(
                    frame,
                    (x2 - conf_size[0] - 8, y1 - conf_size[1] - 8),
                    (x2, y1),
                    (0, 0, 0),
                    -1,
                )
                cv2.putText(
                    frame,
                    conf_text,
                    (x2 - conf_size[0] - 4, y1 - 4),
                    font,
                    0.4,
                    (255, 255, 255),
                    1,
                )

        return frame, detected_fruits

    def draw_stats(self, frame, detected_fruits, fps):
        """
        Draw statistics di frame
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2

        # FPS counter
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(
            frame, fps_text, (10, 30), font, font_scale, (0, 255, 0), font_thickness
        )

        # Detected fruits summary with prices
        y_pos = 60
        if detected_fruits:
            cv2.putText(
                frame,
                "Detected Fruits:",
                (10, y_pos),
                font,
                font_scale,
                (255, 255, 0),
                font_thickness,
            )
            for fruit_name, info in detected_fruits.items():
                y_pos += 25
                # Get count and price
                if isinstance(info, dict):
                    count = info["count"]
                    price = info["price"]
                else:
                    count = info
                    price = "N/A"
                
                # Format price
                if isinstance(price, int):
                    price_str = f"Rp {price:,}"
                else:
                    price_str = f"Rp {price}"
                
                # Display fruit name and count
                fruit_text = f"- {fruit_name}: {count}"
                cv2.putText(
                    frame, fruit_text, (15, y_pos), font, 0.5, (200, 200, 200), 1
                )
                
                # Display price below
                y_pos += 20
                price_text = f"  {price_str}"
                cv2.putText(
                    frame, price_text, (15, y_pos), font, 0.5, (100, 255, 100), 1
                )

        return frame

    def calculate_fps(self):
        """
        Calculate FPS
        """
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            elapsed = time.time() - self.start_time
            self.fps = 30 / elapsed
            self.start_time = time.time()
        return self.fps

    def run_camera(self, camera_id=1, confidence_threshold=0.7):
        """
        Run real-time detection dari kamera

        Args:
            camera_id: ID kamera (0 untuk default)
            confidence_threshold: Confidence threshold untuk deteksi
        """

        self.conf_threshold = confidence_threshold

        # Open camera
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            print("[ERROR] Tidak bisa membuka kamera!")
            return

        print("[INFO] Kamera terbuka. Press 'q' untuk exit, 's' untuk screenshot")
        print(f"[INFO] Confidence threshold: {confidence_threshold}")

        screenshot_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                print("[ERROR] Error membaca frame!")
                break

            # Flip frame untuk mirror effect (optional)
            frame = cv2.flip(frame, 1)

            # Detect fruits
            results = self.detect_fruits(frame)

            # Draw predictions
            frame, detected_fruits = self.draw_predictions(frame, results)

            # Calculate dan draw FPS
            fps = self.calculate_fps()
            frame = self.draw_stats(frame, detected_fruits, fps)

            # Display frame
            cv2.imshow("Fruit Detection - Press Q to exit", frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("[INFO] Exiting...")
                break
            elif key == ord("s"):
                screenshot_path = f"./screenshots/detection_{screenshot_count}.jpg"
                Path("./screenshots").mkdir(exist_ok=True)
                cv2.imwrite(screenshot_path, frame)
                print(f"[INFO] Screenshot saved: {screenshot_path}")
                screenshot_count += 1

        cap.release()
        cv2.destroyAllWindows()
        print("[DONE] Camera detection stopped!")

    def test_on_image(self, image_path):
        """
        Test detection pada image statis
        """
        frame = cv2.imread(image_path)

        if frame is None:
            print(f"[ERROR] Tidak bisa membaca image: {image_path}")
            return

        # Detect
        results = self.detect_fruits(frame)

        # Draw
        frame, detected_fruits = self.draw_predictions(frame, results)
        frame = self.draw_stats(frame, detected_fruits, 0)

        # Display
        cv2.imshow("Fruit Detection Test", frame)

        print("[INFO] Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Optionally save
        output_path = Path(image_path).stem + "_detected.jpg"
        cv2.imwrite(output_path, frame)
        print(f"[INFO] Result saved: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fruit Detection Camera")
    parser.add_argument(
        "--model",
        type=str,
        default="./models/fruit_detector_best.pt",
        help="Path ke model",
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera ID")
    parser.add_argument(
        "--confidence", type=float, default=0.7, help="Confidence threshold"
    )
    parser.add_argument(
        "--test-image", type=str, default=None, help="Test pada image (optional)"
    )

    args = parser.parse_args()

    # Initialize detector
    detector = FruitDetectionCamera(model_path=args.model)

    # Run
    if args.test_image:
        detector.test_on_image(args.test_image)
    else:
        detector.run_camera(camera_id=1, confidence_threshold=args.confidence)
