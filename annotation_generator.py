"""
File 2: Annotation Generator - Membuat label YOLO format
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json


class AnnotationGenerator:
    def __init__(self):
        # Mapping nama file dengan class ID dan info
        self.fruit_mapping = {
            "Peer Ya Li": {"id": 0, "price": 45000},
            "Peer hijau": {"id": 1, "price": 50000},
            "Peer Centuri": {"id": 2, "price": 55000},
            "Pear Ya Li": {"id": 3, "price": 45000},
            "Pear Crown": {"id": 4, "price": 50000},
            "Pear Centuri": {"id": 5, "price": 55000},
            "Jeruk Citrus": {"id": 6, "price": 35000},
            "Apel Malang": {"id": 7, "price": 40000},
            "Apel Fuji Premium": {"id": 8, "price": 60000},
            "Apel Fuji Pinguin": {"id": 9, "price": 55000},
            "Apel Fuji Lwstar": {"id": 10, "price": 50000},
        }

        self.class_names = {v["id"]: k for k, v in self.fruit_mapping.items()}

    def extract_fruit_type(self, filename):
        """
        Extract fruit type dari nama file
        """
        filename_lower = filename.lower()

        for fruit_name, info in self.fruit_mapping.items():
            if fruit_name.lower() in filename_lower:
                return info["id"], fruit_name

        # Default jika tidak ketemu
        return 0, "Unknown"

    def detect_fruit_bbox(self, image_path, class_id):
        """
        Mendeteksi bounding box dari fruit image
        Menggunakan color-based segmentation
        """
        img = cv2.imread(image_path)
        if img is None:
            return None

        # Convert ke HSV untuk better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Buat mask (ignore background yang terlalu terang/gelap)
        lower_black = np.array([0, 0, 0])
        upper_white = np.array([180, 255, 255])

        # Invert: cari area yang bukan background
        mask = cv2.inRange(hsv, lower_black, upper_white)

        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            # Fallback: gunakan seluruh image
            h, w = img.shape[:2]
            return [0.5, 0.5, 1.0, 1.0]

        # Ambil contour terbesar (fruit)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Normalize ke format YOLO (center_x, center_y, width, height) dalam range 0-1
        img_h, img_w = img.shape[:2]

        center_x = (x + w / 2) / img_w
        center_y = (y + h / 2) / img_h
        norm_w = w / img_w
        norm_h = h / img_h

        return [center_x, center_y, norm_w, norm_h]

    def create_yolo_annotation(self, image_path, output_path):
        """
        Membuat file annotasi YOLO format
        Format: class_id center_x center_y width height (normalized)
        """
        filename = Path(image_path).name
        class_id, fruit_name = self.extract_fruit_type(filename)

        # Deteksi bounding box
        bbox = self.detect_fruit_bbox(image_path, class_id)

        if bbox is None:
            return False

        # Tulis annotation
        with open(output_path, "w") as f:
            f.write(f"{class_id} {' '.join(map(str, bbox))}\n")

        return True

    def generate_annotations(self, image_dir, output_dir):
        """
        Generate annotations untuk semua image di direktori
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        images = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png"))]

        print(f"[INFO] Generating annotations untuk {len(images)} images...")

        success_count = 0
        for idx, img_name in enumerate(images):
            img_path = os.path.join(image_dir, img_name)
            label_name = Path(img_name).stem + ".txt"
            label_path = os.path.join(output_dir, label_name)

            if self.create_yolo_annotation(img_path, label_path):
                success_count += 1

            if (idx + 1) % 20 == 0:
                print(
                    f"  [{idx+1}/{len(images)}] Processed {success_count} annotations"
                )

        print(f"\n[SUCCESS] {success_count}/{len(images)} annotations berhasil dibuat")
        return success_count

    def create_dataset_yaml(self, output_path, num_classes=11):
        """
        Membuat file dataset.yaml untuk YOLOv8 training
        """
        yaml_content = f"""path: {os.path.abspath('./data')}
train: processed_images
val: processed_images

nc: {num_classes}
names:
"""

        for class_id in sorted(self.class_names.keys()):
            yaml_content += f"  {class_id}: {self.class_names[class_id]}\n"

        with open(output_path, "w") as f:
            f.write(yaml_content)

        print(f"[INFO] dataset.yaml created at {output_path}")

    def save_class_info(self, output_path):
        """
        Simpan mapping class ID dengan harga untuk referensi
        """
        info = {
            "classes": self.class_names,
            "prices": {k: v["price"] for k, v in self.fruit_mapping.items()},
        }

        with open(output_path, "w") as f:
            json.dump(info, f, indent=2)

        print(f"[INFO] Class info saved at {output_path}")


if __name__ == "__main__":
    IMAGE_DIR = "./data/processed_images"
    ANNOTATION_DIR = "./data/annotations"

    ann_gen = AnnotationGenerator()

    # Generate annotations
    ann_gen.generate_annotations(IMAGE_DIR, ANNOTATION_DIR)

    # Create dataset.yaml
    ann_gen.create_dataset_yaml("./data/dataset.yaml")

    # Save class info
    ann_gen.save_class_info("./data/class_info.json")
