import imgaug.augmenters as iaa
import imageio
import numpy as np
import os
import argparse

def augment_images(input_folder, output_folder, num_augmentations=100):
    """Apply augmentations to images and save them to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define an augmentation sequence
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),  # Horizontal flips
        iaa.Affine(rotate=(-20, 20)),  # Rotations
        iaa.GaussianBlur(sigma=(0, 3.0)),  # Gaussian blur
        iaa.AdditiveGaussianNoise(scale=(0, 0.2*255)),  # Add Gaussian noise
        iaa.Multiply((0.8, 1.2)),  # Change brightness
    ])
    
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)
        
        if not any(img_name.lower().endswith(ext) for ext in supported_extensions):
            print(f"Skipping unsupported file: {img_name}")
            continue
        
        try:
            image = imageio.imread(img_path)
        except Exception as e:
            print(f"Error reading {img_path}: {e}")
            continue
        
        images_augmented = [seq(image=image) for _ in range(num_augmentations)]
        
        for i, img_aug in enumerate(images_augmented):
            aug_img_name = f"{os.path.splitext(img_name)[0]}_aug_{i}{os.path.splitext(img_name)[1]}"
            aug_img_path = os.path.join(output_folder, aug_img_name)
            try:
                imageio.imwrite(aug_img_path, img_aug)
            except Exception as e:
                print(f"Error writing {aug_img_path}: {e}")

        print(f"Processed {img_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Augment images in a folder.')
    parser.add_argument('input_folder', type=str, help='The input folder containing images.')
    parser.add_argument('output_folder', type=str, help='The output folder to save augmented images.')
    parser.add_argument('--num_augmentations', type=int, default=100, help='Number of augmentations per image.')

    args = parser.parse_args()
    augment_images(args.input_folder, args.output_folder, args.num_augmentations)

