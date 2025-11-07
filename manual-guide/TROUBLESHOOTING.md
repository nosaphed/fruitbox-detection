# 🔧 Troubleshooting Guide - Fruit Detection System

Panduan lengkap mengatasi error yang sering muncul.

---

## 📋 Quick Error Reference

| Error | Solusi Cepat | Detail |
|-------|--------------|--------|
| CUDA OOM | Kurangi batch size | [Link](#1-cuda-out-of-memory) |
| No labels found | Run fix structure | [Link](#2-no-labels-found) |
| Camera not open | Cek camera ID | [Link](#3-camera-tidak-terbuka) |
| Import error | Install dependencies | [Link](#4-module-not-found) |
| Training stuck | Check GPU/CPU | [Link](#5-training-stuck) |
| False positives | Increase threshold | [Link](#6-terlalu-banyak-false-positives) |
| No detection | Lower threshold | [Link](#7-tidak-ada-detection) |

---

## 🚨 Error Saat Training

### 1. CUDA Out of Memory

**Error Message**:
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Penyebab**: GPU memory tidak cukup

**Solusi**:

#### Option 1: Kurangi Batch Size
```bash
# Edit training.py atau saat input
Batch size: 4  # atau 2
```

#### Option 2: Gunakan CPU
```python
# Edit training.py line 58
device='cpu'  # ganti dari device=0
```

#### Option 3: Clear CUDA Cache
```bash
python -c "import torch; torch.cuda.empty_cache()"
```

#### Option 4: Gunakan Model Lebih Kecil
```bash
Model size: n  # nano (paling kecil)
```

**Verification**:
```bash
# Cek GPU memory
nvidia-smi

# Cek CUDA available
python -c "import torch; print(torch.cuda.is_available())"
```

---

### 2. No Labels Found

**Error Message**:
```
WARNING ⚠️ no labels found in detect set, can not compute metrics without labels
```

**Penyebab**: Label files tidak ada di folder yang benar

**Solusi**:

#### Step 1: Cek Struktur Folder
```bash
ls data/train/labels/  # Harus ada .txt files
ls data/val/labels/    # Harus ada .txt files
```

#### Step 2: Fix Dataset Structure
```bash
python main.py
# Pilih: 8 (Fix Dataset Structure)
```

#### Step 3: Verify dataset.yaml
```bash
cat data/dataset.yaml
```

Harus seperti ini:
```yaml
path: /absolute/path/to/data
train: train/images
val: val/images
```

**Jika masih error**:
```bash
# Manual fix
python fix_dataset_structure.py
```

---

### 3. Labels Missing or Empty

**Error Message**:
```
⚠️ Labels are missing or empty in /path/to/processed_images.cache
```

**Penyebab**: Annotations belum di-generate atau corrupt

**Solusi**:

#### Step 1: Generate Annotations
```bash
python main.py
# Pilih: 3 (Generate Annotations)
```

#### Step 2: Verify Annotations
```bash
# Cek jumlah
ls data/annotations/*.txt | wc -l
ls data/processed_images/*.jpg | wc -l
# Harus sama!

# Cek isi salah satu
cat data/annotations/Apel_Fuji_Lwstar_aug_0.txt
# Format: class_id x_center y_center width height
# Contoh: 10 0.5 0.5 0.8 0.8
```

#### Step 3: Delete Cache
```bash
rm data/*.cache
rm data/*/*.cache
```

---

### 4. Module Not Found

**Error Message**:
```
ModuleNotFoundError: No module named 'ultralytics'
```

**Solusi**:

#### Option 1: Install via pip
```bash
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

#### Option 2: Install via requirements.txt
```bash
pip install -r requirements.txt
```

#### Option 3: Use Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

**Verification**:
```bash
python -c "import ultralytics; print(ultralytics.__version__)"
python -c "import cv2; print(cv2.__version__)"
```

---

### 5. Training Stuck

**Gejala**: Training tidak progress, stuck di epoch tertentu

**Penyebab**: 
- GPU hang
- Dataset corrupt
- Memory leak

**Solusi**:

#### Step 1: Check GPU
```bash
nvidia-smi
# Cek GPU utilization, jika 0% → problem
```

#### Step 2: Restart Training
```bash
# Kill process
pkill -f python

# Clear cache
rm data/*.cache

# Restart
python main.py → option 4
```

#### Step 3: Use CPU
```python
# Edit training.py line 58
device='cpu'
```

#### Step 4: Reduce Workers
```python
# Edit training.py line 60
workers=2  # ganti dari 4
```

---

### 6. Validation Loss Increasing

**Gejala**: Training loss turun, tapi validation loss naik

**Penyebab**: Overfitting (model terlalu hafal training data)

**Solusi**:

#### Option 1: Stop Training Early
```bash
# Training akan auto-stop dengan patience
# Jika belum, stop manual (Ctrl+C)
```

#### Option 2: Collect More Data
```bash
# Target: 50-100 images per class
# Letakkan di data/raw_images/
# Jalankan ulang Step 2-6
```

#### Option 3: Increase Augmentation
```bash
python main.py → option 2
# Masukkan: 30 atau 40
```

#### Option 4: Use Smaller Model
```bash
Model size: n  # nano
```

---

## 🎥 Error Saat Detection

### 7. Camera Tidak Terbuka

**Error Message**:
```
[ERROR] Tidak bisa membuka kamera!
```

**Solusi**:

#### Step 1: Cek Available Cameras
```bash
# Linux
ls /dev/video*

# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAIL')"
```

#### Step 2: Try Different Camera ID
```bash
python camera_detection.py --camera 1
# atau 2, 3, dst
```

#### Step 3: Check Permissions
```bash
# Linux
sudo usermod -a -G video $USER
# Logout dan login lagi
```

#### Step 4: Test with Simple Script
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imshow('Test', frame)
    cv2.waitKey(0)
else:
    print("Camera failed")
```

---

### 8. Terlalu Banyak False Positives

**Gejala**: Banyak bounding box yang salah

**Solusi**:

#### Option 1: Increase Confidence
```bash
python camera_detection.py --confidence 0.8
# atau 0.9
```

#### Option 2: Increase IoU
```python
# Edit camera_detection.py line 85
iou=0.8  # ganti dari 0.7
```

#### Option 3: Reduce Max Detections
```python
# Edit camera_detection.py line 86
max_det=5  # ganti dari 10
```

#### Option 4: Retrain Model
```bash
# Collect more data
# Increase augmentation
# Retrain
```

---

### 9. Tidak Ada Detection

**Gejala**: Tidak ada bounding box muncul

**Solusi**:

#### Option 1: Lower Confidence
```bash
python camera_detection.py --confidence 0.5
# atau 0.4
```

#### Option 2: Check Lighting
```bash
# Pastikan:
# - Pencahayaan cukup
# - Tidak ada shadow
# - Background kontras dengan object
```

#### Option 3: Check Model
```bash
# Test dengan image
python camera_detection.py --test-image ./test.jpg

# Jika image juga tidak detect → model problem
# Retrain model
```

#### Option 4: Check Distance
```bash
# Optimal distance: 30-50cm dari camera
# Terlalu dekat/jauh → tidak detect
```

---

### 10. FPS Rendah

**Gejala**: FPS < 10, video lag

**Solusi**:

#### Option 1: Use Smaller Model
```bash
# Retrain dengan model nano
Model size: n
```

#### Option 2: Reduce Resolution
```python
# Edit camera_detection.py line 82
imgsz=416  # ganti dari 640
```

#### Option 3: Reduce Max Detections
```python
# Edit camera_detection.py line 86
max_det=5
```

#### Option 4: Use GPU
```bash
# Pastikan CUDA available
python -c "import torch; print(torch.cuda.is_available())"
```

---

### 11. Harga Tidak Muncul

**Gejala**: Detection OK, tapi harga tidak tampil

**Solusi**:

#### Step 1: Check class_info.json
```bash
cat data/class_info.json
```

Harus ada:
```json
{
  "classes": {
    "10": "Apel Fuji Lwstar"
  },
  "prices": {
    "Apel Fuji Lwstar": 50000
  }
}
```

#### Step 2: Regenerate class_info.json
```bash
python main.py → option 3
```

#### Step 3: Check Code
```python
# Edit camera_detection.py
# Pastikan line 109-110 ada:
price = self.prices.get(class_name, "N/A")
```

---

## 📁 Error File/Folder

### 12. Permission Denied

**Error Message**:
```
PermissionError: [Errno 13] Permission denied: './data/...'
```

**Solusi**:

#### Option 1: Change Permissions
```bash
chmod -R 755 ./data
chmod -R 755 ./models
chmod -R 755 ./screenshots
```

#### Option 2: Use Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

#### Option 3: Run as User (not root)
```bash
# Jangan pakai sudo
python main.py  # ✓
sudo python main.py  # ✗
```

---

### 13. File Not Found

**Error Message**:
```
FileNotFoundError: [Errno 2] No such file or directory: './models/fruit_detector_best.pt'
```

**Solusi**:

#### Step 1: Check File Exists
```bash
ls models/fruit_detector_best.pt
```

#### Step 2: Train Model
```bash
# Jika file tidak ada
python main.py → option 4
```

#### Step 3: Check Path
```bash
# Pastikan running dari src/ directory
pwd
# Output harus: /path/to/tugas9/src
```

---

### 14. Disk Space Full

**Error Message**:
```
OSError: [Errno 28] No space left on device
```

**Solusi**:

#### Step 1: Check Space
```bash
df -h
```

#### Step 2: Clean Up
```bash
# Hapus model lama
rm -rf models/fruit_detector[2-5]/

# Hapus cache
rm data/*.cache
rm data/*/*.cache

# Hapus screenshots lama
rm screenshots/detection_*.jpg
```

#### Step 3: Reduce Augmentation
```bash
# Kurangi multiplier
python main.py → option 2
# Masukkan: 15 (instead of 25)
```

---

## 🐛 Error Lain-lain

### 15. Segmentation Fault

**Error Message**:
```
Segmentation fault (core dumped)
```

**Penyebab**: Memory corruption, biasanya OpenCV issue

**Solusi**:

#### Option 1: Reinstall OpenCV
```bash
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-python
```

#### Option 2: Update Libraries
```bash
pip install --upgrade ultralytics opencv-python pillow
```

#### Option 3: Check System
```bash
# Update system
sudo apt update && sudo apt upgrade  # Linux
```

---

### 16. Killed (Signal 9)

**Error Message**:
```
Killed
```

**Penyebab**: Out of memory (RAM)

**Solusi**:

#### Option 1: Reduce Batch Size
```bash
Batch size: 2
```

#### Option 2: Close Other Apps
```bash
# Close browser, IDE, etc
```

#### Option 3: Increase Swap
```bash
# Linux
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### 17. Assertion Error

**Error Message**:
```
AssertionError: No labels found in /path/to/labels
```

**Solusi**: Sama dengan [Error #2](#2-no-labels-found)

---

### 18. YAML Error

**Error Message**:
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solusi**:

#### Step 1: Check dataset.yaml
```bash
cat data/dataset.yaml
```

#### Step 2: Fix Format
```yaml
# Harus ada spasi setelah colon
path: /path/to/data  # ✓
path:/path/to/data   # ✗

# Indentation harus konsisten (2 spaces)
names:
  0: Peer Ya Li      # ✓
  1: Peer hijau      # ✓
```

#### Step 3: Regenerate
```bash
python main.py → option 3
```

---

## 🔍 Debugging Tips

### 1. Enable Verbose Mode
```python
# Edit training.py line 61
verbose=True
```

### 2. Save Logs
```bash
python main.py 2>&1 | tee debug.log
```

### 3. Check System Info
```bash
# Python version
python --version

# Package versions
pip list | grep ultralytics
pip list | grep opencv
pip list | grep torch

# GPU info
nvidia-smi

# Disk space
df -h

# Memory
free -h
```

### 4. Test Components Individually
```bash
# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"

# Test model
python -c "from ultralytics import YOLO; model = YOLO('./models/fruit_detector_best.pt'); print('OK')"

# Test CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 📞 Still Having Issues?

### 1. Run Analysis
```bash
python main.py → option 7
```

### 2. Check Logs
```bash
cat models/fruit_detector/results.csv
tail -n 50 debug.log
```

### 3. Clean Install
```bash
# Backup
cp -r data/ data_backup/
cp models/fruit_detector_best.pt model_backup.pt

# Clean
rm -rf venv/
rm -rf data/*.cache

# Reinstall
python -m venv venv
source venv/bin/activate
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

### 4. System Requirements
```
Minimum:
- Python 3.8+
- 4GB RAM
- 2GB disk space
- CPU only

Recommended:
- Python 3.10+
- 8GB+ RAM
- 10GB disk space
- NVIDIA GPU with CUDA
```

---

**Good luck! 🚀**
