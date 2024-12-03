import os
import threading
from PIL import Image
import pygame
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def load_settings():
    default_settings = {
        "transition_speed": 20,
        "grid_layout": [3, 2],
        "background_color": (0, 0, 0),
        "theme": "dark"
    }
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    else:
        return default_settings
    
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def display_grid(screen, images, captions, screen_width, screen_height, settings):
    screen.fill((settings['background_color']))
    cols, rows = settings['grid_layout']
    margin = 10
    thumb_width = (screen_width - (cols + 1) * margin) // cols
    thumb_height = (screen_height - (rows + 1) * margin) // rows
    font = pygame.font.SysFont("Helvetica", 24)

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

        caption_surface = font.render(caption, True, (255, 255, 255))
        caption_rect = caption_surface.get_rect(center=(x + thumb_width // 2, y + thumb_height - 15))
        screen.blit(caption_surface, caption_rect)

def animate_fade_in(screen, image):
    image_surface = pygame.image.load(image.filename).convert()
    image_surface = pygame.transform.scale(image_surface, (900, 500))
    
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
    image_surface = pygame.transform.scale(image_surface, (900, 500))
    
    alpha = 255
    while alpha > 0:
        image_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image_surface, (0, 50))
        pygame.display.update()
        alpha -= 5
        pygame.time.delay(20)

def center_image(image_surface, screen_width, screen_height):
    image_rect = image_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    return image_rect.topleft

def scale_to_fit(image_surface, screen_width, screen_height):
    image_width, image_height = image_surface.get_size()
    aspect_ratio = image_width / image_height

    if screen_width / screen_height > aspect_ratio:
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = screen_width
        new_height = int(new_width / aspect_ratio)

    return pygame.transform.scale(image_surface, (new_width, new_height))

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
def show_start_screen(screen, screen_width, screen_height):
    font = pygame.font.SysFont("Helvetica-Bold", 50)
    welcome_text = font.render("View Portfolio!", True, (255, 79, 55))
    loading_text = font.render("Click Anywhere to Start", True, (255, 79, 55))
    
    welcome_rect = welcome_text.get_rect(center=(screen_width // 2, screen_height // 3))
    loading_rect = loading_text.get_rect(center=(screen_width // 2, screen_height // 2))
    
    alpha = 0
    image_surface = pygame.Surface((screen_width, screen_height))
    image_surface.fill((135, 193, 255)) 
    
    while alpha < 255:
        image_surface.set_alpha(alpha)
        screen.fill((135, 193, 255))  
        screen.blit(image_surface, (0, 0))
        screen.blit(welcome_text, welcome_rect)
        screen.blit(loading_text, loading_rect)
        pygame.display.update()
        alpha += 5
        pygame.time.delay(30) 
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

    while alpha > 0:
        image_surface.set_alpha(alpha)
        screen.fill((135, 193, 255)) 
        screen.blit(image_surface, (0, 0))
        screen.blit(welcome_text, welcome_rect)
        screen.blit(loading_text, loading_rect)
        pygame.display.update()
        alpha -= 5
        pygame.time.delay(30)

    screen.fill((135, 193, 255)) 
    pygame.display.update()

def animate_transition(images, captions):
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Portfolio Animation")
    font = pygame.font.SysFont("Helvetica", 36)
    
    settings = load_settings()
    current_index = 0
    grid_mode = True
    fade_in_done = False
    running = True

    show_start_screen(screen, screen_width, screen_height)

    while running:
        if grid_mode:
            display_grid(screen, images, captions, screen_width, screen_height, settings)
            fade_in_done = False
        else:
            if not fade_in_done:
                animate_fade_in(screen, images[current_index])
                fade_in_done = True
            else:
                image_surface = pygame.image.load(images[current_index].filename).convert()
                image_surface = scale_to_fit(image_surface, screen_width, screen_height)
                screen.fill((0, 0, 0))
                screen.blit(image_surface, center_image(image_surface, screen_width, screen_height))
                
                caption_surface = font.render(captions[current_index], True, (255, 255, 255))
                caption_rect = caption_surface.get_rect(center=(screen_width // 2, screen_height - 50))
                screen.blit(caption_surface, caption_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    grid_mode = True
                elif event.key == pygame.K_RIGHT and not grid_mode:
                    animate_fade_out(screen, images[current_index])
                    current_index = (current_index + 1) % len(images)
                    fade_in_done = False  
                elif event.key == pygame.K_LEFT and not grid_mode:
                    animate_fade_out(screen, images[current_index])
                    current_index = (current_index - 1) % len(images)
                    fade_in_done = False  
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and grid_mode:
                mouse_x, mouse_y = event.pos
                
                cols, rows = settings['grid_layout']
                margin = 10
                thumb_width = (screen_width - (cols + 1) * margin) // cols
                thumb_height = (screen_height - (rows + 1) * margin) // rows
                
                for i, image in enumerate(images):
                    col = i % cols
                    row = i // cols
                    x = margin + col * (thumb_width + margin)
                    y = margin + row * (thumb_height + margin)
                    if x <= mouse_x <= x + thumb_width and y <= mouse_y <= y + thumb_height:
                        current_index = i
                        grid_mode = False
                        fade_in_done = False
                        break

        pygame.display.update()
    pygame.quit()

def save_portfolio_as_pdf(images, captions):
    c = canvas.Canvas("portfolio.pdf", pagesize=letter)
    width, height = letter
    
    for i, (image, caption) in enumerate(zip(images, captions)):
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        max_width = width - 100  
        max_height = height - 150 

        if aspect_ratio > 1: 
            img_width = min(max_width, img_width)
            img_height = img_width / aspect_ratio
        else: 
            img_height = min(max_height, img_height)
            img_width = img_height * aspect_ratio

        caption_x_position = (width - img_width) / 2
        caption_y_position = (height - img_height) / 2 + img_height + 10  
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(caption_x_position, caption_y_position, caption.upper())

        x_position = (width - img_width) / 2
        y_position = (height - img_height) / 2

        c.drawImage(image.filename, x_position, y_position, width=img_width, height=img_height)
        
        c.showPage()
    
    c.save()
    print("Portfolio saved as portfolio.pdf")

def main():
    print("Welcome to the Animated Portfolio Generator!")
    folder_path = input("Enter the folder path where your images are stored: ")
    images, captions = load_images(folder_path)
    if images:
        print(f"{len(images)} images loaded successfully!")

        animation_thread = threading.Thread(target=animate_transition, args=(images, captions))
        animation_thread.start()

        save_choice = input("Would you like to save this portfolio as a PDF? (y/n): ")
        if save_choice.lower() == 'y':
            save_portfolio_as_pdf(images, captions)

        animation_thread.join()
    else:
        print("No images found. Please check the folder path and try again.")

if __name__ == "__main__":
    main()
