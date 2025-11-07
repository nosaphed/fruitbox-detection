#!/usr/bin/env python3
"""
Fix dataset structure for YOLO training
"""

import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

def fix_dataset_structure():
    """Fix the dataset structure for YOLO training"""
    
    print("🔧 Fixing dataset structure...")
    
    # Source directories
    image_dir = "./data/processed_images"
    label_dir = "./data/annotations"
    
    # Check if source directories exist
    if not os.path.exists(image_dir):
        print(f"❌ Image directory not found: {image_dir}")
        return False
        
    if not os.path.exists(label_dir):
        print(f"❌ Label directory not found: {label_dir}")
        return False
    
    # Get all images
    images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    print(f"📊 Found {len(images)} images")
    
    # Check for corresponding labels
    labels_found = 0
    for img in images:
        label_file = Path(img).stem + ".txt"
        label_path = os.path.join(label_dir, label_file)
        if os.path.exists(label_path):
            labels_found += 1
    
    print(f"📊 Found {labels_found} corresponding labels")
    
    if labels_found == 0:
        print("❌ No labels found! Run annotation generator first.")
        return False
    
    # Split dataset
    train_imgs, val_imgs = train_test_split(
        images, train_size=0.8, random_state=42
    )
    
    # Create target directories
    dirs = [
        "./data/train/images",
        "./data/train/labels", 
        "./data/val/images",
        "./data/val/labels"
    ]
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {d}")
    
    # Copy training files
    print(f"📁 Copying {len(train_imgs)} training images...")
    for img in train_imgs:
        # Copy image
        src_img = os.path.join(image_dir, img)
        dst_img = os.path.join("./data/train/images", img)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding label
        label_file = Path(img).stem + ".txt"
        src_label = os.path.join(label_dir, label_file)
        dst_label = os.path.join("./data/train/labels", label_file)
        
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)
    
    # Copy validation files
    print(f"📁 Copying {len(val_imgs)} validation images...")
    for img in val_imgs:
        # Copy image
        src_img = os.path.join(image_dir, img)
        dst_img = os.path.join("./data/val/images", img)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding label
        label_file = Path(img).stem + ".txt"
        src_label = os.path.join(label_dir, label_file)
        dst_label = os.path.join("./data/val/labels", label_file)
        
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)
    
    # Update dataset.yaml
    yaml_content = f"""path: {os.path.abspath('./data')}
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
    
    print("✓ Updated dataset.yaml")
    print(f"✅ Dataset structure fixed!")
    print(f"   - Training: {len(train_imgs)} images")
    print(f"   - Validation: {len(val_imgs)} images")
    
    return True

if __name__ == "__main__":
    fix_dataset_structure()