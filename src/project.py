import os
from PIL import Image
import pygame
import time

def display_image(image):
    try:
        image.show() 
    except Exception as e:
        print(f"Error displaying image: {e}")

def animate_transition(images, captions):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Portfolio Animation")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    current_index = 0
    running = True
    grid_mode = False

    while running:
        if grid_mode:
            display_grid(screen, images)
        else:
            image = images[current_index]
            animate_slide(screen, image, captions[current_index], font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_index = (current_index + 1) % len(images)
                elif event.key == pygame.K_LEFT:
                    current_index = (current_index - 1) % len(images)
                elif event.key == pygame.K_g:
                    grid_mode = not grid_mode
                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

def animate_slide(screen, image, caption, font):
    screen_width, screen_height = screen.get_size()
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (800, 500))
    
    x = -screen_width
    while x < 0:
        screen.fill((0, 0, 0))
        screen.blit(image_surface, (x, 50)) 
        x += 20
        pygame.display.update()
        pygame.time.delay(30)

    caption_surface = font.render(caption, True, (255, 255, 255))
    caption_rect = caption_surface.get_rect(center=(400, 550))
    screen.blit(caption_surface, caption_rect)

def fade_in(screen, image):
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (800, 500))
    
    alpha = 0
    while alpha < 255:
        image_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image_surface, (0, 50))
        pygame.display.update()
        alpha += 5
        pygame.time.delay(30)

def display_grid(screen, images):
    screen.fill((0, 0, 0))
    cols = 3
    rows = 2
    margin = 10
    thumb_width = (800 - (cols + 1) * margin) // cols
    thumb_height = (600 - (rows + 1) * margin) // rows

    for i, image in enumerate(images[:cols * rows]):
        col = i % cols
        row = i // cols
        x = margin + col * (thumb_width + margin)
        y = margin + row * (thumb_height + margin)
        
        image_surface = pygame.image.load(image.filename).convert()
        image_surface = pygame.transform.scale(image_surface, (thumb_width, thumb_height))
        fade_in_thumbnail(screen, image_surface, x, y)

def fade_in_thumbnail(screen, image_surface, x, y):
    alpha = 0
    while alpha < 255:
        temp_surface = image_surface.copy()
        temp_surface.set_alpha(alpha)
        screen.blit(temp_surface, (x, y))
        pygame.display.update()
        alpha += 10
        pygame.time.delay(20)

def load_images(directory):
    images = []
    captions = []
    if not os.path.isdir(directory):
        print("Invalid directory. Please provide a valid folder path.")
        return images

    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            try:
                image_path = os.path.join(directory, filename)
                images.append(Image.open(image_path))
                captions.append(f"Title: {os.path.splitext(filename)[0]}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"Skipped unsupported file: {filename}")
    return images

def main():
    print("Welcome to the Animated Portfolio Generator!")
    folder_path = input("Enter the folder path where your images are stored: ")
    images = load_images(folder_path)
    if images:
        print(f"{len(images)} images loaded successfully!")
        animate_transition(images[0])
    else:
        print("No images found. Please check the folder path and try again.")

if __name__ == "__main__":
    main()
