# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-07

### 🎉 Initial Release

#### Added
- Real-time fruit detection using YOLOv8
- Support for 11 fruit classes
- Automatic price display
- Interactive main menu system
- Data augmentation pipeline (25x multiplier)
- Automatic annotation generation
- Model training with optimal parameters
- Camera detection with FPS counter
- Screenshot functionality
- Dataset analysis tool
- Dataset structure fixer
- Comprehensive documentation

#### Features
- **Detection System**
  - YOLOv8 nano model
  - Confidence threshold: 0.7
  - IoU threshold: 0.7
  - Max detections: 10 per frame
  - Real-time FPS display
  - Price display in sidebar

- **Training System**
  - Optimized for small datasets
  - Early stopping with patience
  - Automatic train/val split (80/20)
  - GPU/CPU support
  - Progress monitoring

- **Data Pipeline**
  - Background removal and replacement
  - Multiple augmentation techniques
  - Automatic YOLO annotation
  - Class and price mapping

#### Documentation
- Complete user guide
- Troubleshooting guide
- Quick reference card
- Cleanup summary
- Contributing guidelines

#### Performance
- Training: 80 epochs optimal
- Detection: 30+ FPS on GPU
- Accuracy: Good for 11 raw images
- Model size: ~6MB (nano)

---

## [0.9.0] - 2024-11-06

### Fixed
- **Critical**: Excessive bounding boxes issue
  - Increased confidence threshold (0.5 → 0.7)
  - Increased IoU threshold (0.5 → 0.7)
  - Added max detection limit (10)
  
- **UI**: Price visibility issue
  - Moved price to sidebar
  - Simplified bounding box labels
  - Improved text readability

### Changed
- Training configuration optimized for small dataset
  - Model: small → nano
  - Epochs: 100 → 80
  - Batch size: 8 (maintained)
  - Patience: 25 → 20

- Augmentation multiplier: 5 → 25 (default)

### Added
- Dataset analysis tool (`improve_detection.py`)
- Dataset structure fixer (`fix_dataset_structure.py`)
- Menu options for analysis and fixing

---

## [0.8.0] - 2024-11-05

### Added
- Initial training pipeline
- Basic detection system
- Data preparation module
- Annotation generator

### Known Issues
- Too many false positives
- Price display not visible
- Training overfitting on small dataset

---

## Roadmap

### [1.1.0] - Planned
- [ ] Add batch image processing
- [ ] Support for video file input
- [ ] Export detection results to CSV
- [ ] Add confidence adjustment slider
- [ ] Improve annotation accuracy

### [1.2.0] - Planned
- [ ] Web interface using Flask/FastAPI
- [ ] REST API for detection
- [ ] Mobile app support
- [ ] Cloud deployment guide

### [2.0.0] - Future
- [ ] Multi-object tracking
- [ ] Instance segmentation
- [ ] 3D bounding boxes
- [ ] Integration with POS systems
- [ ] Automated inventory management

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-11-07 | Initial stable release |
| 0.9.0 | 2024-11-06 | Fixed detection issues |
| 0.8.0 | 2024-11-05 | Initial development |

---

## Migration Guide

### From 0.9.0 to 1.0.0

No breaking changes. Simply:
1. Pull latest code
2. Run `python main.py`
3. Enjoy new features!

### From 0.8.0 to 0.9.0

**Breaking Changes:**
- Detection parameters changed
- Training configuration updated

**Migration Steps:**
1. Backup your model: `cp models/fruit_detector_best.pt backup/`
2. Update code
3. Retrain model with new parameters
4. Test detection

---

## Contributors

- Main Developer: [Your Name]
- Contributors: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Support

- 📖 [Documentation](README.md)
- 🐛 [Report Bug](https://github.com/yourusername/fruit-detection/issues)
- 💡 [Request Feature](https://github.com/yourusername/fruit-detection/issues)
- 💬 [Discussions](https://github.com/yourusername/fruit-detection/discussions)

---

**[Unreleased]** - Changes in development branch
