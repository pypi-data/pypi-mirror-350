import os
import cv2
import shutil
import albumentations as A
from tqdm import tqdm

class ImageAugmenter:
    def __init__(self, input_dir, output_dir, brightness_limit=0.3, contrast_limit=0.3):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transform = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=brightness_limit,
                                       contrast_limit=contrast_limit, p=1.0)
        ])
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        for filename in tqdm(os.listdir(self.input_dir), desc="Augmenting images"):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.input_dir, filename)
                label_path = os.path.join(self.input_dir, filename.rsplit('.', 1)[0] + '.txt')

                image = cv2.imread(image_path)
                if image is None:
                    print(f"⚠️ Cannot read image: {filename}")
                    continue

                augmented = self.transform(image=image)
                aug_image = augmented['image']

                aug_img_path = os.path.join(self.output_dir, filename)
                cv2.imwrite(aug_img_path, aug_image)

                if os.path.exists(label_path):
                    aug_label_path = os.path.join(self.output_dir, os.path.basename(label_path))
                    shutil.copy(label_path, aug_label_path)
                else:
                    print(f"⚠️ Label not found for: {filename}")

        print("Image augmentation complete.")
