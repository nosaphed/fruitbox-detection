"""
File 3: Model Training - Train YOLOv8 untuk deteksi buah
"""

import os

# import json
from pathlib import Path
from ultralytics import YOLO


class FruitDetectionTrainer:
    def __init__(self, model_size="n"):
        """
        Initialize trainer
        model_size: 'n' (nano) untuk dataset kecil, 's' (small), 'm' (medium)
        """
        self.model_size = model_size
        self.model = None
        self.results = None

    def load_model(self):
        """
        Load pretrained YOLOv8 model
        """
        print(f"[INFO] Loading YOLOv8{self.model_size} model...")
        self.model = YOLO(f"yolov8{self.model_size}.pt")
        print("[SUCCESS] Model loaded!")

    def train(
        self,
        dataset_yaml_path="./data/dataset.yaml",
        epochs=100,
        imgsz=640,
        batch_size=8,
        patience=20,
    ):
        """
        Train model

        Args:
            dataset_yaml_path: Path ke dataset.yaml
            epochs: Jumlah epoch training
            imgsz: Ukuran input image
            batch_size: Batch size (kurangi jika OOM)
            patience: Early stopping patience
        """

        if self.model is None:
            self.load_model()

        print("[INFO] Starting training...")
        print(f"  - Dataset: {dataset_yaml_path}")
        print(f"  - Epochs: {epochs}")
        print(f"  - Image size: {imgsz}")
        print(f"  - Batch size: {batch_size}")

        self.results = self.model.train(
            data=dataset_yaml_path,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch_size,
            patience=patience,
            device=0,  # GPU device ID (0 untuk GPU pertama, 'cpu' untuk CPU)
            save=True,
            project="./models",
            name="fruit_detector",
            pretrained=True,
            augment=True,
        )

        print("[SUCCESS] Training completed!")
        return self.results

    def save_model(self, output_path="./models/fruit_detector.pt"):
        """
        Save trained model
        """
        if self.model is not None:
            self.model.save(output_path)
            print(f"[INFO] Model saved at {output_path}")

    def validate(self):
        """
        Validate model
        """
        if self.model is None:
            print("[ERROR] Model not loaded!")
            return

        print("[INFO] Validating model...")
        metrics = self.model.val()

        print("[SUCCESS] Validation completed!")
        return metrics


def setup_dataset_structure():
    """
    Setup direktori struktur untuk YOLO training
    Jika menggunakan semi-automatic labeling
    """

    dirs = [
        "./data/raw_images",
        "./data/backgrounds",
        "./data/processed_images",
        "./data/annotations",
        "./models",
    ]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Created directory: {d}")


def create_train_val_split(image_dir, label_dir, train_ratio=0.8):
    """
    Split dataset menjadi train dan validation
    """
    import shutil
    from sklearn.model_selection import train_test_split

    images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]

    train_imgs, val_imgs = train_test_split(
        images, train_size=train_ratio, random_state=42
    )

    # Create train/val directories
    train_img_dir = "./data/train/images"
    train_label_dir = "./data/train/labels"
    val_img_dir = "./data/val/images"
    val_label_dir = "./data/val/labels"

    for d in [train_img_dir, train_label_dir, val_img_dir, val_label_dir]:
        Path(d).mkdir(parents=True, exist_ok=True)

    # Copy train files
    for img in train_imgs:
        src = os.path.join(image_dir, img)
        dst = os.path.join(train_img_dir, img)
        shutil.copy(src, dst)

        label_file = Path(img).stem + ".txt"
        src_label = os.path.join(label_dir, label_file)
        dst_label = os.path.join(train_label_dir, label_file)
        if os.path.exists(src_label):
            shutil.copy(src_label, dst_label)

    # Copy val files
    for img in val_imgs:
        src = os.path.join(image_dir, img)
        dst = os.path.join(val_img_dir, img)
        shutil.copy(src, dst)

        label_file = Path(img).stem + ".txt"
        src_label = os.path.join(label_dir, label_file)
        dst_label = os.path.join(val_label_dir, label_file)
        if os.path.exists(src_label):
            shutil.copy(src_label, dst_label)

    print("\n[INFO] Dataset split:")
    print(f"  - Train: {len(train_imgs)} images")
    print(f"  - Validation: {len(val_imgs)} images")

    # Update dataset.yaml untuk split baru
    yaml_content = """path: ./data
train: train/images
val: val/images

nc: 11
names:
  0: Peer Ya Li
  1: Peer hijau
  2: Peer Centuri
  3: Pear Ya Li
  4: Pear Crown
  5: Pear Centuri
  6: Jeruk Citrus
  7: Apel Malang
  8: Apel Fuji Premium
  9: Apel Fuji Pinguin
  10: Apel Fuji Lwstar
"""

    with open("./data/dataset.yaml", "w") as f:
        f.write(yaml_content)

    print("[SUCCESS] Train/val split completed!")


if __name__ == "__main__":
    # Setup direktori
    setup_dataset_structure()

    print("\n" + "=" * 60)
    print("FRUIT DETECTION MODEL TRAINING")
    print("=" * 60 + "\n")

    # Create train/val split - REQUIRED for proper training
    create_train_val_split('./data/processed_images', './data/annotations')

    # Initialize trainer - nano model better for small dataset
    trainer = FruitDetectionTrainer(model_size="n")  # 'n' prevents overfitting with small data

    # Train model - optimized for small dataset
    trainer.train(
        dataset_yaml_path="./data/dataset.yaml",
        epochs=80,  # Slightly increased as nano model trains slower
        imgsz=640,
        batch_size=8,  # Can use 8 with nano model
        patience=20,  # More patience for nano model
    )

    # Save model
    trainer.save_model("./models/fruit_detector_best.pt")

    # Validate
    trainer.validate()

    print("\n[DONE] Training pipeline completed!")
