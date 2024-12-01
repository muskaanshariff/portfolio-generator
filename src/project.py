import os
from PIL import Image
import pygame

def animate_fade_in(screen, image):
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (800, 500))
    
    alpha = 0
    while alpha < 255:
        image_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image_surface, (0, 50))
        pygame.display.update()
        alpha += 5
        pygame.time.delay(20)

def animate_fade_out(screen, image):
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (800, 500))
    
    alpha = 255
    while alpha > 0:
        image_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image_surface, (0, 50))
        pygame.display.update()
        alpha -= 5
        pygame.time.delay(20)

def display_grid(screen, images, captions):
    screen.fill((0, 0, 0))
    cols, rows = 3, 2
    margin = 10
    thumb_width = (800 - (cols + 1) * margin) // cols
    thumb_height = (600 - (rows + 1) * margin) // rows
    font = pygame.font.Font(None, 24)

    for i, (image, caption) in enumerate(zip(images, captions)):
        col = i % cols
        row = i // cols
        x = margin + col * (thumb_width + margin)
        y = margin + row * (thumb_height + margin)
        
        image_surface = pygame.image.load(image.filename).convert()
        image_surface = pygame.transform.scale(image_surface, (thumb_width, thumb_height))
        
        screen.blit(image_surface, (x, y))

        overlay = pygame.Surface((thumb_width, 30), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (x, y + thumb_height - 30))

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



def load_images(directory):
    images = []
    captions = []
    if not os.path.isdir(directory):
        print("Invalid directory. Please provide a valid folder path.")
        return images, captions

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
    return images, captions

def main():
    print("Welcome to the Animated Portfolio Generator!")
    folder_path = input("Enter the folder path where your images are stored: ")
    images, captions = load_images(folder_path)
    if images:
        print(f"{len(images)} images loaded successfully!")
        animate_transition(images, captions)
    else:
        print("No images found. Please check the folder path and try again.")

if __name__ == "__main__":
    main()
