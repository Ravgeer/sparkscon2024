import imgaug.augmenters as iaa
import imageio
import numpy as np
import os

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
    
    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)
        image = imageio.imread(img_path)
        images_augmented = [seq(image=image) for _ in range(num_augmentations)]
        
        for i, img_aug in enumerate(images_augmented):
            aug_img_name = f"{os.path.splitext(img_name)[0]}_aug_{i}{os.path.splitext(img_name)[1]}"
            aug_img_path = os.path.join(output_folder, aug_img_name)
            imageio.imwrite(aug_img_path, img_aug)

# Example usage
input_folder = '/content/drive/MyDrive/Colab Notebooks/scrape_images/apples/granny_smith'
output_folder = '/content/drive/MyDrive/Colab Notebooks/scrape_images/apples/aug_granny_smith'
augment_images(input_folder, output_folder, num_augmentations=100)
