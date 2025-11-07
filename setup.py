"""
File 5: Utility Functions dan Setup
Instalasi dependencies, download sample backgrounds, dll
"""

import os
import subprocess

# import urllib.request
# import zipfile
from pathlib import Path


def install_dependencies():
    """
    Install semua dependencies yang diperlukan
    """
    print("[INFO] Installing dependencies...")

    requirements = [
        "ultralytics",
        "opencv-python",
        "numpy",
        "pillow",
        "albumentations",
        "torch",
        "torchvision",
        "scikit-learn",
    ]

    for package in requirements:
        print(f"  Installing {package}...")
        subprocess.check_call(["pip", "install", package, "-q"])

    print("[SUCCESS] All dependencies installed!")


def setup_project_structure():
    """
    Setup direktori struktur project
    """
    print("[INFO] Setting up project structure...")

    directories = [
        "./data/raw_images",
        "./data/backgrounds",
        "./data/processed_images",
        "./data/annotations",
        "./data/train/images",
        "./data/train/labels",
        "./data/val/images",
        "./data/val/labels",
        "./models",
        "./screenshots",
        "./weights",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {directory}")

    print("[SUCCESS] Project structure ready!")


def download_sample_backgrounds():
    """
    Download sample background images
    (Optional - menggunakan sample backgrounds dari internet)
    """
    print("[INFO] Preparing background images...")

    bg_dir = "./data/backgrounds"

    # Buat beberapa sample background dengan warna solid
    import cv2
    import numpy as np

    backgrounds = [
        ("white_bg.jpg", (255, 255, 255)),
        ("gray_bg.jpg", (128, 128, 128)),
        ("light_bg.jpg", (200, 200, 200)),
        ("wood_bg.jpg", (139, 90, 43)),
        ("beige_bg.jpg", (245, 245, 220)),
        ("blue_bg.jpg", (100, 150, 200)),
        ("green_bg.jpg", (100, 150, 100)),
    ]

    for bg_name, color in backgrounds:
        bg_path = os.path.join(bg_dir, bg_name)
        if not os.path.exists(bg_path):
            # Create 640x640 background
            bg = np.zeros((640, 640, 3), dtype=np.uint8)
            bg[:] = color
            cv2.imwrite(bg_path, bg)
            print(f"  ✓ Created: {bg_name}")

    print("[INFO] Background images ready!")


def create_requirements_txt():
    """
    Create requirements.txt file
    """
    requirements_content = """ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
pillow>=9.5.0
albumentations>=1.3.0
torch>=2.0.0
torchvision>=0.15.0
scikit-learn>=1.3.0
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements_content)

    print("[INFO] requirements.txt created!")


def create_readme():
    """
    Create README.md file
    """
    readme_content = """# Fruit Detection System using YOLOv8

Sistem deteksi buah dalam dus menggunakan YOLOv8 dan OpenCV dengan real-time camera detection.

## Arsitektur Project

```
├── 1_data_preparation.py      # Data augmentation & preprocessing
├── 2_annotation_generator.py  # Generate YOLO annotations
├── 3_train_model.py          # Train YOLOv8 model
├── 4_camera_detection.py     # Real-time camera detection
├── 5_utils_and_setup.py      # Utilities & setup
├── data/
│   ├── raw_images/           # PNG images dari dataset
│   ├── backgrounds/          # Background images
│   ├── processed_images/     # Augmented images
│   ├── annotations/          # YOLO format labels
│   ├── train/               # Training split
│   └── val/                 # Validation split
├── models/                   # Trained models
└── screenshots/             # Detection results
```

## Setup & Installation

### 1. Clone atau buat project directory
```bash
mkdir fruit_detection
cd fruit_detection
```

### 2. Install dependencies
```bash
python 5_utils_and_setup.py
# atau
pip install -r requirements.txt
```

### 3. Setup project structure
```bash
python -c "from utils_and_setup import setup_project_structure; setup_project_structure()"
```

## Workflow

### Step 1: Prepare Dataset
Letakkan PNG images di `./data/raw_images/`

```bash
python 1_data_preparation.py
```

Output:
- Augmented images di `./data/processed_images/`
- Backgrounds diambil dari `./data/backgrounds/`

### Step 2: Generate Annotations
```bash
python 2_annotation_generator.py
```

Output:
- YOLO format labels di `./data/annotations/`
- `dataset.yaml` untuk training
- `class_info.json` untuk reference

### Step 3: Train Model
```bash
python 3_train_model.py
```

Konfigurasi training:
- Model: YOLOv8-small (bisa diubah ke 'n', 'm', 'l', 'x')
- Epochs: 100
- Image size: 640x640
- Batch size: 8

Output:
- Trained model: `./models/fruit_detector_best.pt`
- Training logs: `./models/runs/`

### Step 4: Real-time Detection
```bash
# Default dengan kamera 0
python 4_camera_detection.py

# Dengan custom confidence threshold
python 4_camera_detection.py --confidence 0.6

# Test dengan image
python 4_camera_detection.py --test-image path/to/image.jpg
```

Controls:
- **Q**: Exit
- **S**: Screenshot

## Deteksi Classes

| ID | Fruit Name | Price |
|----|-----------:|------:|
| 0 | Peer Ya Li | 45.000 |
| 1 | Peer hijau | 50.000 |
| 2 | Peer Centuri | 55.000 |
| 3 | Pear Ya Li | 45.000 |
| 4 | Pear Crown | 50.000 |
| 5 | Pear Centuri | 55.000 |
| 6 | Jeruk Citrus | 35.000 |
| 7 | Apel Malang | 40.000 |
| 8 | Apel Fuji Premium | 60.000 |
| 9 | Apel Fuji Pinguin | 55.000 |
| 10 | Apel Fuji Lwstar | 50.000 |

## File Descriptions

### 1_data_preparation.py
- Menghilangkan background transparan dari PNG
- Mengganti dengan background nyata
- Data augmentation: rotation, flip, noise, brightness, blur, perspective

### 2_annotation_generator.py
- Auto-extract fruit type dari nama file
- Deteksi bounding box menggunakan color-based segmentation
- Generate YOLO format annotations
- Buat dataset.yaml dan class_info.json

### 3_train_model.py
- Load pretrained YOLOv8 model
- Train dengan custom dataset
- Early stopping dengan patience
- Save best model

### 4_camera_detection.py
- Real-time detection dari camera/video
- Tampilkan bounding box, class name, harga, confidence
- FPS counter
- Statistics display

### 5_utils_and_setup.py
- Install dependencies
- Setup project structure
- Create sample backgrounds

## Tips & Tricks

### Kurangi Memory Usage
- Ubah batch_size dari 8 menjadi 4 atau lebih kecil di `3_train_model.py`
- Gunakan model 'n' (nano) untuk GPU dengan memory terbatas

### Improve Accuracy
- Tingkatkan augmentation di `1_data_preparation.py`
- Tambah epochs di `3_train_model.py`
- Collect lebih banyak background images di `./data/backgrounds/`

### Custom Fruit Classes
Edit mapping di `2_annotation_generator.py`:
```python
self.fruit_mapping = {
    'Fruit Name': {'id': 0, 'price': 50000},
    ...
}
```

## Troubleshooting

### CUDA OOM Error
- Kurangi batch_size di training
- Kurangi imgsz (misal 416 instead of 640)
- Gunakan device='cpu' untuk CPU-only training

### Model tidak terload
- Pastikan path model correct di `4_camera_detection.py`
- Pastikan model sudah trained di `3_train_model.py`

### Tidak ada bounding box terdeteksi
- Tingkatkan confidence threshold
- Pastikan lighting dan background konsisten
- Collect lebih banyak training data

## Resources

- YOLOv8 Docs: https://docs.ultralytics.com/
- OpenCV Docs: https://docs.opencv.org/
- Albumentations: https://albumentations.ai/

## License

MIT
"""

    with open("README.md", "w") as f:
        f.write(readme_content)

    print("[INFO] README.md created!")


def run_full_setup():
    """
    Run complete setup
    """
    print("\n" + "=" * 60)
    print("FRUIT DETECTION SYSTEM - SETUP")
    print("=" * 60 + "\n")

    # Install dependencies
    install_dependencies()
    print()

    # Setup directories
    setup_project_structure()
    print()

    # Create backgrounds
    download_sample_backgrounds()
    print()

    # Create files
    create_requirements_txt()
    create_readme()

    print("\n" + "=" * 60)
    print("[SUCCESS] Setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Place your PNG images in ./data/raw_images/")
    print("2. Run: python 1_data_preparation.py")
    print("3. Run: python 2_annotation_generator.py")
    print("4. Run: python 3_train_model.py")
    print("5. Run: python 4_camera_detection.py")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            install_dependencies()
        elif sys.argv[1] == "setup":
            setup_project_structure()
        elif sys.argv[1] == "backgrounds":
            download_sample_backgrounds()
        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        run_full_setup()
