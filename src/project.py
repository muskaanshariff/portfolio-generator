import os
from PIL import Image

def main():
    print("Welcome to the Animated Portfolio Generator!")
    folder_path = input("Enter the folder path where your images are stored: ")
    images = load_images(folder_path)
    if images:
        print(f"{len(images)} images loaded successfully!")
    else:
        print("No images found. Please check the folder path and try again.")

def load_images(directory):
    images = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(directory, filename)
                images.append(Image.open(image_path))
        return images
    except Exception as e:
        print(f"Error loading images: {e}")
        return []

if __name__ == "__main__":
    main()
