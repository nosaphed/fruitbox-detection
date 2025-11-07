"""
File 6: Main Entry Point - Complete Pipeline
Run seluruh project dari sini dengan menu interactive
"""

import os
import sys

# from pathlib import Path


class FruitDetectionPipeline:
    def __init__(self):
        self.menu_options = {
            "1": self.setup_system,
            "2": self.prepare_data,
            "3": self.generate_annotations,
            "4": self.train_model,
            "5": self.run_detection,
            "6": self.test_on_image,
            "7": self.analyze_dataset,
            "8": self.fix_dataset_structure,
            "0": self.exit_program,
        }

    def clear_screen(self):
        """Clear terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")

    def print_header(self):
        """Print header"""
        print("\n" + "=" * 70)
        print(" " * 15 + "🍎 FRUIT DETECTION SYSTEM 🍊")
        print("=" * 70 + "\n")

    def print_menu(self):
        """Display main menu"""
        self.print_header()
        print("MAIN MENU:")
        print("-" * 70)
        print("  1. Setup System (Install dependencies & create directories)")
        print("  2. Prepare Data (Data augmentation & preprocessing)")
        print("  3. Generate Annotations (Create YOLO format labels)")
        print("  4. Train Model (Train YOLOv8 on dataset)")
        print("  5. Run Detection (Real-time camera detection)")
        print("  6. Test on Image (Test detection on single image)")
        print("  7. Analyze Dataset (Check dataset quality & get recommendations)")
        print("  8. Fix Dataset Structure (Fix train/val split)")
        print("  0. Exit")
        print("-" * 70)

    def setup_system(self):
        """Setup system"""
        print("\n" + "-" * 70)
        print("[STEP 1] SYSTEM SETUP")
        print("-" * 70)

        from setup import (
            install_dependencies,
            setup_project_structure,
            download_sample_backgrounds,
            create_requirements_txt,
            create_readme,
        )

        try:
            install_dependencies()
            print()
            setup_project_structure()
            print()
            download_sample_backgrounds()
            print()
            create_requirements_txt()
            create_readme()

            print("\n[SUCCESS] System setup completed!")

        except Exception as e:
            print(f"\n[ERROR] Setup failed: {e}")

    def prepare_data(self):
        """Prepare data"""
        print("\n" + "-" * 70)
        print("[STEP 2] DATA PREPARATION")
        print("-" * 70)

        # Check if raw images exist
        raw_dir = "./data/raw_images"
        if not os.listdir(raw_dir):
            print(f"\n[ERROR] No PNG images found in {raw_dir}")
            print("Please place your PNG images there first!")
            return

        print("\nRecommended augmentation multiplier: 20-25")
        print("(This will create 220-275 images from 11 raw images)")
        augmentation_times = input(
            "\nEnter augmentation multiplier (default 25): "
        ).strip()
        augmentation_times = (
            int(augmentation_times) if augmentation_times.isdigit() else 25
        )

        try:
            from preparation import DataPreparation

            prep = DataPreparation(
                input_dir=raw_dir,
                output_dir="./data/processed_images",
                background_dir="./data/backgrounds",
            )

            total = prep.process_dataset(augmentation_times=augmentation_times)
            print(f"\n[SUCCESS] Data preparation completed! Total images: {total}")

        except Exception as e:
            print(f"\n[ERROR] Data preparation failed: {e}")

    def generate_annotations(self):
        """Generate annotations"""
        print("\n" + "-" * 70)
        print("[STEP 3] ANNOTATION GENERATION")
        print("-" * 70)

        # Check if processed images exist
        if not os.listdir("./data/processed_images"):
            print("\n[ERROR] No processed images found!")
            print("Please run 'Prepare Data' first!")
            return

        try:
            from annotation_generator import AnnotationGenerator

            ann_gen = AnnotationGenerator()
            ann_gen.generate_annotations(
                "./data/processed_images", "./data/annotations"
            )
            print()
            ann_gen.create_dataset_yaml("./data/dataset.yaml")
            print()
            ann_gen.save_class_info("./data/class_info.json")

            print("\n[SUCCESS] Annotations generated!")

        except Exception as e:
            print(f"\n[ERROR] Annotation generation failed: {e}")

    def train_model(self):
        """Train model"""
        print("\n" + "-" * 70)
        print("[STEP 4] MODEL TRAINING")
        print("-" * 70)

        # Check if annotations exist
        if not os.path.exists("./data/dataset.yaml"):
            print("\n[ERROR] dataset.yaml not found!")
            print("Please run 'Generate Annotations' first!")
            return

        # Get training parameters
        print("\nTraining Parameters:")
        print("-" * 70)
        print("Recommended for small dataset (11 raw images):")
        print("  - Model: n (nano)")
        print("  - Epochs: 80")
        print("  - Batch: 8")
        print("  - Patience: 20")
        print()

        model_size = input("Model size (n/s/m/l, default 'n'): ").strip() or "n"
        epochs = input("Epochs (default 80): ").strip()
        epochs = int(epochs) if epochs.isdigit() else 80

        batch_size = input("Batch size (default 8): ").strip()
        batch_size = int(batch_size) if batch_size.isdigit() else 8

        patience = input("Early stopping patience (default 20): ").strip()
        patience = int(patience) if patience.isdigit() else 20

        try:
            from training import FruitDetectionTrainer

            print("\n[INFO] Starting training with parameters:")
            print(f"  - Model size: {model_size}")
            print(f"  - Epochs: {epochs}")
            print(f"  - Batch size: {batch_size}")
            print(f"  - Patience: {patience}")

            trainer = FruitDetectionTrainer(model_size=model_size)
            trainer.train(
                dataset_yaml_path="./data/dataset.yaml",
                epochs=epochs,
                imgsz=640,
                batch_size=batch_size,
                patience=patience,
            )

            trainer.save_model("./models/fruit_detector_best.pt")
            trainer.validate()

            print("\n[SUCCESS] Model training completed!")

        except Exception as e:
            print(f"\n[ERROR] Training failed: {e}")
            import traceback

            traceback.print_exc()

    def run_detection(self):
        """Run real-time detection"""
        print("\n" + "-" * 70)
        print("[STEP 5] REAL-TIME DETECTION")
        print("-" * 70)

        # Check if model exists
        model_path = "./models/fruit_detector_best.pt"
        if not os.path.exists(model_path):
            print(f"\n[ERROR] Model not found at {model_path}")
            print("Please train the model first!")
            return

        # Get parameters
        camera_id = input("\nCamera ID (default 0): ").strip()
        camera_id = int(camera_id) if camera_id.isdigit() else 0

        confidence = input("Confidence threshold (0-1, default 0.7): ").strip()
        try:
            confidence = float(confidence) if confidence else 0.7
        except ValueError:
            confidence = 0.7

        try:
            from camera_detection import FruitDetectionCamera

            print("\n[INFO] Starting camera detection...")
            print(f"  - Camera ID: {camera_id}")
            print(f"  - Confidence threshold: {confidence}")
            print("\nControls:")
            print("  - Q: Exit")
            print("  - S: Screenshot")

            detector = FruitDetectionCamera(model_path=model_path)
            detector.run_camera(camera_id=camera_id, confidence_threshold=confidence)

        except Exception as e:
            print(f"\n[ERROR] Detection failed: {e}")
            import traceback

            traceback.print_exc()

    def test_on_image(self):
        """Test on single image"""
        print("\n" + "-" * 70)
        print("[STEP 6] TEST ON IMAGE")
        print("-" * 70)

        # Check if model exists
        model_path = "./models/fruit_detector_best.pt"
        if not os.path.exists(model_path):
            print(f"\n[ERROR] Model not found at {model_path}")
            print("Please train the model first!")
            return

        image_path = input("\nEnter image path: ").strip()

        if not os.path.exists(image_path):
            print(f"\n[ERROR] Image not found: {image_path}")
            return

        try:
            from camera_detection import FruitDetectionCamera

            detector = FruitDetectionCamera(model_path=model_path)
            detector.test_on_image(image_path)

        except Exception as e:
            print(f"\n[ERROR] Test failed: {e}")

    def analyze_dataset(self):
        """Analyze dataset quality"""
        print("\n" + "-" * 70)
        print("[STEP 7] DATASET ANALYSIS")
        print("-" * 70)

        try:
            from improve_detection import DetectionImprover

            improver = DetectionImprover()
            improver.run_full_analysis()

        except Exception as e:
            print(f"\n[ERROR] Analysis failed: {e}")

    def fix_dataset_structure(self):
        """Fix dataset structure"""
        print("\n" + "-" * 70)
        print("[STEP 8] FIX DATASET STRUCTURE")
        print("-" * 70)

        try:
            from fix_dataset_structure import fix_dataset_structure

            success = fix_dataset_structure()
            if success:
                print("\n[SUCCESS] Dataset structure fixed!")
            else:
                print("\n[ERROR] Failed to fix dataset structure")

        except Exception as e:
            print(f"\n[ERROR] Fix failed: {e}")

    def exit_program(self):
        """Exit program"""
        print("\n[INFO] Exiting... Goodbye!")
        sys.exit(0)

    def run(self):
        """Main loop"""
        while True:
            self.clear_screen()
            self.print_menu()

            choice = input("Enter your choice (0-8): ").strip()

            if choice in self.menu_options:
                self.menu_options[choice]()
            else:
                print("\n[ERROR] Invalid choice! Please try again.")

            if choice != "0":
                input("\nPress Enter to continue...")


def main():
    """Entry point"""
    try:
        pipeline = FruitDetectionPipeline()
        pipeline.run()
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
