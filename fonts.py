import pygame

pygame.init()

# Create a font object (you can choose any font)
font = pygame.font.Font(None, 36)

# Get a list of available fonts
available_fonts = pygame.font.get_fonts()

for font_name in available_fonts:
    print(font_name)

pygame.quit()
