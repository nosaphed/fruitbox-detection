"""
File 1: Data Preparation - Preprocessing dan Data Augmentation
Mengubah PNG background transparan ke background nyata
"""

import os
import cv2
import numpy as np
from PIL import Image
import albumentations as A
from pathlib import Path


class DataPreparation:
    def __init__(self, input_dir, output_dir, background_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.background_dir = background_dir

        # Buat direktori output jika belum ada
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def remove_background_add_new(self, image_path, output_path):
        """
        Menghilangkan background transparan dan mengganti dengan background nyata
        """
        img = Image.open(image_path).convert("RGBA")

        # Dapatkan random background
        bg_files = os.listdir(self.background_dir)
        if bg_files:
            bg_path = os.path.join(self.background_dir, np.random.choice(bg_files))
            bg = Image.open(bg_path).convert("RGB")
        else:
            # Jika tidak ada background, buat background solid color
            bg = Image.new(
                "RGB",
                img.size,
                color=(
                    np.random.randint(0, 255),
                    np.random.randint(0, 255),
                    np.random.randint(0, 255),
                ),
            )

        # Resize background sesuai ukuran product image
        bg = bg.resize(img.size)

        # Composite images
        bg.paste(img, (0, 0), img)
        return np.array(bg)

    def augment_image(self, image):
        """
        Data augmentation menggunakan albumentations
        """
        transform = A.Compose(
            [
                A.HorizontalFlip(p=0.5),
                A.Rotate(limit=30, p=0.7),
                A.GaussNoise(p=0.3),
                A.RandomBrightnessContrast(p=0.3),
                A.Blur(blur_limit=3, p=0.3),
                A.Perspective(scale=(0.05, 0.1), p=0.3),
                A.Affine(scale=(0.8, 1.2), p=0.3),
            ]
        )

        augmented = transform(image=image)
        return augmented["image"]

    def preprocess_image(self, image):
        """
        Preprocessing: normalize dan resize
        """
        # Resize ke ukuran standar
        image = cv2.resize(image, (640, 640))

        # Normalize pixel values
        image = image.astype(np.float32) / 255.0

        return image

    def process_dataset(self, augmentation_times=5):
        """
        Proses semua image: background replacement + augmentation
        """
        images = [f for f in os.listdir(self.input_dir) if f.endswith(".png")]

        print(f"[INFO] Menemukan {len(images)} image untuk diproses")

        for idx, img_name in enumerate(images):
            img_path = os.path.join(self.input_dir, img_name)
            base_name = Path(img_name).stem

            print(f"[{idx+1}/{len(images)}] Processing: {img_name}")

            # Original dengan background baru
            original_with_bg = self.remove_background_add_new(img_path, None)
            original_with_bg = cv2.cvtColor(original_with_bg, cv2.COLOR_RGB2BGR)
            cv2.imwrite(
                os.path.join(self.output_dir, f"{base_name}_original.jpg"),
                original_with_bg,
            )

            # Data augmentation
            for aug_idx in range(augmentation_times):
                augmented = self.augment_image(original_with_bg)

                output_path = os.path.join(
                    self.output_dir, f"{base_name}_aug_{aug_idx}.jpg"
                )
                cv2.imwrite(output_path, augmented)

        print(
            f"[INFO] Dataset berhasil diproses! Total image: {len(images) * (augmentation_times + 1)}"
        )
        return len(images) * (augmentation_times + 1)


if __name__ == "__main__":
    # Konfigurasi path
    INPUT_DIR = "./data/raw_images"  # Path ke PNG files
    OUTPUT_DIR = "./data/processed_images"
    BACKGROUND_DIR = "./data/backgrounds"

    # Buat direktori jika belum ada
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(BACKGROUND_DIR, exist_ok=True)

    # Inisialisasi
    prep = DataPreparation(INPUT_DIR, OUTPUT_DIR, BACKGROUND_DIR)

    # Proses dataset
    total_images = prep.process_dataset(augmentation_times=5)

    print(f"\n[SUCCESS] Total dataset setelah augmentation: {total_images} images")
