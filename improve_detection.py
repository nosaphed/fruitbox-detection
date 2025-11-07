#!/usr/bin/env python3
"""
Script to improve detection quality by addressing common issues
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO


class DetectionImprover:
    def __init__(self, model_path="./models/fruit_detector_best.pt"):
        self.model_path = model_path
        self.model = None
        
    def load_model(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            self.model = YOLO(self.model_path)
            print(f"✓ Model loaded: {self.model_path}")
        else:
            print(f"❌ Model not found: {self.model_path}")
            
    def analyze_dataset_size(self):
        """Analyze current dataset size"""
        raw_dir = "./data/raw_images"
        processed_dir = "./data/processed_images"
        annotations_dir = "./data/annotations"
        
        raw_count = len([f for f in os.listdir(raw_dir) if f.endswith(('.png', '.jpg'))])
        processed_count = len([f for f in os.listdir(processed_dir) if f.endswith(('.jpg'))])
        annotation_count = len([f for f in os.listdir(annotations_dir) if f.endswith('.txt')])
        
        print("\n" + "="*50)
        print("DATASET ANALYSIS")
        print("="*50)
        print(f"Raw images: {raw_count}")
        print(f"Processed images: {processed_count}")
        print(f"Annotations: {annotation_count}")
        
        # Recommendations
        if raw_count < 20:
            print("\n⚠️  CRITICAL: Too few raw images!")
            print("   Recommendation: Collect at least 50-100 images per class")
            
        if processed_count < 500:
            print("\n⚠️  WARNING: Small processed dataset")
            print("   Recommendation: Increase augmentation multiplier")
            
        return raw_count, processed_count, annotation_count
        
    def test_detection_quality(self, test_image_path=None, conf_threshold=0.7, iou_threshold=0.7):
        """Test detection with improved parameters"""
        if self.model is None:
            self.load_model()
            
        if test_image_path is None:
            # Use first available processed image
            processed_dir = "./data/processed_images"
            images = [f for f in os.listdir(processed_dir) if f.endswith('.jpg')]
            if not images:
                print("❌ No test images found")
                return
            test_image_path = os.path.join(processed_dir, images[0])
            
        print(f"\n🔍 Testing detection on: {test_image_path}")
        print(f"   Confidence threshold: {conf_threshold}")
        print(f"   IoU threshold: {iou_threshold}")
        
        # Load image
        image = cv2.imread(test_image_path)
        if image is None:
            print(f"❌ Cannot load image: {test_image_path}")
            return
            
        # Test with different parameters
        results_low = self.model(image, conf=0.5, iou=0.5, max_det=100)
        results_high = self.model(image, conf=conf_threshold, iou=iou_threshold, max_det=10)
        
        low_count = len(results_low[0].boxes) if results_low[0].boxes is not None else 0
        high_count = len(results_high[0].boxes) if results_high[0].boxes is not None else 0
        
        print(f"\n📊 Detection Results:")
        print(f"   Low thresholds (conf=0.5, iou=0.5): {low_count} detections")
        print(f"   High thresholds (conf={conf_threshold}, iou={iou_threshold}): {high_count} detections")
        
        if low_count > high_count * 3:
            print("✓ Improved parameters significantly reduce false positives")
        else:
            print("⚠️  May need even higher thresholds or more training data")
            
        return low_count, high_count
        
    def suggest_improvements(self):
        """Provide specific improvement suggestions"""
        raw_count, processed_count, annotation_count = self.analyze_dataset_size()
        
        print("\n" + "="*50)
        print("IMPROVEMENT RECOMMENDATIONS")
        print("="*50)
        
        # Dataset size recommendations
        if raw_count < 50:
            print("\n🎯 PRIORITY 1: Increase Dataset Size")
            print("   • Collect 50-100 images per fruit class")
            print("   • Take photos from different angles")
            print("   • Vary lighting conditions")
            print("   • Include different backgrounds")
            
        # Augmentation recommendations
        if processed_count < 1000:
            print("\n🎯 PRIORITY 2: Increase Augmentation")
            print("   • Increase augmentation multiplier to 10-15")
            print("   • Add more diverse transformations")
            print("   • Ensure balanced class distribution")
            
        # Model training recommendations
        print("\n🎯 PRIORITY 3: Improve Training")
        print("   • Use consistent model size (yolov8s recommended)")
        print("   • Train for more epochs (150-200)")
        print("   • Use early stopping with patience=30")
        print("   • Monitor validation loss carefully")
        
        # Detection parameters
        print("\n🎯 PRIORITY 4: Optimize Detection Parameters")
        print("   • Use confidence threshold ≥ 0.7")
        print("   • Use IoU threshold ≥ 0.7")
        print("   • Limit max detections to 10-15")
        print("   • Consider ensemble methods")
        
    def create_improved_training_config(self):
        """Create improved training configuration"""
        config = {
            "model_size": "s",  # Small model for better accuracy
            "epochs": 150,
            "batch_size": 8,
            "imgsz": 640,
            "patience": 30,
            "conf_threshold": 0.7,
            "iou_threshold": 0.7,
            "max_det": 10,
            "augmentation_multiplier": 15
        }
        
        with open("./improved_config.json", "w") as f:
            json.dump(config, f, indent=2)
            
        print("\n✓ Created improved_config.json with recommended settings")
        return config
        
    def run_full_analysis(self):
        """Run complete analysis and provide recommendations"""
        print("🔍 FRUIT DETECTION QUALITY ANALYSIS")
        print("="*60)
        
        # Analyze dataset
        self.analyze_dataset_size()
        
        # Test detection if model exists
        if os.path.exists(self.model_path):
            self.test_detection_quality()
        else:
            print(f"\n⚠️  Model not found: {self.model_path}")
            print("   Train a model first before testing detection quality")
            
        # Provide suggestions
        self.suggest_improvements()
        
        # Create improved config
        self.create_improved_training_config()
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("1. Collect more raw images (target: 50+ per class)")
        print("2. Increase augmentation multiplier")
        print("3. Retrain with improved configuration")
        print("4. Test with higher confidence/IoU thresholds")
        print("="*60)


if __name__ == "__main__":
    improver = DetectionImprover()
    improver.run_full_analysis()