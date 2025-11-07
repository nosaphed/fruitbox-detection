# 🍎 Fruit Detection System - User Guide

Panduan lengkap penggunaan sistem deteksi buah menggunakan YOLOv8.

---

## 📋 Table of Contents

1. [Instalasi](#instalasi)
2. [Quick Start](#quick-start)
3. [Workflow Lengkap](#workflow-lengkap)
4. [Troubleshooting](#troubleshooting)
5. [FAQ](#faq)
6. [Tips & Tricks](#tips--tricks)

---

## 🚀 Instalasi

### Requirements
- Python 3.8+
- CUDA-capable GPU (recommended) atau CPU
- Webcam (untuk real-time detection)
- Minimal 4GB RAM
- 2GB disk space

### Step 1: Clone/Download Project
```bash
cd /path/to/your/workspace
# Project sudah ada di: /home/grego/streamer/compvis/tugas9/src
```

### Step 2: Install Dependencies
```bash
cd src
python main.py
# Pilih option 1: Setup System
```

Atau manual:
```bash
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

---

## ⚡ Quick Start

### Cara Tercepat (Jika Sudah Ada Model)

```bash
cd src
python camera_detection.py --confidence 0.7
```

### Dari Awal (Training Baru)

```bash
cd src
python main.py
```

Ikuti menu:
1. Setup System (option 1)
2. Prepare Data (option 2) → masukkan `25`
3. Generate Annotations (option 3)
4. Train Model (option 4) → model: `n`, epochs: `80`
5. Run Detection (option 5)

---

## 📖 Workflow Lengkap

### Step 1: Setup System

**Tujuan**: Install dependencies dan buat folder structure

```bash
python main.py
# Pilih: 1
```

**Output**:
```
✓ Dependencies installed
✓ Created: ./data/raw_images
✓ Created: ./data/backgrounds
✓ Created: ./models
...
```

**Troubleshooting**:
- ❌ **Error: pip not found**
  ```bash
  # Install pip dulu
  sudo apt install python3-pip  # Linux
  # atau
  brew install python3  # macOS
  ```

- ❌ **Error: Permission denied**
  ```bash
  # Gunakan virtual environment
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # atau
  venv\Scripts\activate  # Windows
  ```

---

### Step 2: Prepare Data

**Tujuan**: Augmentasi gambar dari 11 → 275 images

**Persiapan**:
1. Letakkan 11 gambar PNG di `./data/raw_images/`
2. Pastikan nama file mengandung nama buah (contoh: `Apel Fuji Lwstar.png`)

**Jalankan**:
```bash
python main.py
# Pilih: 2
# Masukkan: 25 (augmentation multiplier)
```

**Output**:
```
Processing: Apel Fuji Lwstar.png
  ✓ Created 25 augmented versions
Processing: Peer Ya Li.png
  ✓ Created 25 augmented versions
...
Total images: 275
```

**Troubleshooting**:
- ❌ **Error: No PNG images found**
  ```bash
  # Cek isi folder
  ls data/raw_images/
  # Pastikan ada file .png
  ```

- ❌ **Error: Background directory empty**
  ```bash
  # Generate backgrounds
  python setup.py
  # Atau manual:
  ls data/backgrounds/  # Harus ada minimal 1 image
  ```

- ❌ **Error: Out of memory**
  ```bash
  # Kurangi augmentation multiplier
  # Masukkan: 15 atau 10
  ```

---

### Step 3: Generate Annotations

**Tujuan**: Buat YOLO format labels untuk setiap gambar

```bash
python main.py
# Pilih: 3
```

**Output**:
```
Processing: Apel Fuji Lwstar_aug_0.jpg
  ✓ Annotation saved
Processing: Apel Fuji Lwstar_aug_1.jpg
  ✓ Annotation saved
...
✓ dataset.yaml created
✓ class_info.json created
```

**Troubleshooting**:
- ❌ **Error: No processed images found**
  ```bash
  # Jalankan Step 2 dulu
  ls data/processed_images/  # Harus ada .jpg files
  ```

- ❌ **Error: Cannot detect bounding box**
  ```bash
  # Gambar mungkin terlalu gelap/terang
  # Cek manual:
  python -c "from PIL import Image; img = Image.open('data/processed_images/xxx.jpg'); img.show()"
  ```

- ❌ **Error: Invalid class name**
  ```bash
  # Pastikan nama file sesuai dengan class yang ada
  # Edit annotation_generator.py → fruit_mapping
  ```

---

### Step 4: Analyze Dataset (Optional)

**Tujuan**: Cek kualitas dataset sebelum training

```bash
python main.py
# Pilih: 7
```

**Output**:
```
DATASET ANALYSIS
Raw images: 11
Processed images: 275
Annotations: 275

⚠️ CRITICAL: Too few raw images!
Recommendation: Collect at least 50-100 images per class
```

**Action**:
- Jika raw images < 20: Collect more images
- Jika processed < 500: Increase augmentation
- Jika annotations mismatch: Run option 8 (Fix Structure)

---

### Step 5: Fix Dataset Structure (Jika Perlu)

**Tujuan**: Split dataset ke train/val dengan benar

```bash
python main.py
# Pilih: 8
```

**Output**:
```
✓ Created: ./data/train/images
✓ Created: ./data/train/labels
✓ Created: ./data/val/images
✓ Created: ./data/val/labels
✓ Copying 220 training images...
✓ Copying 55 validation images...
✓ Updated dataset.yaml
```

**Troubleshooting**:
- ❌ **Error: No labels found**
  ```bash
  # Jalankan Step 3 dulu
  ls data/annotations/  # Harus ada .txt files
  ```

---

### Step 6: Train Model

**Tujuan**: Train YOLOv8 model dengan dataset

```bash
python main.py
# Pilih: 4
```

**Input Parameters**:
```
Model size: n          # nano (recommended untuk dataset kecil)
Epochs: 80            # optimal untuk 11 raw images
Batch size: 8         # sesuaikan dengan GPU memory
Patience: 20          # early stopping
```

**Output**:
```
Epoch 1/80: loss=2.5, mAP=0.3
Epoch 2/80: loss=2.1, mAP=0.4
...
Epoch 45/80: loss=0.8, mAP=0.85
✓ Best model saved: ./models/fruit_detector_best.pt
```

**Troubleshooting**:

- ❌ **Error: CUDA out of memory**
  ```bash
  # Solusi 1: Kurangi batch size
  # Masukkan: 4 atau 2
  
  # Solusi 2: Gunakan CPU
  # Edit training.py line 58:
  device='cpu'  # ganti dari device=0
  ```

- ❌ **Error: Labels missing**
  ```bash
  # Jalankan option 8 (Fix Dataset Structure)
  python main.py
  # Pilih: 8
  ```

- ❌ **Error: No labels in detect set**
  ```bash
  # Cek dataset.yaml
  cat data/dataset.yaml
  # Pastikan path benar:
  # train: train/images
  # val: val/images
  ```

- ❌ **Training stuck / tidak progress**
  ```bash
  # Cek GPU usage
  nvidia-smi  # Jika ada GPU
  
  # Atau gunakan CPU
  # Edit training.py → device='cpu'
  ```

- ❌ **Validation loss meningkat terus**
  ```bash
  # Overfitting! Stop training
  # Solusi:
  # 1. Collect more raw images
  # 2. Increase augmentation
  # 3. Use smaller model (nano)
  ```

---

### Step 7: Run Detection

**Tujuan**: Real-time detection menggunakan webcam

```bash
python main.py
# Pilih: 5
```

**Input**:
```
Camera ID: 0           # 0 = default webcam, 1 = external
Confidence: 0.7        # threshold untuk detection
```

**Controls**:
- **Q**: Quit/Exit
- **S**: Screenshot (save ke ./screenshots/)

**Output**:
```
[INFO] Kamera terbuka
[INFO] Confidence threshold: 0.7
FPS: 30.1
Detected Fruits:
- Apel Fuji Lwstar: 1
  Rp 50,000
```

**Troubleshooting**:

- ❌ **Error: Cannot open camera**
  ```bash
  # Cek available cameras
  ls /dev/video*  # Linux
  
  # Coba camera ID lain
  # Masukkan: 1 atau 2
  
  # Test manual
  python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
  ```

- ❌ **Error: Model not found**
  ```bash
  # Cek model exists
  ls models/fruit_detector_best.pt
  
  # Jika tidak ada, train dulu (Step 6)
  ```

- ❌ **FPS sangat rendah (<10)**
  ```bash
  # Solusi 1: Gunakan model nano
  # Solusi 2: Kurangi resolusi
  # Edit camera_detection.py line 82:
  imgsz=416  # ganti dari 640
  ```

- ❌ **Terlalu banyak false positives**
  ```bash
  # Naikkan confidence threshold
  python camera_detection.py --confidence 0.8
  # atau 0.9
  ```

- ❌ **Tidak ada detection sama sekali**
  ```bash
  # Turunkan confidence threshold
  python camera_detection.py --confidence 0.5
  
  # Atau cek lighting
  # Pastikan pencahayaan cukup
  ```

- ❌ **Harga tidak muncul**
  ```bash
  # Cek class_info.json
  cat data/class_info.json
  # Pastikan ada price untuk setiap class
  ```

---

### Step 8: Test on Image

**Tujuan**: Test detection pada single image

```bash
python main.py
# Pilih: 6
# Masukkan path: ./test_image.jpg
```

**Atau langsung**:
```bash
python camera_detection.py --test-image ./test_image.jpg
```

**Troubleshooting**:
- ❌ **Error: Image not found**
  ```bash
  # Cek path benar
  ls ./test_image.jpg
  
  # Gunakan absolute path
  /home/grego/streamer/compvis/tugas9/src/test_image.jpg
  ```

---

## 🔧 Troubleshooting Umum

### 1. Import Error

```bash
❌ ModuleNotFoundError: No module named 'ultralytics'
```

**Solusi**:
```bash
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

---

### 2. CUDA Error

```bash
❌ RuntimeError: CUDA out of memory
```

**Solusi**:
```bash
# Option 1: Kurangi batch size
# training.py → batch_size=4 atau 2

# Option 2: Gunakan CPU
# training.py → device='cpu'

# Option 3: Clear cache
python -c "import torch; torch.cuda.empty_cache()"
```

---

### 3. Permission Error

```bash
❌ PermissionError: [Errno 13] Permission denied
```

**Solusi**:
```bash
# Gunakan virtual environment
python -m venv venv
source venv/bin/activate

# Atau ubah permission
chmod -R 755 ./data
chmod -R 755 ./models
```

---

### 4. Dataset Error

```bash
❌ WARNING: no labels found in detect set
```

**Solusi**:
```bash
# Fix dataset structure
python main.py
# Pilih: 8

# Atau manual
python fix_dataset_structure.py
```

---

### 5. Model Performance Buruk

**Gejala**: Banyak false positives atau tidak detect

**Solusi**:
```bash
# 1. Analyze dataset
python main.py → option 7

# 2. Collect more raw images (target: 50+ per class)

# 3. Retrain dengan augmentation lebih tinggi
python main.py → option 2 → masukkan: 30

# 4. Adjust confidence threshold
python camera_detection.py --confidence 0.8
```

---

## ❓ FAQ

### Q: Berapa minimal raw images yang dibutuhkan?
**A**: Minimal 20-30 per class. Saat ini 11 images total sudah cukup untuk proof-of-concept, tapi untuk production butuh 50-100+ per class.

### Q: Kenapa training lama sekali?
**A**: 
- Gunakan GPU jika ada
- Kurangi epochs (80 → 50)
- Gunakan model nano (n)
- Kurangi batch size jika OOM

### Q: Bagaimana cara menambah class baru?
**A**:
1. Tambah gambar baru di `data/raw_images/`
2. Edit `annotation_generator.py` → `fruit_mapping`
3. Jalankan ulang Step 2-6

### Q: Apakah bisa pakai video file instead of webcam?
**A**: Ya, edit `camera_detection.py`:
```python
# Line 234, ganti:
cap = cv2.VideoCapture("path/to/video.mp4")
```

### Q: Bagaimana cara export model untuk deployment?
**A**:
```bash
# Export ke ONNX
python -c "from ultralytics import YOLO; model = YOLO('./models/fruit_detector_best.pt'); model.export(format='onnx')"
```

---

## 💡 Tips & Tricks

### 1. Improve Accuracy
- Collect 50-100 images per class
- Vary lighting conditions
- Include different angles
- Use diverse backgrounds
- Increase augmentation to 30-40x

### 2. Speed Up Training
- Use GPU (CUDA)
- Reduce image size (640 → 416)
- Use smaller model (nano)
- Enable mixed precision (amp=True)

### 3. Reduce False Positives
- Increase confidence threshold (0.7 → 0.8)
- Increase IoU threshold (0.7 → 0.8)
- Reduce max_det (10 → 5)
- Retrain with more data

### 4. Better Detection
- Good lighting (avoid shadows)
- Clean background
- Stable camera position
- Optimal distance (30-50cm)

### 5. Save Disk Space
```bash
# Hapus model lama
rm -rf models/fruit_detector[2-5]/

# Hapus cache
rm data/*.cache
rm data/*/*.cache

# Compress screenshots
find screenshots/ -name "*.jpg" -exec jpegoptim {} \;
```

---

## 📞 Support

Jika masih ada error:

1. **Check logs**:
   ```bash
   # Training logs
   cat models/fruit_detector/results.csv
   
   # System logs
   python main.py 2>&1 | tee debug.log
   ```

2. **Run analysis**:
   ```bash
   python main.py → option 7
   ```

3. **Check versions**:
   ```bash
   python --version
   pip list | grep ultralytics
   pip list | grep opencv
   ```

4. **Clean install**:
   ```bash
   # Backup data
   cp -r data/ data_backup/
   
   # Fresh install
   pip uninstall ultralytics opencv-python -y
   pip install ultralytics opencv-python
   ```

---

## 📝 Changelog

### v1.0 (Current)
- ✅ Fixed excessive bounding boxes
- ✅ Improved UI (price in sidebar)
- ✅ Optimized training for small dataset
- ✅ Added analysis tools
- ✅ Added dataset structure fixer

---

**Happy Detecting! 🍎🍊🍐**
