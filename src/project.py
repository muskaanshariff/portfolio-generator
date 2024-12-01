import os
from PIL import Image
import pygame

def display_image(image):
    try:
        image.show() 
    except Exception as e:
        print(f"Error displaying image: {e}")

def animate_transition(image):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Portfolio Animation")

    clock = pygame.time.Clock()
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (800, 600))

    alpha = 0
    running = True
    while running and alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        image_surface.set_alpha(alpha)
        screen.blit(image_surface, (0, 0))
        pygame.display.update()
        alpha += 5
        clock.tick(30)

    pygame.quit()
    

def main():
    print("Welcome to the Animated Portfolio Generator!")
    folder_path = input("Enter the folder path where your images are stored: ")
    images = load_images(folder_path)
    if images:
        print(f"{len(images)} images loaded successfully!")
        animate_transition(images[0])
    else:
        print("No images found. Please check the folder path and try again.")

def load_images(directory):
    images = []
    if not os.path.isdir(directory):
        print("Invalid directory. Please provide a valid folder path.")
        return images

    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            try:
                image_path = os.path.join(directory, filename)
                images.append(Image.open(image_path))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"Skipped unsupported file: {filename}")
    return images

if __name__ == "__main__":
    main()
