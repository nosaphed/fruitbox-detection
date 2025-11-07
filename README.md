# 🍎 Fruit Detection System using YOLOv8

Sistem deteksi buah real-time menggunakan YOLOv8 dan OpenCV dengan tampilan harga otomatis.

![Status](https://img.shields.io/badge/status-stable-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-nano-orange)

## ✨ Features

- 🎯 Real-time fruit detection dengan YOLOv8
- 💰 Tampilan harga otomatis per buah
- 📊 11 jenis buah (Apel, Pear, Jeruk)
- 🚀 Optimized untuk dataset kecil
- 📸 Screenshot detection results
- 🔧 Built-in troubleshooting tools

## 📁 Project Structure

```
src/
├── main.py                      # Main entry point ⭐
├── camera_detection.py          # Real-time detection
├── training.py                  # Model training
├── preparation.py               # Data augmentation
├── annotation_generator.py      # Label generation
├── improve_detection.py         # Analysis tools
├── fix_dataset_structure.py     # Dataset fixer
├── setup.py                     # System setup
├── data/
│   ├── raw_images/             # 11 original images
│   ├── processed_images/       # 275 augmented images
│   ├── train/                  # Training split (80%)
│   └── val/                    # Validation split (20%)
├── models/
│   └── fruit_detector_best.pt  # Trained model
└── screenshots/                # Detection results
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install ultralytics opencv-python pillow numpy albumentations scikit-learn
```

### 2. Run Main Menu
```bash
cd src
python main.py
```

### 3. Follow Workflow
1. Setup System (option 1)
2. Prepare Data (option 2) → enter `25`
3. Generate Annotations (option 3)
4. Train Model (option 4) → model: `n`, epochs: `80`
5. Run Detection (option 5)

### Quick Detection (if model exists)
```bash
python camera_detection.py --confidence 0.7
```

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Panduan lengkap penggunaan
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solusi error & debugging
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Changelog & cleanup guide

## 🎯 Current Status

| Metric | Value |
|--------|-------|
| Raw Images | 11 |
| Processed Images | 275 (25x augmentation) |
| Training Images | 220 (80%) |
| Validation Images | 55 (20%) |
| Classes | 11 fruit types |
| Model | YOLOv8 nano |
| Confidence Threshold | 0.7 |
| IoU Threshold | 0.7 |

## 📊 Training Parameters

**Optimized for Small Dataset:**
- Model: `nano` (prevents overfitting)
- Epochs: `80` (optimal for 11 raw images)
- Batch Size: `8`
- Patience: `20` (early stopping)
- Augmentation: `25x` multiplier

## 🎥 Detection Output

```
FPS: 30.1
Detected Fruits:
- Apel Fuji Lwstar: 1
  Rp 50,000
```

**Controls:**
- `Q` - Quit
- `S` - Screenshot

## 📝 Workflow Detail

### Step 1: Prepare Dataset
```bash
python main.py → option 2
# Enter augmentation: 25
```

Output:
- 275 augmented images created
- Backgrounds applied

### Step 2: Generate Annotations
```bash
python main.py → option 3
```

Output:
- YOLO labels in `./data/annotations/`
- `dataset.yaml` created
- `class_info.json` with prices

### Step 3: Train Model
```bash
python main.py → option 4
# Model: n, Epochs: 80, Batch: 8
```

Output:
- Model: `./models/fruit_detector_best.pt`
- Training metrics logged

### Step 4: Run Detection
```bash
python main.py → option 5
# Camera: 0, Confidence: 0.7
```

Or directly:
```bash
python camera_detection.py --confidence 0.7
```

## 🍎 Detected Fruit Classes

| ID | Fruit Name | Price (Rp) |
|----|-----------|----------:|
| 0 | Peer Ya Li | 45,000 |
| 1 | Peer hijau | 50,000 |
| 2 | Peer Centuri | 55,000 |
| 3 | Pear Ya Li | 45,000 |
| 4 | Pear Crown | 50,000 |
| 5 | Pear Centuri | 55,000 |
| 6 | Jeruk Citrus | 35,000 |
| 7 | Apel Malang | 40,000 |
| 8 | Apel Fuji Premium | 60,000 |
| 9 | Apel Fuji Pinguin | 55,000 |
| 10 | Apel Fuji Lwstar | 50,000 |

## 🔧 Troubleshooting

### Common Issues

**1. CUDA Out of Memory**
```bash
# Reduce batch size
Batch size: 4  # or 2
```

**2. No Labels Found**
```bash
python main.py → option 8  # Fix dataset structure
```

**3. Camera Not Opening**
```bash
python camera_detection.py --camera 1  # Try different ID
```

**4. Too Many False Positives**
```bash
python camera_detection.py --confidence 0.8  # Increase threshold
```

**5. No Detection**
```bash
python camera_detection.py --confidence 0.5  # Lower threshold
```

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for complete guide.

## 💡 Tips for Better Results

### Improve Accuracy
- Collect 50-100 images per class
- Vary lighting conditions
- Include different angles
- Use diverse backgrounds
- Increase augmentation to 30-40x

### Speed Up Training
- Use GPU (CUDA)
- Reduce image size (640 → 416)
- Use smaller model (nano)
- Enable mixed precision

### Reduce False Positives
- Increase confidence (0.7 → 0.8)
- Increase IoU (0.7 → 0.8)
- Reduce max_det (10 → 5)
- Retrain with more data

### Add New Fruit Class
1. Add images to `data/raw_images/`
2. Edit `annotation_generator.py` → `fruit_mapping`
3. Run workflow from Step 2

## 📚 Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Albumentations](https://albumentations.ai/)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

MIT License - feel free to use for your projects!

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- Albumentations library

---

**Made with ❤️ for fruit detection**
