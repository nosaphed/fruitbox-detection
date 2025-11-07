# 🚀 Quick Reference - Fruit Detection System

Cheat sheet untuk command yang sering dipakai.

---

## 📋 Main Commands

```bash
# Run main menu
python main.py

# Direct detection
python camera_detection.py --confidence 0.7

# Test on image
python camera_detection.py --test-image ./test.jpg

# Analyze dataset
python improve_detection.py

# Fix dataset structure
python fix_dataset_structure.py
```

---

## 🎯 Menu Options

| Option | Action | When to Use |
|--------|--------|-------------|
| 1 | Setup System | First time setup |
| 2 | Prepare Data | After adding raw images |
| 3 | Generate Annotations | After data preparation |
| 4 | Train Model | After annotations ready |
| 5 | Run Detection | After model trained |
| 6 | Test on Image | Test single image |
| 7 | Analyze Dataset | Check dataset quality |
| 8 | Fix Structure | Fix train/val split |
| 0 | Exit | Close program |

---

## ⚙️ Recommended Parameters

### For Small Dataset (11 raw images)
```
Augmentation: 25
Model: n (nano)
Epochs: 80
Batch: 8
Patience: 20
Confidence: 0.7
IoU: 0.7
```

### For Medium Dataset (50+ raw images)
```
Augmentation: 15
Model: s (small)
Epochs: 100
Batch: 8
Patience: 25
Confidence: 0.6
IoU: 0.6
```

### For Large Dataset (100+ raw images)
```
Augmentation: 10
Model: s or m
Epochs: 150
Batch: 16
Patience: 30
Confidence: 0.5
IoU: 0.5
```

---

## 🔧 Quick Fixes

### CUDA Out of Memory
```bash
# Option 1: Reduce batch
Batch size: 4

# Option 2: Use CPU
# Edit training.py → device='cpu'
```

### No Labels Found
```bash
python main.py
# Choose: 8 (Fix Dataset Structure)
```

### Camera Not Opening
```bash
# Try different camera ID
python camera_detection.py --camera 1
```

### Too Many False Positives
```bash
# Increase confidence
python camera_detection.py --confidence 0.8
```

### No Detection
```bash
# Lower confidence
python camera_detection.py --confidence 0.5
```

---

## 📁 Important Files

```
src/
├── main.py                      # Main entry point
├── camera_detection.py          # Detection script
├── training.py                  # Training script
├── data/
│   ├── raw_images/             # Put PNG images here
│   ├── dataset.yaml            # Dataset config
│   └── class_info.json         # Class & price info
└── models/
    └── fruit_detector_best.pt  # Trained model
```

---

## 🎮 Keyboard Controls

### During Detection
- `Q` - Quit/Exit
- `S` - Screenshot

---

## 📊 Check Status

```bash
# Dataset size
ls data/raw_images/ | wc -l
ls data/processed_images/ | wc -l

# Model exists
ls models/fruit_detector_best.pt

# GPU available
python -c "import torch; print(torch.cuda.is_available())"

# Disk space
df -h

# Memory
free -h
```

---

## 🔍 Debug Commands

```bash
# Check Python version
python --version

# Check packages
pip list | grep ultralytics
pip list | grep opencv

# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"

# Test model
python -c "from ultralytics import YOLO; model = YOLO('./models/fruit_detector_best.pt'); print('OK')"

# Clear cache
rm data/*.cache
rm data/*/*.cache
```

---

## 🗑️ Cleanup Commands

```bash
# Remove old models
rm -rf models/fruit_detector[2-5]/

# Remove cache
rm data/*.cache
rm data/*/*.cache

# Remove screenshots
rm screenshots/detection_*.jpg

# Remove pretrained models
rm yolo*.pt
```

---

## 📝 Edit Configuration

### Change Confidence Threshold
```python
# camera_detection.py line 38
self.conf_threshold = 0.7  # Change this
```

### Change IoU Threshold
```python
# camera_detection.py line 85
iou=0.7  # Change this
```

### Change Max Detections
```python
# camera_detection.py line 86
max_det=10  # Change this
```

### Add New Fruit Class
```python
# annotation_generator.py
self.fruit_mapping = {
    'New Fruit': {'id': 11, 'price': 45000},
    # Add here
}
```

---

## 🚨 Emergency Commands

### Kill Stuck Process
```bash
pkill -f python
```

### Force Stop Training
```bash
Ctrl + C
```

### Reset Everything
```bash
# Backup first!
cp -r data/ data_backup/
cp models/fruit_detector_best.pt model_backup.pt

# Clean
rm -rf data/train/ data/val/
rm data/*.cache

# Restart from Step 3
python main.py → option 8
```

---

## 📞 Get Help

```bash
# Run analysis
python main.py → option 7

# Check logs
cat models/fruit_detector/results.csv

# Save debug log
python main.py 2>&1 | tee debug.log
```

---

## 🎯 Workflow Shortcuts

### Full Pipeline (First Time)
```bash
python main.py
# 1 → 2 (enter 25) → 3 → 4 (n, 80, 8, 20) → 5
```

### Retrain Only
```bash
python main.py
# 4 (n, 80, 8, 20)
```

### Detection Only
```bash
python camera_detection.py --confidence 0.7
```

### Quick Test
```bash
python camera_detection.py --test-image ./test.jpg
```

---

## 💾 Backup Important Files

```bash
# Backup model
cp models/fruit_detector_best.pt ~/backup/

# Backup data
tar -czf data_backup.tar.gz data/

# Backup config
cp data/dataset.yaml ~/backup/
cp data/class_info.json ~/backup/
```

---

## 🔄 Update System

```bash
# Update packages
pip install --upgrade ultralytics opencv-python

# Update YOLOv8
pip install --upgrade ultralytics

# Check versions
pip list | grep ultralytics
```

---

**Keep this handy! 📌**
